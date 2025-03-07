#!/usr/bin/env bash
set -eux
echo "Initializing conda..."
conda init
# Check if any channels are set
channels=$(conda config --show channels 2>/dev/null | grep 'channels:')
if [ -n "$channels" ]; then
    echo "Removing existing Conda channels..."
    conda config --remove-key channels
fi
echo "Adding conda-forge as the only channel..."
conda config --add channels conda-forge
echo "Setting strict channel priority..."
conda config --set channel_priority strict
echo "Verifying channels..."
conda config --show channels
echo "Updating conda..."
conda update -n base --all -y
echo "Creating log directory..."
mkdir -p $LOG_DIR
if [ -d $ENV_DIR ] && find $ENV_DIR -name '*.yaml' | grep -q .; then
    umask 0002;
    for file in $ENV_DIR/*.yaml; do
        conda env update --file "$file" 2>&1 | tee "$LOG_DIR/$(basename "$file").log";
    done;
fi
echo "Cleaning up cache..."
conda clean --all -y
