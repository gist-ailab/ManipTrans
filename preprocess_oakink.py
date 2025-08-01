import os
import glob

# generate urdf file for each object

object_list = [
    "O02@0011@00003",
    "O02@0206@00001",
    "O02@0206@00002",
]

template = "assets/obj_urdf_example.urdf"


data_root = '/ailab_mat2/dataset/hand_object_dataset/OakInk-v2'
# /ailab_mat2/dataset/hand_object_dataset/OakInk-v2/object_preview/object_raw/align_ds
visual_path_format = os.path.join(data_root, 'object_preview', 'object_raw', 'align_ds', '{}') # + *.ply
# /ailab_mat2/dataset/hand_object_dataset/OakInk-v2/coacd_object_preview/align_ds
collision_path_format = os.path.join(data_root, 'coacd_object_preview', 'align_ds', '{}') # + *.ply

# the save dir is the same as the collision dir
# the visual path is absolute path
# the collision path is relative path, because the collision file is in the same folder as the urdf file

def check_files_exist(object_id):
    """Check if visual and collision files exist for the given object"""
    visual_dir = visual_path_format.format(object_id)
    collision_dir = collision_path_format.format(object_id)
    
    # Check for .ply files in both directories
    visual_files = glob.glob(os.path.join(visual_dir, "*.ply"))
    collision_files = glob.glob(os.path.join(collision_dir, "*.ply"))
    
    return len(visual_files) > 0, len(collision_files) > 0, visual_files, collision_files

def generate_urdf(object_id, template_content, visual_file_path, collision_file_path):
    """Generate URDF content for the given object"""
    # Replace the mesh filename in the template with absolute paths
    urdf_content = template_content.replace("102_obj.obj", visual_file_path)
    urdf_content = urdf_content.replace("102_obj.obj", collision_file_path)
    
    # Update the robot name to include the object ID
    urdf_content = urdf_content.replace('name="design"', f'name="{object_id}"')
    
    return urdf_content

def main():
    # Read the template URDF file
    with open(template, 'r') as f:
        template_content = f.read()
    
    print("Starting URDF generation for OakInk objects...")
    
    for object_id in object_list:
        print(f"\nProcessing object: {object_id}")
        
        # 1. check visual and collision file exist
        visual_exists, collision_exists, visual_files, collision_files = check_files_exist(object_id)
        
        if not visual_exists:
            print(f"  Warning: No visual files found for {object_id}")
            continue
            
        if not collision_exists:
            print(f"  Warning: No collision files found for {object_id}")
            continue
        
        # Use the first available file from each directory with absolute paths
        visual_file_path = visual_files[0]  # Full absolute path
        collision_file_path = collision_files[0]  # Full absolute path
        
        print(f"  Visual file: {visual_file_path}")
        print(f"  Collision file: {collision_file_path}")
        
        # 2. generate urdf file
        urdf_content = generate_urdf(object_id, template_content, visual_file_path, collision_file_path)
        
        # 3. save to target_dir
        # urdf_filename = f"{object_id}.urdf"
        urdf_filename = os.path.basename(collision_file_path).replace(".ply", ".urdf")

        save_dir = os.path.dirname(collision_file_path)
        urdf_path = os.path.join(save_dir, urdf_filename)
        
        with open(urdf_path, 'w') as f:
            f.write(urdf_content)
        
        print(f"  Generated: {urdf_path}")
    
    print(f"\nURDF generation complete! Files saved to: {save_dir}")

if __name__ == "__main__":
    main()
