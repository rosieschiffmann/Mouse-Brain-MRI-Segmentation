# Mouse-Brain-MRI-Segmentation
My 4th year MPhys Physics Masters project at the University of Manchester


## Setup Instructions
To recreate the environment used for this project:

1. Clone the repo:
   `git clone https://github.com/rosieschiffmann/Mouse-Brain-MRI-Segmentation.git`
2. Create the environment:
   `conda env create -f environment.yml`
3. Activate it:
   `conda activate nnunet`


## nnU-Net Inference Instructions
To infer brain segmentation labels using nnU-Net trained architecture:

### 1. Pre-processing: Header Correction
The trained model expects voxel spacing to be scaled by a factor of 10 to ensure compatibility with the nnU-Net architecture settings used during training.  


- Place your raw .nii.gz files in an input folder.  

- Go to fix_headers.py, located in nnunet/scripts/ and update your input and output folders accordingly:  

   `input_folder = r"INITIAL_NIFTI_FOLDER"`  

   `output_folder = r"SCALED_NIFTI_FOLDER"`  

- Run the fix_headers.py script  

   `python nnunet/scripts/fix_headers.py`  

- Result: This creates a new folder of images with corrected metadata. Use these scaled images for the next steps.


### 2. Configure the Inference Script  

Open nnunet/scripts/track_inference.py and update the following variables within the command string:


- Input Path (-i): Point this to the folder containing your scaled images.  

- Output Path (-o): Create a new folder where you want the .nii.gz segmentations to be saved.  

- Configuration (-c): Choose between 2d or 3d_fullres.


   - **2d**: Processes the volume slice-by-slice. Faster and lower memory usage.  

   - **3d_fullres**: Processes the entire 3D block. Better for lower resolution images but requires more RAM.


### 3. Execution  

- Ensure your conda environment is active and run the script:  

   `conda activate nnunet`  

   `python nnunet/scripts/inference.py`


- **Note:** There is an additional script for running inferences with emission tracking via CodeCarbon (nnunet/scripts/inference_tracking_emissions.py). Follow the same steps to run this code, remembering to update the emission log output folder.
