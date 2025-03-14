#!/usr/bin/env bash
set -eux
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
mkdir -p $LOG_DIR
python "$SCRIPT_FILEPATH" \
  --filepath "$METADATA_FILEPATH" \
  --packages "$PACKAGES" \
  --python-version "$PYTHON_VERSION" \
  --sources $SOURCES \
  --conda-env-name "$CONDA_ENV_NAME" | tee "$LOG_DIR/pkg_install.log"
echo "Cleaning up cache..."
conda clean --all -y
