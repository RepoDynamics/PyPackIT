#!/usr/bin/env bash
set -euxo pipefail

# Redirect stdout and stderr to a file
echo "Creating log directory..."
mkdir -p "$LOG_DIRPATH"
LOG_FILE="${LOG_DIRPATH}/install.log"
exec > >(tee -a "$LOG_FILE") 2>&1

echo "Initializing conda..."
conda init --all

echo "Removing existing Conda channels..."
conda config --remove-key channels 2>/dev/null || true

echo "Adding conda-forge as the only channel..."
conda config --add channels conda-forge

echo "Setting strict channel priority..."
conda config --set channel_priority strict

echo "Verifying channels..."
conda config --show channels

echo "Updating conda..."
conda update -n base --all -y

if [ -d $ENV_DIR ] && find $ENV_DIR -name '*.yaml' | grep -q .; then
    umask 0002;
    for file in $ENV_DIR/*.yaml; do
        conda env update --file "$file" 2>&1 | tee "$LOG_DIRPATH/env_$(basename "$file").log";
    done;
fi

echo "Cleaning up cache..."
conda clean --all -y
