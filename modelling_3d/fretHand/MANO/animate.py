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

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


model_path = Path('../mano_v1_2/models')
guitar_path = Path('Guitar2.obj')
n_comps = 45
batch_size = 1

class CustomModel(Entity):
    def __init__(self, model, vertices, faces, **kwargs):
        super().__init__(**kwargs)
        self.model = model
        self.vertices = vertices  # Store vertices
        self.faces = faces  # Store faces
        self.color = color.white
        self.generate_model()  # Generate the initial model
      
        self.animation_time = 0
        self.animation_duration = 2
    def generate_model(self):
        # Update the model with current vertices and faces
        self.model.vertices = self.vertices
        self.model.triangles = self.faces
        self.model.generate()

    def update_model(self, new_vertices, new_faces):
        # Update vertices and faces
        self.vertices = new_vertices
        self.faces = new_faces
        self.generate_model()  # Re-generate the model

    def update(self):
        logging.debug("In update function")
        if self.animation_time < self.animation_duration:
            t = self.animation_time / self.animation_duration
            interpolated_pose = (1 - t) * pose + t * pose_middle_fs2
            logging.debug("Pose Shape:", pose.shape)
            logging.debug("Pose Middle FS2 Shape:", pose_middle_fs2.shape)
            vertices, faces = create_model(model_path, n_comps, batch_size, interpolated_pose, betas, global_orient, transl)
            custom_model.update_model(vertices, faces)
            self.animation_time += time.dt

def create_model(path, n_comps, batch_size, pose, betas, global_orient, transl):
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




def load_position(position_path="default"):
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
            vertices, faces = create_model(model_path, n_comps, batch_size, pose, betas, global_orient, transl)
            return vertices, faces, pose, betas, global_orient, transl,
            
    else:
        # Define default tensors if the file does not exist
        n_comps = 45  
        batch_size = 1
        pose = torch.zeros((batch_size, n_comps))
        betas = torch.zeros((batch_size, 10))
        global_orient = torch.zeros((batch_size, 3))
        transl = torch.zeros((batch_size, 3))
        vertices, faces = create_model(model_path, n_comps, batch_size, pose, betas, global_orient, transl)
        return vertices, faces, pose, betas, global_orient, transl,


# def interpolate(start_pose, end_pose, alpha):
#     """ Linearly interpolate between two poses. """
#     print("Updating pose")
#     return start_pose * (1 - alpha) + end_pose * alpha

from ursina import *

def setup():
    # set up app
    app = Ursina(borderless=False, fullscreen=True)

    camera.position = (1, 11, -20)
    
    #DirectionalLight(color=color.white, direction=(1, -1, 1))

    # Load guitar model
    guitar_model = load_model(str(guitar_path))  
    guitar = Entity(model=guitar_model, world_rotation=(67,158,40),color=rgb(102, 255, 255), scale=(1,1,1),
                world_position=Vec3(0,0,0),  texture='heightmap_1',
                eternal=True, collider='Guitar2.obj')
    guitar.enable
    # window.color = color.light_gray
    global animation_time, animation_duration, pose, pose_middle_fs2, custom_model, betas, global_orient, transl

    # load in default pose
    vertices, faces, pose, betas, global_orient, transl, = load_position()
    vertices_middle_fs2, faces_middle_fs2, pose_middle_fs2, betasload_position_middle_fs2, global_orientload_position_middle_fs2, translload_position_middle_fs2, = load_position("Middle f2s1")

    #vertices, faces = create_model(model_path, n_comps, batch_size, pose, betas, global_orient, transl)
    custom_mesh = Mesh(vertices=vertices, triangles=faces)
    custom_model = CustomModel(model=custom_mesh, vertices=vertices, faces=faces, color=color.blue)
    custom_model.scale = Vec3(22, 22, 22)

    logging.debug("Outside of update function")
    

    def update_hand(vertices, faces, pose_updated, betas_updated, global_orient_updated, transl_updated):
        custom_model.update_model(vertices, faces)
        pose = pose_updated
        betas = betas_updated
        global_orient = global_orient_updated
        trans_l = transl_updated

    EditorCamera()
    app.run()

setup()

