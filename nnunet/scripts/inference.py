import subprocess

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