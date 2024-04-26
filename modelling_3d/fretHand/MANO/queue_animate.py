import torch
import mano
from mano.utils import Mesh, colors
import glfw
from OpenGL.GL import *
import numpy as np
from ursina import *
from time import time
from pathlib import Path
import json
import logging
from musicClassesLinux import Note, Song
import XMLInterpret
from guitar_sound import GuitarSimulator


# Set up basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Optionally, configure specific loggers if you know which module to target
logger = logging.getLogger('ursina')  # For example, targeting all loggers under 'ursina'
logger.setLevel(logging.INFO)



class CustomModel(Entity):
    def __init__(self, model_path, n_comps, batch_size, **kwargs):
        super().__init__(**kwargs)
        self.model_path = model_path
        self.n_comps = n_comps
        self.batch_size = batch_size
        self.color = color.white
        self.model = None  # This will be set up later
        self.vertices = None  # Initialize vertices
        self.model = None  # This will be set up later
        # self.guitar_simulator = GuitarSimulator()

        # Init hand variables
        self.pose = None
        self.betas = None
        self.global_orient = None
        self.transl = None

        self.next_vertices = None
        self.next_faces = None
        self.next_pose = None
        self.next_betas = None
        self.next_global_orient = None
        self.next_transl = None
        
        # Initialize animation parameters
        self.animation_time = 0
        self.animation_duration = 2
        self.ready = True
        self.animation_queue = []

        # music
        self.music_queue = []
        self.sound_duration = []
        self.current_audio = None
        self.audio_start_time = None
        self.audio_clips = []

    def setup_initial_model(self, vertices, faces):
        self.vertices = vertices
        self.faces = faces
        self.model = Mesh(vertices=vertices, triangles=faces)  # Assuming Mesh setup requires vertices and faces
        self.generate_model()  # Generate the initial model setup

    def generate_model(self):
        # Assume this updates the Entity's rendering data based on self.model
        if self.model:
            self.model.vertices = self.vertices
            self.model.triangles = self.faces
            self.model.generate()

    def update_model(self, new_vertices, new_faces):
        self.vertices = new_vertices
        self.faces = new_faces
        self.generate_model()
    
    def set_next_pose(self, path):
        self.ready = False
        try:
            result = self.load_position(path)
            if result:
                self.next_vertices, self.next_faces, self.next_pose, self.next_betas, self.next_global_orient, self.next_transl = result
                
            else:
                logging.error(f"No position data found for path: {path}")
        except Exception as e:
            logging.error(f"Failed to load next pose due to: {e}")

    def preload_audio(self):
        """Preloads audio files into the dictionary."""
        if self.music_queue:
            for path in self.music_queue:
                full_path = f"sound/{path}.mp3"
                self.audio_clips.append(Audio(full_path, loop=False, autoplay=False))
            logging.info("done preloading")

    def play_audio(self, audio, duration):
        if self.current_audio:
            self.current_audio.stop()  # Stop any currently playing audio
        self.current_audio = audio
        if self.current_audio:
            self.current_audio.play()
            logging.info(f"Playing audio {self.current_audio} for duration: {duration}")
            self.audio_start_time = time.time()
            self.audio_duration = duration

    def update(self):
        # Manage audio playback duration
        if self.current_audio and self.audio_start_time:
            self.ready = False
            if time.time() - self.audio_start_time > self.audio_duration:
                self.current_audio.stop()
                self.current_audio = None  # Reset the current audio
                # Move to next animation only after audio has stopped
                if self.animation_queue and not self.ready:
                    next_pose = self.animation_queue.pop(0)
                    self.set_next_pose(next_pose)
                    self.ready = False

        # Manage animations
        if self.ready and self.animation_queue and not self.current_audio:
            next_pose = self.animation_queue.pop(0)
            self.set_next_pose(next_pose)
            self.ready = False

        # Update model if there is a new pose to transition to
        if self.next_pose is not None and not self.ready:
            if self.animation_time < self.animation_duration:
                t = self.animation_time / self.animation_duration
                interpolated_pose = (1 - t) * self.pose + t * self.next_pose
                vertices, faces = self.create_model(self.model_path, self.n_comps, self.batch_size, interpolated_pose, self.betas, self.global_orient, self.transl)
                self.update_model(vertices, faces)
                self.animation_time += time.dt
            else:
                self.pose = self.next_pose
                self.animation_time = 0
                
                logging.info("Animation completed, model is ready for next pose.")
                # Play audio after animation ends
                if self.audio_clips and self.sound_duration:
                    duration = self.sound_duration.pop(0)
                    audio = self.audio_clips.pop(0)
                    #self.play_audio(audio, duration)
                self.ready = True

    def create_model(self, path, n_comps, batch_size, pose, betas, global_orient, transl):
        lh_model = mano.load(model_path=str(path),
                            is_rhand = True,
                            num_pca_comps=n_comps,
                            batch_size=batch_size,
                            flat_hand_mean=False)

        output = lh_model(betas=betas,
                        global_orient=global_orient,
                        hand_pose=pose,
                        transl=transl,
                        return_verts=True,
                        return_tips = True)


        h_meshes = lh_model.hand_meshes(output)
        j_meshes = lh_model.joint_meshes(output)

        # Example for one hand mesh; you may loop through `h_meshes` if multiple
        hand_mesh = h_meshes[0]  # Assuming at least one mesh is present

        # Extract vertices and faces
        vertices = hand_mesh.vertices  
        faces = hand_mesh.faces  

        vertices_np = np.array(vertices).astype('float32')  # Ensure vertices are float32
        faces_flat = faces.flatten().astype('int32')  # Ensure faces are flattened and int32


        return vertices_np.tolist(), faces_flat.tolist()

    def load_position(self, position_path="default"):
        default_file = Path(f'positions/{position_path}.txt')
        if default_file.exists():
            with open(default_file, 'r') as file:
                # grab json data
                data = json.loads(file.read())
                # default values
                n_comps = 45
                batch_size = 1
                # grab json data from data
                pose = torch.tensor(data['pose'])
                betas = torch.tensor(data['betas'])
                global_orient = torch.tensor(data['global_orient'])
                transl = torch.tensor(data['transl'])
                # creat model
                vertices, faces = self.create_model(model_path, n_comps, batch_size, pose, betas, global_orient, transl)
                return vertices, faces, pose, betas, global_orient, transl,
                
        else:
            # Define default tensors if the file does not exist
            n_comps = 45  
            batch_size = 1
            pose = torch.zeros((batch_size, n_comps))
            betas = torch.zeros((batch_size, 10))
            global_orient = torch.zeros((batch_size, 3))
            transl = torch.zeros((batch_size, 3))
            vertices, faces = self.create_model(model_path, n_comps, batch_size, pose, betas, global_orient, transl)
            return vertices, faces, pose, betas, global_orient, transl,



from ursina import *


#xml_path = Path('/home/zappizap/Projects/Prosthetic_Guitar_Simulator/musicXML_Files/Teapot.xml')
xml_path = Path('../../../CadenCV/output/XML/teapot.xml')
guitar_song = XMLInterpret.XMLInterpret(str(xml_path))

model_path = Path('../mano_v1_2/models')
guitar_path = Path('Guitar2.obj')
n_comps = 45
batch_size = 1

def setup():
    app = Ursina(borderless=False, fullscreen=True)
    camera.position = (1, 11, -20)

    

    # Setting up Guitar
    guitar_model = load_model(str(guitar_path))
    guitar = Entity(model=guitar_model, world_rotation=(67, 158, 40), color=rgb(102, 255, 255), scale=(1, 1, 1),
                    world_position=Vec3(0, 0, 0), texture='heightmap_1', eternal=True, collider='Guitar2.obj')

    # Initialize CustomModel but don't set up the mesh yet
    custom_model = CustomModel(model_path=model_path, n_comps=n_comps, batch_size=batch_size)
   
    # Load initial position and set up the initial model mesh
    vertices, faces, pose, betas, global_orient, transl = custom_model.load_position()
    custom_model.pose = pose
    custom_model.betas = betas
    custom_model.global_orient = global_orient
    custom_model.transl = transl
    guitar_song.printAttribs()

 

    for note in guitar_song.notes:
        custom_model.animation_queue.append(note.animation)
        custom_model.music_queue.append(note.sound)
        custom_model.sound_duration.append(note.noteLengthTime)
   
    custom_model.preload_audio()
    custom_model.setup_initial_model(vertices, faces)
    custom_model.scale = Vec3(22, 22, 22)
    
    
    EditorCamera()
    app.update = custom_model.update
    app.run()

setup()

