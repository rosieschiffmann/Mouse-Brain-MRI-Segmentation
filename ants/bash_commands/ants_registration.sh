#!/bin/bash

# Folder with the subject images
SUBJECT_DIR="./data/subjects"
# The folder where the transforms are saved from the atlas generation step
ATLAS_DIR="./results/atlas"
# Your manually defined labels on the template
TEMPLATE_LABELS="./data/template_labels/TemplateLabels.nii.gz"
# Where to save the subject-space labels
FINAL_OUTPUT="./results/subject_labels"

mkdir -p "$FINAL_OUTPUT"

echo "Warping Template Labels to Subject Space..."

for img in "${SUBJECT_DIR}"/*.nii; do
    sub=$(basename "$img" .nii)
    
    echo "Processing Inverse Transforms for: $sub"

    # ANTs applies transforms in REVERSE order listed:
    # 1. Inverse Warp first (non-linear)
    # 2. Inverted Affine second (linear)
    antsApplyTransforms \
        -d 3 \
        -i "$TEMPLATE_LABELS" \
        -r "$img" \
        -o "${FINAL_OUTPUT}/${sub}_labels_native.nii.gz" \
        -n GenericLabel \
        -t ["${ATLAS_DIR}/${sub}0GenericAffine.mat", 1] \
        -t "${ATLAS_DIR}/${sub}1InverseWarp.nii.gz"
done

echo "Label propagation complete. Results saved to $FINAL_OUTPUT"