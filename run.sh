#!/bin/bash

ENV_NAME="chatbot"

echo "Conda base: $(conda info --base)"
source $(conda info --base)/etc/profile.d/conda.sh
echo "Trying to activate $ENV_NAME"
conda activate $ENV_NAME
echo "Active conda env: $CONDA_DEFAULT_ENV"


# Load .env variables if .env exists
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Run the app
streamlit run app.py
