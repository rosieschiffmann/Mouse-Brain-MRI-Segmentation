#!/bin/bash

# Path to the template - the "Moving" image
MOVING_TEMPLATE="/home/input/template_template0.nii"
# The atlas labels drawn on that template
TEMPLATE_LABELS="/home/input/final_labels.nii.gz"
# The directory containing the subject images (Fixed targets)
INPUT_DIR="/home/input/test_images"
# Where to save registrations and warped labels
BASE_OUTPUT="/home/output"

# Define specific folders for organization
REG_DIR="${BASE_OUTPUT}/registrations"
LABEL_DIR="${BASE_OUTPUT}/labels"

# Create those folders automatically
mkdir -p "$REG_DIR"
mkdir -p "$LABEL_DIR"

# Registration of template onto subject's space
for FIXED_SUBJECT in "$INPUT_DIR"/*.nii.gz; do
    
    BASE_NAME=$(basename "$FIXED_SUBJECT")
    FILE_ID=${BASE_NAME%.nii*} 

    echo "----------------------------------------------------"
    echo "Processing Subject ID: $FILE_ID"
    echo "----------------------------------------------------"

    # Outputs saved to the 'registrations' folder
    antsRegistrationSyN.sh \
        -d 3 \
        -f "$FIXED_SUBJECT" \
        -m "$MOVING_TEMPLATE" \
        -o "${REG_DIR}/${FILE_ID}_"

    # Forward warping the labels by applying transforms
    # Final masks saved to the 'labels' folder
    echo "Warping labels for: $FILE_ID"
    
    antsApplyTransforms \
        -d 3 \
        -i "$TEMPLATE_LABELS" \
        -r "$FIXED_SUBJECT" \
        -o "${LABEL_DIR}/${FILE_ID}_labels.nii.gz" \
        -n GenericLabel \
        -t "${REG_DIR}/${FILE_ID}_1Warp.nii.gz" \
        -t "${REG_DIR}/${FILE_ID}_0GenericAffine.mat"

done