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




from ursina import *

def setup():
    app = Ursina()

    # Fixed parameters
    betas = torch.rand(batch_size, 10) * .1
    global_orient = torch.rand(batch_size, 3) * .1
    transl = torch.rand(batch_size, 3) * .1

    new_pose = torch.zeros(batch_size, n_comps)  # Start with a neutral pose
    vertices, faces = create_model(model_path, n_comps, batch_size, new_pose, betas, global_orient, transl)
    custom_mesh = Mesh(vertices=vertices, triangles=faces)
    custom_model = CustomModel(model=custom_mesh, vertices=vertices, faces=faces, color=color.blue)
    custom_model.scale = Vec3(50, 50, 50)

    # Create a slider_index_base
    def update_slider_index_base(value=None):
        if slider_index_base.value is None:
            print("Warning: Received None in update_pose")
            print(f"Slider values is: {slider_index_base.value}")
            return
        print(f"Updating pose with value: {slider_index_base.value}")
        
        new_pose[:, 2] = slider_index_base.value
        vertices, faces = create_model(model_path, n_comps, batch_size, new_pose, betas, global_orient, transl)
        custom_model.update_model(vertices, faces)



    slider_index_base = Slider(min=-2, max=2, step=0.01, default=0, dynamic=True)    
    slider_index_base.x =0
    slider_index_base.y = -0.4
    slider_index_base.on_value_changed = update_slider_index_base    
    slider_index_base.text = "Adjust Pose"
    slider_index_base.parent = camera.ui  # Make the slider part of the UI

    # Create a slider_index_middle
    def update_slider_index_middle(value=None):
        if slider_index_middle.value is None:
            print("Warning: Received None in update_pose")
            print(f"Slider values is: {slider_index_middle.value}")
            return
        print(f"Updating pose with value: {slider_index_middle.value}")
        
        new_pose[:, 5] = slider_index_middle.value
        vertices, faces = create_model(model_path, n_comps, batch_size, new_pose, betas, global_orient, transl)
        custom_model.update_model(vertices, faces)



    slider_index_middle = Slider(min=-2, max=2, step=0.01, default=0, dynamic=True)    
    slider_index_middle.x =0
    slider_index_middle.y = -0.2
    slider_index_middle.on_value_changed = update_slider_index_middle    
    slider_index_middle.text = "Adjust Pose"
    slider_index_middle.parent = camera.ui  # Make the slider part of the UI

    EditorCamera()
    app.run()

setup()

