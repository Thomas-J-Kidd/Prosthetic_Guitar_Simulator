import torch
import mano
from mano.utils import Mesh, colors
import glfw
from OpenGL.GL import *
import numpy as np
from ursina import *
from time import time

model_path = Path('../mano_v1_2/models')
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
    rh_model = mano.load(model_path=str(path),
                        is_rhand= False,
                        num_pca_comps=n_comps,
                        batch_size=batch_size,
                        flat_hand_mean=False)

    output = rh_model(betas=betas,
                    global_orient=global_orient,
                    hand_pose=pose,
                    transl=transl,
                    return_verts=True,
                    return_tips = True)


    h_meshes = rh_model.hand_meshes(output)
    j_meshes = rh_model.joint_meshes(output)

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
    new_pose = torch.zeros(batch_size, n_comps)  # Start with a neutral pose

    
    def slider_value_changed(value=None):
        if slider.value is None:
            print(f"Warning: Received None for joint {joint_index}")
            return
        print(f"Updating joint {joint_index} with value: {slider.value}")
        pose[:, joint_index] = slider.value
        vertices, faces = create_model(model_path, n_comps, batch_size, pose, betas, global_orient, transl)
        update_function(vertices, faces)

    print(f"Slider value: {slider.value}")
    slider.on_value_changed = slider_value_changed

   
    
    return slider



from ursina import *

def setup():
    app = Ursina()

    # Fixed parameters
    betas = torch.rand(batch_size, 10) * .1
    global_orient = torch.rand(batch_size, 3) * .1
    transl = torch.rand(batch_size, 3) * .1

    print(f"Global orient: {global_orient}")
    print(f"Translation: {transl}")

    new_pose = torch.zeros(batch_size, n_comps)  # Start with a neutral pose
    vertices, faces = create_model(model_path, n_comps, batch_size, new_pose, betas, global_orient, transl)
    custom_mesh = Mesh(vertices=vertices, triangles=faces)
    custom_model = CustomModel(model=custom_mesh, vertices=vertices, faces=faces, color=color.blue)
    custom_model.scale = Vec3(50, 50, 50)

    def update_hand(vertices, faces):
        custom_model.update_model(vertices, faces)

    # Creating sliders for different joints
    create_joint_slider(2, -2, 2, 0.01, 0, -0.5, 0.4, "Index Base Pose", update_hand, new_pose, betas, global_orient, transl)
    create_joint_slider(5, -2, 2, 0.01, 0, -0.5, 0.2, "Index Middle Pose", update_hand, new_pose, betas, global_orient, transl)
    create_joint_slider(8, -2, 2, 0.01, 0, -0.5, 0, "Index Tip Pose", update_hand, new_pose, betas, global_orient, transl)


    EditorCamera()
    app.run()

setup()

