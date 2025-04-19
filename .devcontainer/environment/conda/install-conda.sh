#!/usr/bin/env bash

set -euxo pipefail

CONDA_ACTIVATION_SCRIPT_RELPATH="etc/profile.d/conda.sh"
MAMBA_ACTIVATION_SCRIPT_RELPATH="etc/profile.d/mamba.sh"

NAME="Miniforge3"
VERSION="latest"
CONDA_DIR="/opt/conda"
CONDA_GROUP="conda"
USERNAME="${SUDO_USER:-$(id -un)}"
NO_CLEAN=true
NO_CACHE_CLEAN=true
INTERACTIVE=false
REINSTALL=false
INSTALLER="/tmp/miniforge.sh"
LOGFILE=""

show_help() {
echo "============="
echo "Install Conda"
echo "============="
echo "Usage: $0 <package-list-file> [OPTIONS]"
echo
echo "Install conda and mamba using the Miniforge installer."
echo
echo "Options:"
echo
echo "    --name <name>           Name of the Miniforge variant to install."
echo "                            Default: '$NAME'"
echo "    --version               Version of the Miniforge variant to install."
echo "                            Either 'latest' or a full version string like '24.11.3-2'."
echo "                            Default: '$VERSION'"
echo "    --conda-dir <path>      Directory to install conda into."
echo "                            Default: '$CONDA_DIR'"
echo "    --group <name>          Name of a user group to give access to conda."
echo "                            Default: 'conda'"
echo "    --username <name>       Name of a user to add to the conda group."
echo "                            This user must already exist."
echo "                            Defaults to the real user running this script."
echo "                            Default: '$USERNAME'"
echo "    --activate <path>       Path to a shell configuration file to append conda initialization to."
echo "                            Can be provided multiple times."
echo "                            Examples:"
echo "                                /etc/skel/.bashrc"
echo "                                /etc/bash.bashrc"
echo "                                /etc/zsh/zshrc"
echo "                                ~/.bashrc"
echo "                                ~/.zshrc"
echo "    --no-clean              Skip removing installer artifacts after installation."
echo "    --no-cache-clean        Skip 'conda clean' commands after installation."
echo "    --interactive           Allow the installer to prompt the user."
echo "    --reinstall             If conda is already installed, uninstall it and continue with the installation."
echo "    --installer <path>      Path to download the Miniforge installer script to."
echo "                            Default: '$INSTALLER'"
echo "    --logfile <path>        Log all output (stdout + stderr) to this file in addition to console."
echo "                            Otherwise output is only printed to the console."
echo "    --help                  Show this help message and exit."
echo
echo "Example:"
echo "    $0 --version 24.11.3-2 --no-clean"
echo
echo "References:"
echo "    Miniforge Docker image: https://github.com/conda-forge/miniforge-images/blob/master/ubuntu/Dockerfile"
echo "    Miniforge repository README: https://github.com/conda-forge/miniforge?tab=readme-ov-file#install"
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --name)
            shift
            NAME=$1
            ;;
        --version)
            shift
            VERSION=$1
            ;;
        --conda-dir)
            shift
            CONDA_DIR=$1
            ;;
        --activate)
            shift
            ACTIVATE_PATHS+=("$1")
            ;;
        --no-clean)
            NO_CLEAN=true
            ;;
        --no-cache-clean)
            NO_CACHE_CLEAN=true
            ;;
        --interactive)
            INTERACTIVE=true
            ;;
        --reinstall)
            REINSTALL=true
            ;;
        --installer)
            shift
            INSTALLER=$1
            ;;
        --logfile)
            shift
            LOGFILE=$1
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            show_help >&2
            exit 1
            ;;
    esac
    shift
done

if [[ -n "$LOGFILE" ]]; then
    echo "📝 Initializing logging to '$LOGFILE'."
    mkdir -p "$(dirname "$LOGFILE")"
    exec > >(tee -a "$LOGFILE") 2>&1
fi

if [ "$(id -u)" -ne 0 ]; then
    echo -e '⛔ This script must be run as root. Use sudo, su, or add "USER root" to your Dockerfile before running this script.' >&2
    exit 1
fi

if command -v conda >/dev/null 2>&1; then
    echo "⚠️ Conda installation found."
    if [[ "$REINSTALL" == true ]]; then
        echo "🗑 Uninstalling conda."
        # Refs:
        # - https://github.com/conda-forge/miniforge?tab=readme-ov-file#uninstall
        # - https://www.anaconda.com/docs/getting-started/miniconda/uninstall#manual-uninstall
        conda init --reverse
        rm -rf "$(conda info --base)"
        rm -f "${HOME}/.condarc"
        rm -rf ${HOME}/.conda
    else
        echo "⏩ Conda is already available; exiting installation."
        exit 0
    fi
fi

INSTALLER_PLATFORM="$(uname)-$(uname -m)"

if [[ "$VERSION" == "latest" ]]; then
    INSTALLER_URL="https://github.com/conda-forge/miniforge/releases/latest/download/$NAME-$INSTALLER_PLATFORM.sh"
else
    INSTALLER_URL="https://github.com/conda-forge/miniforge/releases/download/$VERSION/$NAME-$VERSION-$INSTALLER_PLATFORM.sh"
fi

if command -v wget >/dev/null 2>&1; then
    echo "📥 Downloading installer using wget from $INSTALLER_URL"
    wget --no-hsts "$INSTALLER_URL" -O "$INSTALLER"
elif command -v curl >/dev/null 2>&1; then
    echo "📥 Downloading installer using curl from $INSTALLER_URL"
    curl --fail --location --output "$INSTALLER" "$INSTALLER_URL"
else
    echo "⛔ Neither wget nor curl is available." >&2
    exit 1
fi

echo "📦 Installing conda to $CONDA_DIR"
if [[ "$INTERACTIVE" == true ]]; then
    /bin/bash "$INSTALLER" -p ${CONDA_DIR}
else
    /bin/bash "$INSTALLER" -b -p ${CONDA_DIR}
fi

if [[ "$NO_CACHE_CLEAN" == false ]]; then
    conda clean --tarballs --index-cache --packages --yes
    conda clean --force-pkgs-dirs --all --yes
fi

if [[ "$NO_CLEAN" == false ]]; then
    rm "$INSTALLER"
    find ${CONDA_DIR} -follow -type f -name '*.a' -delete
    find ${CONDA_DIR} -follow -type f -name '*.pyc' -delete
fi

if [[ ${#ACTIVATE_PATHS[@]} -gt 0 ]]; then
    CONDA_SCRIPT="$CONDA_DIR/$CONDA_ACTIVATION_SCRIPT_RELPATH"
    MAMBA_SCRIPT="$CONDA_DIR/$MAMBA_ACTIVATION_SCRIPT_RELPATH"
    for path in "${ACTIVATE_PATHS[@]}"; do
        echo "▶️ Sourcing activation script to '$path'"
        echo ". '$CONDA_SCRIPT'" >> "$path"
        echo ". '$MAMBA_SCRIPT'" >> "$path"
        echo "conda activate base" >> "$path"
    done
fi

# Add group and fix permissions
# - https://github.com/devcontainers/features/blob/8895eb3d161d28ada3a8de761a83135e811cae3d/src/conda/install.sh#L81-L115
groupadd -r "$CONDA_GROUP"
usermod -a -G "$CONDA_GROUP" "$USERNAME"
chown -R "$USERNAME:$CONDA_GROUP" "$CONDA_DIR"
chmod -R g+r+w "$CONDA_DIR"
find "$CONDA_DIR" -type d -print0 | xargs -n 1 -0 chmod g+s
