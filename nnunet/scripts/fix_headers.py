import nibabel as nib
import os
import numpy as np

# Setup paths
input_folder = r"C:\Users\MBCX7BD2\mastersproject\test_images\new_data"
output_folder = r"C:\Users\MBCX7BD2\mastersproject\test_images\new_data_scaled"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Define a threshold: if spacing is smaller than this, we multiply by 10
THRESHOLD = 0.2 

print(f"Checking and Scaling Voxel Spacing in: {input_folder}")

for filename in os.listdir(input_folder):
    if filename.endswith(".nii.gz") or filename.endswith(".nii"):
        img_path = os.path.join(input_folder, filename)
        
        # Load the image
        img = nib.load(img_path)
        zooms = list(img.header.get_zooms())
        
        # Determine the scaling factor
        # If the first dimension (X) is very small, we need to scale up
        if zooms[0] < THRESHOLD:
            factor = 10
            status = "SCALING (10x)"
        else:
            factor = 1
            status = "KEEPING ORIGINAL"

        # Load data in float32 to save RAM
        data = img.get_fdata(dtype=np.float32) 
        
        # Update the Affine Matrix
        new_affine = img.affine.copy()
        new_affine[:3, :3] *= factor
        new_affine[:3, 3] *= factor
        
        # Update the Header Zooms
        new_header = img.header.copy()
        new_zooms = [z * factor for z in zooms[:3]]
        if len(zooms) > 3:
            new_zooms.append(zooms[3])
            
        new_header.set_zooms(new_zooms)

        # Create and Save
        new_img = nib.Nifti1Image(data, new_affine, new_header)
        
        save_path = os.path.join(output_folder, filename)
        if not save_path.endswith('.gz'):
            save_path += '.gz'
            
        nib.save(new_img, save_path)
        print(f"{status}: {filename} | Resulting Spacing: {new_zooms}")

print("\nDone! All files in the output folder now have consistent 'large' headers.")