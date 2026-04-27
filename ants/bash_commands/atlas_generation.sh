#!/bin/bash

# Define your paths (Change these to your actual folders)
#INPUT_DIR="/home/user/project/raw_data"
#OUTPUT_DIR="/home/user/project/processed/atlas"

INPUT_DIR="/home/christi/input/input_ANTS"
OUTPUT_DIR="/home/christi/output"

# Create the output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Run the command 
# We use the full path for the output prefix and the input files
antsMultivariateTemplateConstruction2.sh \
  -d 3 \
  -i 4 \
  -o "${OUTPUT_DIR}/template_" \
  "${INPUT_DIR}"/*.nii