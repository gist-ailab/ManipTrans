import os

from oakink2_toolkit.dataset import OakInk2__Dataset
# from manotorch.manolayer import ManoLayer, MANOOutput
# from hand_model import ManoTorchTwoHand
# from o3d_ho_gui import visualize_hand_object

# Load the dataset
oakink2_dataset = OakInk2__Dataset(
    dataset_prefix='/ailab_mat2/dataset/hand_object_dataset/OakInk-v2',
    return_instantiated=True,   # set to False if only metainfo wanted
    anno_offset='anno_preview',
    obj_offset='object_repair', # set to 'object_raw' for downsampled object raw scans
    affordance_offset="object_affordance",
)

# Load sequence
seq_key = 'scene_03__A004/seq__20aed35da30d4b869590__2023-04-22-18-45-27' # convert ++ to /
complex_task_data = oakink2_dataset.load_complex_task(seq_key)
primitive_task_data_list = oakink2_dataset.load_primitive_task(complex_task_data)
for pm_t in primitive_task_data_list:
    print(pm_t.task_desc)


max_frame = max(complex_task_data.frame_range) # start from 0 to max_frame

img_dir = os.path.join(oakink2_dataset.data_prefix, complex_task_data.seq_token)
serials = os.listdir(img_dir)
img_path_format = os.path.join(img_dir, serials[0], '{:06d}.png')

# load obj
obj_list = complex_task_data.scene_obj_list
obj_transforms = complex_task_data.obj_transf
obj_meshes = {}
for obj_key in obj_list:
    print(obj_key) 
    obj = oakink2_dataset._load_obj(obj_key)
    obj_meshes[obj_key] = obj # trimesh



