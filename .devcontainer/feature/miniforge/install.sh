#!/usr/bin/env bash

set -euo pipefail

# Constants
CONDA_ACTIVATION_SCRIPT_RELPATH="etc/profile.d/conda.sh"
MAMBA_ACTIVATION_SCRIPT_RELPATH="etc/profile.d/mamba.sh"

# Default arguments
DOWNLOAD=false
INSTALL=false
REINSTALL=false
ACTIVATES=()
ENV_FILES=()
ENV_DIRS=()
SET_PERMISSION=false

MINIFORGE_NAME="Miniforge3"
MINIFORGE_VERSION="latest"
CONDA_DIR="/opt/conda"
GROUP="conda"
USER="${SUDO_USER:-$(id -un)}"
NO_CLEAN=false
NO_CACHE_CLEAN=false
UPDATE_BASE=false
ACTIVE_ENV="base"
INTERACTIVE=false
INSTALLER_DIR="/tmp/miniforge-installer"
LOGFILE=""
DEBUG=false


show_help() {
    echo "============="
    echo "Install Conda"
    echo "============="
    echo "Usage: $0 [OPTIONS]"
    echo
    echo "Install and setup conda and mamba on Linux or macOS."
    echo
    echo "Task Options (specify at least one):"
    echo "    --download                 Download the Miniforge installer to '--installer-dir'."
    echo "    --install                  Install conda and mamba using the Miniforge installer at '--installer-dir'."
    echo "                               Raises an error if conda is already installed."
    echo "    --reinstall                Same as '--install', but uninstall first if conda is already installed."
    echo "    --activate <filepath>      Path to a shell configuration file to append conda initialization to."
    echo "                               Can be provided multiple times."
    echo "                               Examples:"
    echo "                                   /etc/skel/.bashrc"
    echo "                                   /etc/bash.bashrc"
    echo "                                   /etc/zsh/zshrc"
    echo "                                   ~/.bashrc"
    echo "                                   ~/.zshrc"
    echo "    --update-base              Update the base conda environment."
    echo "    --envfile <filepath>       Path to a conda environment YAML file to install."
    echo "                               Can be provided multiple times."
    echo "                               Example: /path/to/env.yaml"
    echo "    --envdir <dirpath>         Path to a directory containing conda environment YAML files to install."
    echo "                               All .yaml and .yml files in this directory and its subdirectories will be installed."
    echo "                               Can be provided multiple times."
    echo "                               Example: /path/to/envs/"
    echo "    --set-permission           Set permissions for the conda directory."
    echo "                               This is done by adding the '--user' to the conda '--group'"
    echo "                               and setting the group ownership of the conda directory."
    echo
    echo "Installation Options (only required for --install and --reinstall):"
    echo "    --miniforge-name <name>    Name of the Miniforge variant to install."
    echo "                               Default: '$MINIFORGE_NAME'"
    echo "    --miniforge-version <ver>  Version of the Miniforge variant to install."
    echo "                               Either 'latest' or a full version string like '24.11.3-2'."
    echo "                               Default: '$MINIFORGE_VERSION'"
    echo "    --conda-dir <dirpath>      Directory to install conda into."
    echo "                               This corresponds to the CONDA_DIR environment variable."
    echo "                               Default: '$CONDA_DIR'"
    echo "    --installer-dir <dirpath>  Path to directory to download the Miniforge installer to."
    echo "                               Default: '$INSTALLER_DIR'"
    echo "    --no-clean                 Skip removing installer artifacts after installation."
    echo "    --interactive              Allow the installer to prompt the user."
    echo "    --group <name>             Name of a user group to give access to conda."
    echo "                               Default: '$GROUP'"
    echo "    --user <name>              Name of a user to add to the conda group."
    echo "                               This user must already exist."
    echo "                               Defaults to the real user running this script."
    echo "                               Default: '$USER'"
    echo "    --active-env <name>        Name of a conda environment to activate in '--activate' files."
    echo "    --no-cache-clean           Skip 'conda clean' commands after installation."
    echo "    --logfile <filepath>       Log all output (stdout + stderr) to this file in addition to console."
    echo "                               Otherwise output is only printed to the console."
    echo "    --debug                    Enable debug mode."
    echo "    --help                     Show this help message and exit."
    echo
    echo "Example:"
    echo "    $0 --download --install --miniforge-version 24.11.3-2 --no-clean"
    echo
    echo "References:"
    echo "    - Miniforge Docker image: https://github.com/conda-forge/miniforge-images/blob/master/ubuntu/Dockerfile"
    echo "    - Miniforge repository README: https://github.com/conda-forge/miniforge?tab=readme-ov-file#install"
    echo "    - Devcontainers conda feature: https://github.com/devcontainers/features/tree/main/src/conda"
}


set_installer_filename() {
    # Set the following global variables:
    # - INSTALLER_FILENAME
    #       Filename of the installer script.
    # - INSTALLER
    #       Full path to the installer file.
    # - CHECKSUM
    #       Full path to the corresponding checksum file.
    local installer_platform="$(uname)-$(uname -m)"
    if [[ "$MINIFORGE_VERSION" == "latest" ]]; then
        INSTALLER_FILENAME="${MINIFORGE_NAME}-${installer_platform}.sh"
    else
        INSTALLER_FILENAME="${MINIFORGE_NAME}-${MINIFORGE_VERSION}-${installer_platform}.sh"
    fi
    INSTALLER="${INSTALLER_DIR}/${INSTALLER_FILENAME}"
    CHECKSUM="${INSTALLER}.sha256"
}


set_executable_path() {
    # Set the executable path for conda and mamba.
    #
    # Parameters
    # ----------
    # verify : {"verify"}, optional
    #     Verify the existence of the executables.
    #     This is useful before running the post-installation steps.
    # Outputs
    # -------
    # CONDA_EXEC
    #     Path to the conda executable.
    # MAMBA_EXEC
    #     Path to the mamba executable.
    CONDA_EXEC="${CONDA_DIR}/bin/conda"
    MAMBA_EXEC="${CONDA_DIR}/bin/mamba"
    if [ "${1:-}" != "verify" ]; then
        return
    fi
    if [[ ! -f "$CONDA_EXEC" ]]; then
        if command -v conda >/dev/null 2>&1; then
            CONDA_DIR="$(conda info --base)"
            CONDA_EXEC="${CONDA_DIR}/bin/conda"
        else
            echo "⛔ Conda executable not found at '$CONDA_EXEC'." >&2
            exit 1
        fi
    fi
    if [[ ! -f "$MAMBA_EXEC" ]]; then
        if command -v mamba >/dev/null 2>&1; then
            MAMBA_EXEC="$(mamba info --base | tail -n 2 | head -n 1)/bin/mamba"
        else
            echo "⛔ Mamba executable not found at '$MAMBA_EXEC'." >&2
            exit 1
        fi
    fi
    if [[ ! -f "$CONDA_EXEC" ]]; then
        echo "⛔ Conda executable not found." >&2
        exit 1
    fi
    if [[ ! -f "$MAMBA_EXEC" ]]; then
        echo "⛔ Mamba executable not found." >&2
        exit 1
    fi
    echo "🎛 Conda executable located at '$CONDA_EXEC'."
    echo "🎛 Mamba executable located at '$MAMBA_EXEC'."
}


download_miniforge() {
    # Download and verify the Miniforge installer.
    local installer_url
    local checksum_url
    if [[ "$MINIFORGE_VERSION" == "latest" ]]; then
        installer_url="https://github.com/conda-forge/miniforge/releases/latest/download/${INSTALLER_FILENAME}"
        checksum_url=""  # TODO: Find a way to get the checksum URL for the latest version.
    else
        installer_url="https://github.com/conda-forge/miniforge/releases/download/${MINIFORGE_VERSION}/${INSTALLER_FILENAME}"
        checksum_url="$installer_url.sha256"
    fi
    mkdir -p "$INSTALLER_DIR"
    if command -v wget >/dev/null 2>&1; then
        echo "📥 Downloading installer using wget from $installer_url" >&2
        wget --no-hsts --tries 3 --output-document "$INSTALLER" "$installer_url"
        if [[ -n "$checksum_url" ]]; then
            wget --no-hsts --tries 3 --output-document "$CHECKSUM" "$checksum_url"
        fi
    elif command -v curl >/dev/null 2>&1; then
        echo "📥 Downloading installer using curl from $installer_url" >&2
        curl --fail --location --retry 3 --output "$INSTALLER" "$installer_url"
        if [[ -n "$checksum_url" ]]; then
            curl --fail --location --retry 3 --output "$CHECKSUM" "$checksum_url"
        fi
    else
        echo "⛔ Neither wget nor curl is available." >&2
        exit 1
    fi
    if [[ -n "$checksum_url" ]]; then
        verify_miniforge
    fi
}


verify_miniforge() {
    # Verify the installer using the checksum file if downloaded.
    echo "📦 Verifying installer checksum"
    if command -v sha256sum >/dev/null 2>&1; then
        if (cd "$INSTALLER_DIR" && sha256sum --check --status "$CHECKSUM"); then
            echo "✅ Checksum verification passed" >&2
        else
            echo "❌ Checksum verification failed" >&2
            exit 1
        fi
    elif command -v shasum >/dev/null 2>&1; then
        if (cd "$INSTALLER_DIR" && shasum --algorithm 256 --check --status "$CHECKSUM"); then
            echo "✅ Checksum verification passed" >&2
        else
            echo "❌ Checksum verification failed" >&2
            exit 1
        fi
    else
        echo "⛔ Neither sha256sum nor shasum is available." >&2
        exit 1
    fi
}


uninstall_miniforge() {
    # Uninstall Miniforge from the system.
    #
    # References
    # ----------
    # - https://github.com/conda-forge/miniforge?tab=readme-ov-file#uninstall
    # - https://www.anaconda.com/docs/getting-started/miniconda/uninstall#manual-uninstall
    echo "🗑 Uninstalling conda (Miniforge)."
    "$CONDA_EXEC" init --reverse
    rm -rf "$("$CONDA_EXEC" info --base)"
    rm -f "$HOME/.condarc"
    rm -rf "$HOME/.conda"
    user_home=$(getent passwd "$USER" | cut -d: -f6)
    rm -rf "$user_home/.condarc"
    rm -rf "$user_home/.conda"
}


install_miniforge() {
    echo "📦 Installing conda to $CONDA_DIR"
    if [[ "$INTERACTIVE" == true ]]; then
        /bin/bash "$INSTALLER" -p "$CONDA_DIR"
    else
        /bin/bash "$INSTALLER" -b -p "$CONDA_DIR"
    fi

    # Post-installation validation.
    echo "Displaying conda info:"
    "$CONDA_EXEC" info
    echo "Displaying conda config:"
    "$CONDA_EXEC" config --show
    echo "Displaying conda env list:"
    "$CONDA_EXEC" env list
    echo "Displaying conda list:"
    "$CONDA_EXEC" list --name base

    clean_post_install
}


clean_post_install() {
    # Clean up after installation.
    if [[ "$NO_CLEAN" == false ]]; then
        [ -f "$INSTALLER" ] && { echo "🗑 Removing installer script at '$INSTALLER'" >&2; rm -f "$INSTALLER"; }
        [ -f "$CHECKSUM" ] && { echo "🗑 Removing checksum file at '$CHECKSUM'" >&2; rm -f "$CHECKSUM"; }
        [ -d "$INSTALLER_DIR" ] && [ -z "$(ls -A "$INSTALLER_DIR")" ] && {
            echo "🗑 Removing installation directory at '$INSTALLER_DIR'" >&2
            rmdir "$INSTALLER_DIR"
        }
    fi
    find "$CONDA_DIR" -follow -type f -name '*.a' -delete
    find "$CONDA_DIR" -follow -type f -name '*.pyc' -delete
    if [[ "$NO_CACHE_CLEAN" == false ]] && [[ -f "$CONDA_EXEC" ]]; then
        echo "🧹 Cleaning up conda cache."
        "$CONDA_EXEC" clean --all --force-pkgs-dirs --yes
    fi
}


add_activation_to_rcfile() {
    # Add conda activation to the specified shell configuration file.
    local conda_script="$CONDA_DIR/$CONDA_ACTIVATION_SCRIPT_RELPATH"
    local mamba_script="$CONDA_DIR/$MAMBA_ACTIVATION_SCRIPT_RELPATH"
    lines=(
        ". '$conda_script'"
        ". '$mamba_script'"
    )
    if [[ -n "$ACTIVE_ENV" ]]; then
        lines+=("conda activate $ACTIVE_ENV")
    fi

    for path in "${ACTIVATES[@]}"; do
        echo "▶️ Sourcing activation script to '$path'"
        [[ -f "$path" ]] || touch "$path"
        for line in "${lines[@]}"; do
            if grep -Fxq "$line" "$path"; then
                echo "⏭️ Line already exists in '$path': $line"
            else
                echo "$line" >> "$path"
                echo "ℹ️ Appended to '$path': $line"
            fi
        done
    done
}


setup_environments() {
    # Setup conda environments from the specified YAML files.
    umask 0002
    for env_file in "${ENV_FILES[@]}"; do
        echo "📦 Installing conda environment from '$env_file'."
        "$MAMBA_EXEC" env update --file "$env_file"
    done

    for env_dir in "${ENV_DIRS[@]}"; do
        find "$env_dir" -type f \( -name "*.yml" -o -name "*.yaml" \) | while IFS= read -r env_file; do
            echo "📦 Installing conda environment from '$env_file'."
            "$MAMBA_EXEC" env update --file "$env_file"
        done
    done

    if [[ "$NO_CACHE_CLEAN" == false ]]; then
        echo "🧹 Cleaning up conda cache."
        "$MAMBA_EXEC" clean --all -y
    fi
}


set_permission() {
    # Add user group and fix permissions.
    #
    # References
    # ----------
    # - https://github.com/devcontainers/features/blob/8895eb3d161d28ada3a8de761a83135e811cae3d/src/conda/install.sh#L81-L115
    echo "🔐 Setting permissions for conda directory."
    getent group "$GROUP" >/dev/null || groupadd -r "$GROUP"
    id -nG "$USER" | grep -qw "$GROUP" || usermod -a -G "$GROUP" "$USER"
    chown -R "$USER:$GROUP" "$CONDA_DIR"
    chmod -R g+r+w "$CONDA_DIR"
    find "$CONDA_DIR" -type d -print0 | xargs -n 1 -0 chmod g+s
}


while [ "$#" -gt 0 ]; do
    case "$1" in
        --download) DOWNLOAD=true;;
        --install) INSTALL=true;;
        --reinstall) REINSTALL=true;;
        --activate) ACTIVATES+=("$2"); shift;;
        --envfile) ENV_FILES+=("$2"); shift;;
        --envdir) ENV_DIRS+=("$2"); shift;;
        --set-permission) SET_PERMISSION=true;;
        --miniforge-name) MINIFORGE_NAME="$2"; shift;;
        --miniforge-version) MINIFORGE_VERSION="$2"; shift;;
        --conda-dir) CONDA_DIR="$2"; shift;;
        --group) GROUP="$2"; shift;;
        --user) USER="$2"; shift;;
        --update-base) UPDATE_BASE=true;;
        --no-clean) NO_CLEAN=true;;
        --active-env) ACTIVE_ENV="$2"; shift;;
        --no-cache-clean) NO_CACHE_CLEAN=true;;
        --interactive) INTERACTIVE=true;;
        --installer-dir) INSTALLER_DIR="$2"; shift;;
        --logfile) LOGFILE="$2"; shift;;
        --debug) DEBUG=true;;
        --help) show_help; exit 0;;
        --) break;;
        *) echo "Unknown option: $1" >&2; show_help >&2; exit 1;;
    esac
    shift
done

if [[ "$DEBUG" == true ]]; then
    set -x
fi

if [[ -n "$LOGFILE" ]]; then
    echo "📝 Initializing logging to '$LOGFILE'."
    mkdir -p "$(dirname "$LOGFILE")"
    exec > >(tee -a "$LOGFILE") 2>&1
fi

echo "📩 Input Arguments:"
echo "   - install: $INSTALL"
echo "   - reinstall: $REINSTALL"
echo "   - activate: ${ACTIVATES[*]}"
echo "   - envfile: ${ENV_FILES[*]}"
echo "   - envdir: ${ENV_DIRS[*]}"
echo "   - set-permission: $SET_PERMISSION"
echo "   - miniforge-name: $MINIFORGE_NAME"
echo "   - miniforge-version: $MINIFORGE_VERSION"
echo "   - conda-dir: $CONDA_DIR"
echo "   - group: $GROUP"
echo "   - user: $USER"
echo "   - no-clean: $NO_CLEAN"
echo "   - no-cache-clean: $NO_CACHE_CLEAN"
echo "   - interactive: $INTERACTIVE"
echo "   - installer-dir: $INSTALLER_DIR"
echo "   - logfile: $LOGFILE"
echo "   - debug: $DEBUG"


# Check installation requirements and user inputs.
if [ "$(id -u)" -ne 0 ]; then
    echo -e '⛔ This script must be run as root. Use sudo, su, or add "USER root" to your Dockerfile before running this script.' >&2
    exit 1
fi

for env_file in "${ENV_FILES[@]}"; do
    if [[ ! -f "$env_file" ]]; then
        echo "⛔ Environment file '$env_file' not found." >&2
        exit 1
    fi
done

for env_dir in "${ENV_DIRS[@]}"; do
    if [[ ! -d "$env_dir" ]]; then
        echo "⛔ Environment directory '$env_dir' not found." >&2
        exit 1
    fi
done

set_executable_path

# Workflow
if [[ "$DOWNLOAD" == true || "$INSTALL" == true || "$REINSTALL" == true ]]; then
    set_installer_filename
fi

trap 'echo "💥 Script failed"; clean_post_install' ERR

if [[ "$DOWNLOAD" == true ]]; then
    download_miniforge
fi

if [[ "$DOWNLOAD" == true || "$INSTALL" == true || "$REINSTALL" == true ]]; then
    if [[ -f "$CHECKSUM" ]]; then
        verify_miniforge
    else
        echo "⚠️ Checksum file not found. Skipping verification." >&2
    fi
fi

if [[ "$INSTALL" == true || "$REINSTALL" == true ]]; then
    if command -v conda >/dev/null 2>&1; then
        echo "⚠️ Conda installation found."
        if [[ "$REINSTALL" != true ]]; then
            echo "⏩ Conda is already available."
        else
            uninstall_miniforge
            install_miniforge
        fi
    else
        install_miniforge
    fi
fi

# If installation was not performed in this run,
# update the CONDA_EXEC variable to point to the correct location.
set_executable_path "verify"

if [[ ${#ACTIVATES[@]} -gt 0 ]]; then
    add_activation_to_rcfile
fi

if [[ "$UPDATE_BASE" == true ]]; then
    echo "⚠️ Updating base conda environment."
    "$MAMBA_EXEC" update -n base --all -y
fi

if [[ ${#ENV_FILES[@]} -gt 0 || ${#ENV_DIRS[@]} -gt 0 ]]; then
    setup_environments
fi

if [[ "$SET_PERMISSION" == true ]]; then
    set_permission
fi

echo "✅ Conda installation complete."
