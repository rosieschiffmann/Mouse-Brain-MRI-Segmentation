import subprocess
import os

# Get the directory where the current script is located
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Automatically set environment variables relative to the script location
os.environ['nnUNet_raw'] = os.path.join(base_path, 'nnUNet_raw')
os.environ['nnUNet_preprocessed'] = os.path.join(base_path, 'nnUNet_preprocessed')
os.environ['nnUNet_results'] = os.path.join(base_path, 'nnUNet_results')

# Perform Inference
command = (
    'nnUNetv2_predict '
    '-i "C:\\Users\\MBCX7BD2\\mastersproject\\test_images\\new_data_scaled" '    # Test images
    '-o "C:\\Users\\MBCX7BD2\\mastersproject\\inferences\\new_data_scaled\\2d" '    # Output folder
    '-d 1 -c 2d -f 0 -chk checkpoint_best.pth' # Dataset ID, config, fold 0 only, using best checkpoint
)

# Tell Python to run the command in the terminal
print("Running nnU-Net prediction...")
subprocess.run(command, shell=True)

print("=========================================")
print("DONE! Prediction complete.")
print("=========================================")