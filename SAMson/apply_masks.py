import os
import nibabel as nib
import numpy as np

# define input folders
brains_folder = r"C:\Users\Rosie\OneDrive - The University of Manchester\Year 4\MPhys Project\shared_files\SEMESTER 2\additional data\new_data_scaled"
masks_folder = r"C:\Users\Rosie\OneDrive - The University of Manchester\Year 4\MPhys Project\shared_files\SEMESTER 2\additional data\masks_scaled_skullstripped"

# define output folder for skullstripped brains
output_folder = r"C:\Users\Rosie\OneDrive - The University of Manchester\Year 4\MPhys Project\shared_files\SEMESTER 2\additional data\brains_skullstripped_samson"

os.makedirs(output_folder, exist_ok=True)

# Find all the original brain files
brain_files = [f for f in os.listdir(brains_folder) if f.endswith('.nii') or f.endswith('.nii.gz')]

print(f"Found {len(brain_files)} brains. Starting skull-stripping process...")
print("-" * 50)

for brain_filename in brain_files:
    # Figure out what the mask filename should be
    base_name = brain_filename.replace('.nii.gz', '').replace('.nii', '')
    mask_filename = f"{base_name}_mask.nii.gz"
    
    brain_path = os.path.join(brains_folder, brain_filename)
    mask_path = os.path.join(masks_folder, mask_filename)
    output_path = os.path.join(output_folder, brain_filename)
    
    # Check if the matching mask actually exists
    if not os.path.exists(mask_path):
        print(f" Warning: Could not find mask for {brain_filename}. Skipping...")
        continue
        
    # Load the brain and the mask
    brain_img = nib.load(brain_path)
    mask_img = nib.load(mask_path)
    
    brain_data = brain_img.get_fdata()
    mask_data = mask_img.get_fdata()
    
    # Apply the mask
    skullstripped_data = brain_data * mask_data
    
    # Save the new brain using the original brain's spatial map (affine)
    stripped_img = nib.Nifti1Image(skullstripped_data, brain_img.affine, brain_img.header)
    nib.save(stripped_img, output_path)
    
    print(f"Successfully stripped and saved: {brain_filename}")
