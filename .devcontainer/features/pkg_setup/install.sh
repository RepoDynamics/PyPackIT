#!/usr/bin/env bash
set -euxo pipefail
mkdir -p $LOG_DIR
LOG_FILE="${LOG_DIR}/install.log"
# Redirect stdout and stderr to a file
exec > >(tee -a "$LOG_FILE") 2>&1

echo "Initializing conda..."
conda init
echo "Removing existing Conda channels..."
conda config --remove-key channels 2>/dev/null || true
echo "Adding conda-forge as the only channel..."
conda config --add channels conda-forge
echo "Setting strict channel priority..."
conda config --set channel_priority strict
echo "Verifying channels..."
conda config --show channels
echo "Creating log directory..."
python "$SCRIPT_FILEPATH" \
  --packages '["main", "test"]' \
  --filepath "$METADATA_FILEPATH" \
  --python-version "$PYTHON_VERSION" \
  --sources $SOURCES \
  --conda-env-name "$CONDA_ENV_NAME"
echo "Cleaning up cache..."
conda clean --all -y
