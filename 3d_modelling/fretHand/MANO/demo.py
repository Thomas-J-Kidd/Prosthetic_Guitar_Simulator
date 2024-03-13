
import torch
import mano
from mano.utils import Mesh, colors

model_path = '/home/zappi/Projects/Prosthetic_Guitar_Simulator/3d_modelling/fretHand/mano_v1_2/models'
n_comps = 45
batch_size = 1

rh_model = mano.load(model_path=model_path,
                     is_rhand= False,
                     num_pca_comps=n_comps,
                     batch_size=batch_size,
                     flat_hand_mean=False)

# betas = torch.rand(batch_size, 10)*.1
# pose = torch.rand(batch_size, n_comps)*1
# global_orient = torch.rand(batch_size, 3)
# transl        = torch.rand(batch_size, 3)
test_var = 0.1
test_var2 = -0.2
test_var2a = -0.2
test_var3 = -0.3
test_var4 = -0.2
test_var5 = -0.3
test_var6 = 0.1
betas = torch.tensor([[test_var, test_var, test_var, test_var, test_var, test_var, test_var, test_var, test_var, test_var]])
# pose = torch.tensor([[   test_var2, test_var2, test_var2, test_var2, test_var2, test_var2, test_var2, test_var2, test_var2,
#                          test_var3, test_var3, test_var3, test_var3, test_var3, test_var3, test_var3, test_var3, test_var3,
#                          test_var4, test_var4, test_var4, test_var4, test_var4, test_var4, test_var4, test_var4, test_var4,
#                          test_var5, test_var5, test_var5, test_var5, test_var5, test_var5, test_var5, test_var5, test_var5,
#                          test_var6, test_var6, test_var6, test_var6, test_var6, test_var6, test_var6, test_var6, test_var6,]])
#                         1st: left, right, forward/backward 2nd: twist, twist, forward/backward, 3rd:
pose = torch.tensor([[   test_var2a, test_var2a, test_var2, test_var2a, test_var2a, test_var2, test_var2a, test_var2a, test_var2a,
                         test_var3, test_var3, test_var3, test_var3, test_var3, test_var3, test_var3, test_var3, test_var3,
                         test_var4, test_var4, test_var4, test_var4, test_var4, test_var4, test_var4, test_var4, test_var4,
                         test_var5, test_var5, test_var5, test_var5, test_var5, test_var5, test_var5, test_var5, test_var5,
                         test_var6, test_var6, test_var6, test_var6, test_var6, test_var6, test_var6, test_var6, test_var6,]])
global_orient = torch.tensor([[0, 0, 0]])
transl = torch.tensor([[0, 0, 0]])
print(f"These are the variables being randomly generated:\nBetas: {betas}\nPose: {pose}\nGlobal Orient: {global_orient}\nTransl: {transl}")

output = rh_model(betas=betas,
                  global_orient=global_orient,
                  hand_pose=pose,
                  transl=transl,
                  return_verts=True,
                  return_tips = True)


h_meshes = rh_model.hand_meshes(output)
j_meshes = rh_model.joint_meshes(output)


def render_guitar(obj_file_path, vc=colors['purple']):
    # Load the guitar mesh from the obj file
    mesh = Mesh(filename=obj_file_path)

    # Optionally, set other properties such as wireframe or smooth
    # mesh.wireframe = True
    # mesh.smooth = True

    # Return the guitar mesh object
    return mesh

# Example usage:
guitar_mesh = render_guitar("/home/zappi/Projects/Prosthetic_Guitar_Simulator/3d_modelling/FINALMODEL.obj")
# guitar_mesh.show()

#visualize hand mesh only
h_meshes[0].show()

#visualize joints mesh only
# j_meshes[0].show()

#visualize hand and joint meshes
# hj_meshes = Mesh.concatenate_meshes([h_meshes[0], guitar_mesh])
# hj_meshes.show() 

