#!/bin/bash

ENV_NAME="chatbot"

# Step 1: Create the conda environment
conda create --yes --name $ENV_NAME python=3.11

# Step 2: Activate conda for scripting
source $(conda info --base)/etc/profile.d/conda.sh

# Step 3: Activate the environment
conda activate $ENV_NAME

# Step 4: Install pip requirements
pip install -r requirements.txt

echo "Setup complete! Now run './run.sh' to start the app."
