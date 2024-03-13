
import torch
import mano
from mano.utils import Mesh

model_path = '/home/tk/Projects/OpenSource/guitarHand/mano_v1_2/models'
n_comps = 45
batch_size = 1

rh_model = mano.load(model_path=model_path,
                     is_rhand= True,
                     num_pca_comps=n_comps,
                     batch_size=batch_size,
                     flat_hand_mean=False)

betas = torch.rand(batch_size, 10)*1
pose = torch.rand(batch_size, n_comps)*1
var1 = 0.1
var2 = 1
var3 = 1
var4 = 1
var5 = 1
var6 = 0.1
var7 = 0.1
var8 = 0.1
var9 = 0.1
var10 = 0.1
# pose = torch.tensor([[var1, var2, var3, var4, var5, var6, var7, var8, var9, var10]])

global_orient = torch.rand(batch_size, 3)
transl        = torch.rand(batch_size, 3)
print(f"These are the variables being randomly generated:\nBetas: {betas}\nPose: {pose}\nGlobal Orient: {global_orient}\nTransl: {transl}")

output = rh_model(betas=betas,
                  global_orient=global_orient,
                  hand_pose=pose,
                  transl=transl,
                  return_verts=True,
                  return_tips = True)


h_meshes = rh_model.hand_meshes(output)
j_meshes = rh_model.joint_meshes(output)

#visualize hand mesh only
h_meshes[0].show()

#visualize joints mesh only
# j_meshes[0].show()

#visualize hand and joint meshes
# hj_meshes = Mesh.concatenate_meshes([h_meshes[0], j_meshes[0]])
# hj_meshes.show() 

