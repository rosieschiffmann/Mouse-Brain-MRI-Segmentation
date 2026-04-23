# Mouse-Brain-MRI-Segmentation
This repository contains code and documentation for my 4th year MPhys Physics Masters project at the University of Manchester. I have completed the following steps to arrive at a fully functional CNN for inferring mouse bran segmentations:
1. Generate a population-representitive atlas, with labels.
2. Perform atlas based image registration using Advanced Normalisation Tools (ANTs).
3. Use registered labels to train nnU-Net CNN architecture.

# Machine Learning Based Segmentation

In order to perform ML based segmentation in this project, nnU-Net architecture was utilised. Below, both inference and retraining processes are explained 


The results of fold 0 training in the 2d configuration are stored in this repository. However, the full 5 folds for 2d and 3d can be accessed via Zenodo:
   - 2d model results: [zenodo.19709402](https://doi.org/10.5281/zenodo.19709402)
   - 3d_fullres model results: [zenodo.19709506](https://doi.org/10.5281/zenodo.19709506)


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

#### 1. Pre-processing: Header Correction
The trained model expects voxel spacing to be scaled by a factor of 10 to ensure compatibility with the nnU-Net architecture settings used during training.  


- Place your raw .nii.gz files in an input folder.  

- Go to fix_headers.py, located in nnunet/scripts/ and update your input and output folders accordingly:  

   `input_folder = r"INITIAL_NIFTI_FOLDER"`  

   `output_folder = r"SCALED_NIFTI_FOLDER"`  

- Run the fix_headers.py script  

   `python nnunet/scripts/fix_headers.py`  

- Result: This creates a new folder of images with corrected metadata. Use these scaled images for the next steps.


#### 2. Configure the Inference Script  

Open nnunet/scripts/track_inference.py and update the following variables within the command string:


- Input Path (-i): Point this to the folder containing your scaled images.  

- Output Path (-o): Create a new folder where you want the .nii.gz segmentations to be saved.  

- Configuration (-c): Choose between 2d or 3d_fullres.


   - **2d**: Processes the volume slice-by-slice. Faster and lower memory usage.  

   - **3d_fullres**: Processes the entire 3D block. Better for lower resolution images but requires more RAM.


#### 3. Execution  

- Ensure your conda environment is active and run the script:  

   `conda activate nnunet`  

   `python nnunet/scripts/inference.py`


- **Note:** There is an additional script for running inferences with emission tracking via CodeCarbon (nnunet/scripts/inference_tracking_emissions.py). Follow the same steps to run this code, remembering to update the emission log output folder.


## Retraining the Model (Adding New Data)
If you have acquired new labelled mouse brains and wish to improve the model's accuracy, follow this pipeline to retrain and update the network.

#### 1. Prepare New Data  

- 10x Header Scaling: Every new .nii.gz scan must be processed with fix_headers.py (located in nnunet/scripts/) to ensure the voxel spacing matches the model's expected 10x scale.  
- Naming Convention: Ensure each new training brain and corresponding label map follows the naming convention, and move these images into the required nnU-Net folder structure.
   * Training Images: MouseIDName_0000.nii.gz
   * Training Labels: MouseIDName.nii.gz
   * Label Intensities: The voxel values and regions in your label maps must match the indices defined in dataset.json
   * Placement: Move these into nnunet/nnUNet_raw/Dataset001_MouseBrain/imagesTr and labelsTr respectively. 

- Data Pooling: Add the original training data used to the same folders. These can be found on the lab PC, in the imagesTr and labelsTr folders, or on Zenodo. Using a combined dataset (containing both original and new trainign data) prevents catastrophic forgetting during the fine-tuning process.
   - original training images: [zenodo.19708196](https://doi.org/10.5281/zenodo.19708196)
   - Original training labels: [zenodo.19708248](https://doi.org/10.5281/zenodo.19708248)

- Metadata: Update the new dataset.json in the nnUNet_raw folder, changing the `"numTraining":` item to reflect the new total number of images in the imagesTr folder. 

#### 2. Update Environment Variables  

Before running the commands, ensure your terminal knows where the modular folders are. Run these in your PowerShell session:  


   `$env:nnUNet_raw="C:\path\to\repo\nnunet\nnUNet_raw"`  

   `$env:nnUNet_preprocessed="C:\path\to\repo\nnunet\nnUNet_preprocessed"`  

   `$env:nnUNet_results="C:\path\to\repo\nnunet\nnUNet_results"`  

#### 3. Pre-processing & Fingerprinting
Prior to training, nnU-Net must analyse the new data distribution. Run:

   `nnUNetv2_plan_and_preprocess -d 1 -c 2d`  

- d 1: Dataset ID.

- c 2d: Configuration (use 3d_fullres if retraining the 3D model).

#### 4. The Fine-Tuning Command  

To "add" to the current model knowledge, use the -pretrained_weights flag. This tells nnU-Net to load your existing checkpoint_best.pth as the starting point.


`nnUNetv2_train 1 2d 0 -pretrained_weights "C:\path\to\repo\nnunet\nnUNet_results\Dataset001_MouseBrain\nnUNetTrainer__nnUNetPlans__2d\fold_0\checkpoint_best.pth"`


   - d 1: Dataset ID.

   - c 2d: Configuration (use 3d_fullres if retraining the 3D model).

   - f 0: Fold 0.

   - pretrained_weights: Path to the current "best" model weights.  

Results: the new updated model weights will overwrite the original checkpoint_best.pth file.
- **Note:** to avoid overwriting, rename the original checkpoint_best.pth file to checkpoint_best_v1.pth, and adjust the pretrained weights path accordingly. 
