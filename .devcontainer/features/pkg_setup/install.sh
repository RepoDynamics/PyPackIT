#!/usr/bin/env bash
set -euxo pipefail

echo "Creating log directory..."
mkdir -p "$LOG_DIR"
LOG_FILE="${LOG_DIR}/install.log"
# Redirect stdout and stderr to a file
exec > >(tee -a "$LOG_FILE") 2>&1

# Create postStartCommand script
POST_START_SCRIPT_DIRPATH="/usr/local/share/app_installation"
POST_START_SCRIPT_FILEPATH="${POST_START_SCRIPT_DIRPATH}/post-start-command.sh"
mkdir -p "$POST_START_SCRIPT_DIRPATH"
{
  echo '#!/usr/bin/env bash'
  echo 'set -euxo pipefail'
} > "$POST_START_SCRIPT_FILEPATH"
chmod +x "$POST_START_SCRIPT_FILEPATH"

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

if ! echo "$PACKAGES" | jq empty; then
    echo "Invalid JSON in PACKAGES"
    exit 1
fi

for conda_env_name in $(echo "$PACKAGES" | jq -r 'keys[]'); do
    value=$(echo "$PACKAGES" | jq -c --arg k "$conda_env_name" '.[$k]')
    packages=$(echo "$value" | jq -c '.packages')

    # Build the base command
    cmd=(
      python "$SCRIPT_FILEPATH"
        --conda-env-name "$conda_env_name"
        --packages "$packages"
        --filepath "$METADATA_FILEPATH"
        --no-self
    )

    # Optionally add --python-version
    if echo "$value" | jq -e 'has("python-version")' > /dev/null; then
        python_version=$(echo "$value" | jq -r '.["python-version"]')
        cmd+=(--python-version "$python_version")
    fi

    # Optionally add --sources
    if echo "$value" | jq -e 'has("sources")' > /dev/null; then
        sources=$(echo "$value" | jq -r '.sources')
        cmd+=(--sources $sources)
    fi

    # Capture and write command output
    output=$("${cmd[@]}")

    # Append output to the file
    while IFS= read -r line; do
        echo "$line" >> "$POST_START_SCRIPT_FILEPATH"
    done <<< "$output"
done

echo "Cleaning up cache..."
conda clean --all -y
