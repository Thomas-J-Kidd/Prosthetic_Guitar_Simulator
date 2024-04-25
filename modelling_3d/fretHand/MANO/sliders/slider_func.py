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

def create_joint_slider(joint_index, min_value, max_value, step, default_value, position_x, position_y, label, update_function, pose, betas, global_orient, transl):
    slider = Slider(min=min_value, max=max_value, step=step, default=default_value, dynamic=True)
    slider.x = position_x
    slider.y = position_y
    slider.text = label
    slider.parent = camera.ui

    
    def slider_value_changed(value=None):
        if slider.value is None:
            print(f"Warning: Received None for joint {joint_index}")
            return
        print(f"Updating joint {joint_index} with value: {slider.value}")
        pose[:, joint_index] = slider.value
        vertices, faces = create_model(model_path, n_comps, batch_size, pose, betas, global_orient, transl)
        update_function(vertices, faces, pose, betas, global_orient, transl)

    print(f"Slider value: {slider.value}")
    slider.on_value_changed = slider_value_changed 
    return slider

def create_orientation_slider(orient_index, min_value, max_value, step, default_value, position_y, label, pose, betas, global_orient, transl, update_function):
    slider = Slider(min=min_value, max=max_value, step=step, default=default_value, dynamic=True)
    slider.x = 0
    slider.y = position_y
    slider.text = label
    slider.parent = camera.ui

    def on_orientation_changed(value=None):
        if slider.value is not None:
            print(f"Orientation {label} updated to: {slider.value} radians")
            global_orient[0, orient_index] = slider.value
            vertices, faces = create_model(model_path, n_comps, batch_size, pose, betas, global_orient, transl)
            update_function(vertices, faces, pose, betas, global_orient, transl)
        else:
            print(f"Warning: Slider for {label} returned None")

    slider.on_value_changed = on_orientation_changed
    return slider

def create_translation_slider(orient_index, min_value, max_value, step, default_value, position_y, label, pose, betas, global_orient, transl, update_function):
    slider = Slider(min=min_value, max=max_value, step=step, default=default_value, dynamic=True)
    slider.x = 0
    slider.y = position_y
    slider.text = label
    slider.parent = camera.ui

    def on_orientation_changed(value=None):
        if slider.value is not None:
            print(f"Orientation {label} updated to: {slider.value} radians")
            transl[0, orient_index] = slider.value
            vertices, faces = create_model(model_path, n_comps, batch_size, pose, betas, global_orient, transl)
            update_function(vertices, faces, pose, betas, global_orient, transl)
        else:
            print(f"Warning: Slider for {label} returned None")

    slider.on_value_changed = on_orientation_changed
    return slider

def save_position(filename, model, pose, betas, global_orient, transl):
    position_dir = Path('positions')
    position_dir.mkdir(exist_ok=True)
    with open(position_dir / f'{filename}.txt', 'w') as f:
        data = {
            'vertices': model.vertices,
            'faces': model.faces,
            'pose': pose.tolist(),
            'betas': betas.tolist(),
            'global_orient': global_orient.tolist(),
            'transl': transl.tolist()
            
        }
        json.dump(data, f) 
    print(f'Position saved as {filename}.txt in "positions" directory')

def load_default_position():
    default_file = Path('positions/default.txt')
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

    

from ursina import *

def setup():
    # set up app
    app = Ursina(borderless=False, fullscreen=True)

    camera.position = (0, 0, -10)
    #DirectionalLight(color=color.white, direction=(1, -1, 1))

    # Load guitar model
    guitar_model = load_model(str(guitar_path))  
    guitar = Entity(model=guitar_model, world_rotation=(67,158,40),color=rgb(102, 255, 255), scale=(1,1,1),
                world_position=Vec3(0,0,0),  texture='heightmap_1',
                eternal=True, collider='Guitar2.obj')
    guitar.enable
    # window.color = color.light_gray

    # load in default pose
    vertices, faces, pose, betas, global_orient, transl, = load_default_position()

    #vertices, faces = create_model(model_path, n_comps, batch_size, pose, betas, global_orient, transl)
    custom_mesh = Mesh(vertices=vertices, triangles=faces)
    custom_model = CustomModel(model=custom_mesh, vertices=vertices, faces=faces, color=color.blue)
    custom_model.scale = Vec3(22, 22, 22)

    def update_hand(vertices, faces, pose_updated, betas_updated, global_orient_updated, transl_updated):
        custom_model.update_model(vertices, faces)
        pose = pose_updated
        betas = betas_updated
        global_orient = global_orient_updated
        transl = transl_updated

    # Global Orient Sliders
    # create_orientation_slider(0, -np.pi, np.pi, 0.01, 0, 0.2, 'Rotate X', pose, betas, global_orient, transl, update_hand)
    # create_orientation_slider(1, -np.pi, np.pi, 0.01, 0, 0.1, 'Rotate Y', pose, betas, global_orient, transl, update_hand)
    # create_orientation_slider(2, -np.pi, np.pi, 0.01, 0, 0, 'Rotate Z', pose, betas, global_orient, transl, update_hand)

    # Tranlational Sliders
    # create_translation_slider(0, -np.pi, np.pi, 0.01, 0, -0.3, 'Rotate X', pose, betas, global_orient, transl, update_hand)
    # create_translation_slider(1, -np.pi, np.pi, 0.01, 0, -0.2, 'Rotate Y', pose, betas, global_orient, transl, update_hand)
    # create_translation_slider(2, -np.pi, np.pi, 0.01, 0, -0.1, 'Rotate Z', pose, betas, global_orient, transl, update_hand)

    # Creating sliders for different joints
    create_joint_slider(2, -2, 2, 0.01, 0, -0.5, 0.4, "Index Base Pose", update_hand, pose, betas, global_orient, transl)
    create_joint_slider(5, -2, 2, 0.01, 0, -0.5, 0.2, "Index Middle Pose", update_hand, pose, betas, global_orient, transl)
    create_joint_slider(8, -2, 2, 0.01, 0, -0.5, 0, "Index Tip Pose", update_hand, pose, betas, global_orient, transl)
    

    # Button to save the position
    def on_save():
        filename = input_field.text if input_field.text else 'default_position'
        save_position(filename, custom_model, pose, betas, global_orient, transl)
    
    # button for reset
    def on_reset():
        vertices, faces, pose, betas, global_orient, transl, = load_default_position()
        vertices, faces = create_model(model_path, n_comps, batch_size, pose, betas, global_orient, transl)
        custom_model.update_model(vertices, faces)


    # Text field for filename
    input_field = InputField(default_value='filename', scale=(0.2, 0.05), size=Vec2(0.1, 0.04))
    input_field.x = 0.6  # Adjust according to the full screen
    input_field.y = 0.43
    input_field.max_length = 20  # Limit text input length if necessary

    # Button to save the position
    save_button = Button(text='Save', scale=(0.05, 0.05), color=color.azure)
    save_button.x = 0.6
    save_button.y = 0.48
    save_button.on_click = lambda: on_save()

    # Button to save the position
    reset_button = Button(text='Reset', scale=(0.08, 0.05), color=color.azure)
    reset_button.x = -0.6
    reset_button.y = 0.48
    reset_button.on_click = lambda: on_reset()

    EditorCamera()
    app.run()

setup()

