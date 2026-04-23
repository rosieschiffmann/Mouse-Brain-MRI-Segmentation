from codecarbon import EmissionsTracker
import subprocess

# Initialize the tracker 
tracker = EmissionsTracker(
    project_name="nnUNet_2D_new_data_LabPC", 
    # Enter your desired output folder for emissions data
    output_dir=r"C:\Users\MBCX7BD2\mastersproject\emissions\new_data_scaled"
)

print("Starting CodeCarbon Energy Tracker...")
tracker.start()

# Perfrom Inference
command = (
    'nnUNetv2_predict '
    '-i "C:\\Users\\MBCX7BD2\\mastersproject\\test_images\\new_data_scaled" '    # Test images
    '-o "C:\\Users\\MBCX7BD2\\mastersproject\\inferences\\new_data_scaled\\2d" '    # Output folder
    '-d 1 -c 2d -f 0 1 2 3 4 -chk checkpoint_best.pth'
)

# Tell Python to run the command in the terminal
print("Running nnU-Net prediction...")
subprocess.run(command, shell=True)

# Stop the tracker once the command finishes
emissions = tracker.stop()

print("=========================================")
print(f"DONE! Total Emissions: {emissions:.6f} kg CO2eq")
print("=========================================")