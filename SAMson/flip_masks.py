import os
import nibabel as nib
import numpy as np

# Define folder of un-flipped masks
input_folder = r"C:\Users\Rosie\OneDrive - The University of Manchester\Year 4\MPhys Project\shared_files\SEMESTER 2\SAMson\SAMson\skullstripped\full_auto"

# Define folder to save flipped masks
output_folder = r"C:\Users\Rosie\OneDrive - The University of Manchester\Year 4\MPhys Project\shared_files\SEMESTER 2\additional data\new_data_scaled_skullstripped"

# Create the output folder automatically if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Get un-flipped mask files
files = [f for f in os.listdir(input_folder) if f.endswith('.nii') or f.endswith('.nii.gz')]
print(f"Found {len(files)} masks to process. Starting flip...")
print("-------------------------------------------------")

# Flip and save masks
for filename in files:
    input_path = os.path.join(input_folder, filename)
    output_path = os.path.join(output_folder, filename)
    
    # Load the NIfTI file and extract the 3D array
    img = nib.load(input_path)
    data = img.get_fdata()
    
    # Reverse the order of the slices along the Z-axis (axis=2)
    flipped_data = np.flip(data, axis=2)
    
    # Create a new NIfTI file with the flipped data, keeping the original spatial map
    flipped_img = nib.Nifti1Image(flipped_data, img.affine, img.header)
    
    # Save the corrected file
    nib.save(flipped_img, output_path)
    print(f"Flipped and saved: {filename}")