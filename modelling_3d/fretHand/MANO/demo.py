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
        self.last_update_time = time()
        self.update_interval = 0.5  # Update every 0.5 seconds
        self.color = color.white

    def update(self):
        current_time = time()
        if current_time - self.last_update_time > self.update_interval:
            self.pose_index = (self.pose_index + 1) % len(self.poses)
            new_vertices, new_faces = self.poses[self.pose_index]
            self.model.vertices = new_vertices
            self.model.triangles = new_faces
            self.model.generate()
            self.last_update_time = current_time


    def set_poses(self, poses):
        # Set the animation poses
        self.poses = poses
        self.pose_index = 0


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


    return vertices_np, faces_flat



def setup():
    app = Ursina()

    # Fixed parameters
    betas = torch.rand(batch_size, 10) * .1
    global_orient = torch.rand(batch_size, 3) * .1
    transl = torch.rand(batch_size, 3) * .1

    poses = []  # Will store vertices for different poses
    for _ in range(10):  # Assuming 10 poses for example
        new_pose = torch.rand(batch_size, n_comps) * 0.2  # Randomly generate a new pose
        vertices, faces = create_model(model_path, n_comps, batch_size, new_pose, betas, global_orient, transl)
        poses.append((vertices.tolist(), faces.tolist()))
        
    initial_vertices, initial_faces = poses[0]  # Unpack the first pose

    custom_mesh = Mesh(vertices=initial_vertices, triangles=initial_faces)  # Assuming triangles can be updated

    custom_model = CustomModel(model=custom_mesh, vertices=initial_vertices, faces=initial_faces, color=color.blue)
    custom_model.scale = Vec3(10, 10, 10)
    custom_model.set_poses(poses)

    EditorCamera()
    app.run()


setup()

