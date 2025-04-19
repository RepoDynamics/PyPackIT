#!/usr/bin/env bash

set -euxo pipefail

# Constants
CONDA_ACTIVATION_SCRIPT_RELPATH="etc/profile.d/conda.sh"
MAMBA_ACTIVATION_SCRIPT_RELPATH="etc/profile.d/mamba.sh"

# Default arguments
NAME="Miniforge3"
VERSION="latest"
CONDA_DIR="/opt/conda"
GROUP="conda"
USER="${SUDO_USER:-$(id -un)}"
ACTIVATES=()
NO_CLEAN=false
NO_CACHE_CLEAN=false
INTERACTIVE=false
REINSTALL=false
INSTALLER_DIR="/tmp/miniforge"
LOGFILE=""
DEBUG=false

show_help() {
echo "============="
echo "Install Conda"
echo "============="
echo "Usage: $0 [OPTIONS]"
echo
echo "Install conda and mamba on Linux or macOS using the Miniforge installer."
echo
echo "Options:"
echo "    --name <name>           Name of the Miniforge variant to install."
echo "                            Default: '$NAME'"
echo "    --version               Version of the Miniforge variant to install."
echo "                            Either 'latest' or a full version string like '24.11.3-2'."
echo "                            Default: '$VERSION'"
echo "    --conda-dir <path>      Directory to install conda into."
echo "                            This corresponds to the CONDA_DIR environment variable."
echo "                            Default: '$CONDA_DIR'"
echo "    --group <name>          Name of a user group to give access to conda."
echo "                            Default: '$GROUP'"
echo "    --user <name>           Name of a user to add to the conda group."
echo "                            This user must already exist."
echo "                            Defaults to the real user running this script."
echo "                            Default: '$USER'"
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
echo "    --installer-dir <path>  Path to directory to download the Miniforge installer to."
echo "                            Default: '$INSTALLER_DIR'"
echo "    --logfile <path>        Log all output (stdout + stderr) to this file in addition to console."
echo "                            Otherwise output is only printed to the console."
echo "    --debug                 Enable debug mode."
echo "    --help                  Show this help message and exit."
echo
echo "Example:"
echo "    $0 --version 24.11.3-2 --no-clean"
echo
echo "References:"
echo "    - Miniforge Docker image: https://github.com/conda-forge/miniforge-images/blob/master/ubuntu/Dockerfile"
echo "    - Miniforge repository README: https://github.com/conda-forge/miniforge?tab=readme-ov-file#install"
echo "    - Devcontainers conda feature: https://github.com/devcontainers/features/tree/main/src/conda"
}

OPTS=$(
    getopt \
        --longoptions name:,version:,conda-dir:,group:,user:,activate:,no-clean,no-cache-clean,interactive,reinstall,installer-dir:,logfile:,debug,help \
        --name "$0" \
        --options '' \
        -- "$@"
)

if [[ $? -ne 0 ]]; then
    echo "Failed to parse options." >&2
    exit 1
fi

eval set -- "$OPTS"

while true; do
    case "$1" in
        --name) NAME="$2"; shift 2;;
        --version) VERSION="$2"; shift 2;;
        --conda-dir) CONDA_DIR="$2"; shift 2;;
        --group) GROUP="$2"; shift 2;;
        --user) USER="$2"; shift 2;;
        --activate) ACTIVATES+=("$2"); shift 2;;
        --no-clean) NO_CLEAN=true; shift;;
        --no-cache-clean) NO_CACHE_CLEAN=true; shift;;
        --interactive) INTERACTIVE=true; shift;;
        --reinstall) REINSTALL=true; shift;;
        --installer-dir) INSTALLER_DIR="$2"; shift 2;;
        --logfile) LOGFILE="$2"; shift 2;;
        --debug) DEBUG=true; shift;;
        --help) show_help; exit 0;;
        --) shift; break;;
        *) echo "Unknown option: $1" >&2; show_help >&2; exit 1;;
    esac
done

if ! [[ "$DEBUG" == true ]]; then
    set +x
fi

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
        rm -f "$HOME/.condarc"
        rm -rf "$HOME/.conda"
        user_home=$(getent passwd "$USER" | cut -d: -f6)
        rm -rf "$user_home/.condarc"
        rm -rf "$user_home/.conda"
    else
        echo "⏩ Conda is already available; exiting installation."
        exit 0
    fi
fi

INSTALLER_PLATFORM="$(uname)-$(uname -m)"

mkdir -p "$INSTALLER_DIR"
INSTALLER_FILENAME="$NAME-$VERSION-$INSTALLER_PLATFORM.sh"
INSTALLER="$INSTALLER_DIR/$INSTALLER_FILENAME"
INSTALLER_CHECKSUM="$INSTALLER_DIR/$INSTALLER_FILENAME.sha256"

if [[ "$VERSION" == "latest" ]]; then
    INSTALLER_URL="https://github.com/conda-forge/miniforge/releases/latest/download/$NAME-$INSTALLER_PLATFORM.sh"
    CHECKSUM_URL=""
else
    INSTALLER_URL="https://github.com/conda-forge/miniforge/releases/download/$VERSION/$INSTALLER_FILENAME"
    CHECKSUM_URL="$INSTALLER_URL.sha256"
fi

trap 'echo "💥 Script failed"; rm -f "$INSTALLER"; rm -f "$INSTALLER_CHECKSUM"' ERR

if command -v wget >/dev/null 2>&1; then
    echo "📥 Downloading installer using wget from $INSTALLER_URL"
    wget --no-hsts --tries 3 --output-document "$INSTALLER" "$INSTALLER_URL"
    if [[ -n "$CHECKSUM_URL" ]]; then
        wget --no-hsts --tries 3 --output-document "$INSTALLER_CHECKSUM" "$CHECKSUM_URL"
    fi
elif command -v curl >/dev/null 2>&1; then
    echo "📥 Downloading installer using curl from $INSTALLER_URL"
    curl --fail --location --retry 3 --output "$INSTALLER" "$INSTALLER_URL"
    if [[ -n "$CHECKSUM_URL" ]]; then
        curl --fail --location --retry 3 --output "$INSTALLER_CHECKSUM" "$CHECKSUM_URL"
    fi
else
    echo "⛔ Neither wget nor curl is available." >&2
    exit 1
fi

if [[ -n "$CHECKSUM_URL" ]]; then
    echo "📦 Verifying installer checksum"
    if ! [[ -f "$INSTALLER_CHECKSUM" ]]; then
        echo "⛔ Checksum file not found: $INSTALLER_CHECKSUM" >&2
        exit 1
    fi
    if command -v sha256sum >/dev/null 2>&1; then
        if (cd "$INSTALLER_DIR" && sha256sum --check --status "$INSTALLER_CHECKSUM"); then
            echo "✅ Checksum verification passed"
        else
            echo "❌ Checksum verification failed" >&2
            exit 1
        fi
    elif command -v shasum >/dev/null 2>&1; then
        if (cd "$INSTALLER_DIR" && shasum --algorithm 256 --check --status "$INSTALLER_CHECKSUM"); then
            echo "✅ Checksum verification passed"
        else
            echo "❌ Checksum verification failed" >&2
            exit 1
        fi
    else
        echo "⛔ Neither sha256sum nor shasum is available." >&2
        exit 1
    fi
fi

echo "📦 Installing conda to $CONDA_DIR"
if [[ "$INTERACTIVE" == true ]]; then
    /bin/bash "$INSTALLER" -p "$CONDA_DIR"
else
    /bin/bash "$INSTALLER" -b -p "$CONDA_DIR"
fi

if [[ "$NO_CACHE_CLEAN" == false ]]; then
    "$CONDA_DIR/bin/conda" clean --tarballs --index-cache --packages --yes
    "$CONDA_DIR/bin/conda" clean --force-pkgs-dirs --all --yes
fi

if [[ "$NO_CLEAN" == false ]]; then
    rm "$INSTALLER"
    find "$CONDA_DIR" -follow -type f -name '*.a' -delete
    find "$CONDA_DIR" -follow -type f -name '*.pyc' -delete
fi

if [[ ${#ACTIVATES[@]} -gt 0 ]]; then
    CONDA_SCRIPT="$CONDA_DIR/$CONDA_ACTIVATION_SCRIPT_RELPATH"
    MAMBA_SCRIPT="$CONDA_DIR/$MAMBA_ACTIVATION_SCRIPT_RELPATH"
    for path in "${ACTIVATES[@]}"; do
        echo "▶️ Sourcing activation script to '$path'"
        [[ -f "$path" ]] || touch "$path"
        for line in ". '$CONDA_SCRIPT'" ". '$MAMBA_SCRIPT'" "conda activate base"; do
            if grep -Fxq "$line" "$path"; then
                echo "⏭️ Line already exists in '$path': $line"
            else
                echo "$line" >> "$path"
                echo "ℹ️ Appended to '$path': $line"
            fi
        done
    done
fi

# Add group and fix permissions
# - https://github.com/devcontainers/features/blob/8895eb3d161d28ada3a8de761a83135e811cae3d/src/conda/install.sh#L81-L115
getent group "$GROUP" >/dev/null || groupadd -r "$GROUP"
id -nG "$USER" | grep -qw "$GROUP" || usermod -a -G "$GROUP" "$USER"
chown -R "$USER:$GROUP" "$CONDA_DIR"
chmod -R g+r+w "$CONDA_DIR"
find "$CONDA_DIR" -type d -print0 | xargs -n 1 -0 chmod g+s

echo "✅ Conda installation complete."
