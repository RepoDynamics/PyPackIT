#!/usr/bin/env bash

set -euxo pipefail

# Constants
DEBIAN_EQUIVS_FILENAME="debian-equivs-2023-ex.txt"
DEBIAN_EQUIVS_URL="https://tug.org/texlive/files/$DEBIAN_EQUIVS_FILENAME"

# Default arguments
MIRROR_URI="rsync://rsync.dante.ctan.org/CTAN/systems/texlive/tlnet/"
VERSION="latest"
CONDA_DIR="/opt/conda"
GROUP="conda"
USER="${SUDO_USER:-$(id -un)}"
ACTIVATES=()
NO_CLEAN=false
NO_CACHE_CLEAN=false
INTERACTIVE=false
REINSTALL=false
INSTALLER_DIR="/tmp/texlive-installer"
LOGFILE=""
DEBUG=false

show_help() {
echo "============="
echo "Install Conda"
echo "============="
echo "Usage: $0 [OPTIONS]"
echo
echo "Install conda and mamba using the Miniforge installer."
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

if ! command -v curl >/dev/null 2>&1; then
    echo "⛔ curl is not available." >&2
    exit 1
fi

if command -v tlmgr >/dev/null 2>&1; then
    echo "⚠️ LaTeX installation found."
    if [[ "$REINSTALL" == true ]]; then
        echo "🗑 Uninstalling LaTeX."
        # Refs:
        # - https://www.tug.org/texlive/doc/texlive-en/texlive-en.html#x1-380003.6
        tlmgr uninstall --all
        rm -rf "$(kpsewhich -var-value=TEXMFVAR)"
    else
        echo "⏩ LaTeX is already available; exiting installation."
        exit 0
    fi
fi

mkdir -p "$INSTALLER_DIR"



# Download and install equivs file for dummy package.
# This tells apt that all TeX Live packages are installed.
# - https://gitlab.com/islandoftex/images/texlive/-/blob/72240db12e00510972aeea19cd0a08edc22c4152/Dockerfile#L21-46
curl "$DEBIAN_EQUIVS_URL" --output "DEBIAN_EQUIVS"
read DEBIAN_EQUIVS_PKG DEBIAN_EQUIVS_VERSION < <(
    awk -F': ' '/^Package:/{pkg=$2} /^Version:/{ver=$2} END{print pkg, ver}' "$DEBIAN_EQUIVS"
)
DEBIAN_EQUIVS_DUMMY_VERSION="9999.99999999-1"
sed -i "s/$DEBIAN_EQUIVS_VERSION/$DEBIAN_EQUIVS_VERSION_DUMMY/" "DEBIAN_EQUIVS"
equivs-build "DEBIAN_EQUIVS"
dpkg -i "$DEBIAN_EQUIVS_PKG_$DEBIAN_EQUIVS_DUMMY_VERSION_all.deb"
apt-get install -qyf --no-install-recommends
apt-get dist-clean
rm -rf /var/cache/apt/
rm -rf ./*texlive*



# Install TeX Live from upstream mirror using full scheme with no docs or sources
echo "Fetching installation from mirror $TLMIRRORURL"
rsync -a --stats "$TLMIRRORURL" texlive
cd texlive
# Create installation profile for full scheme installation
echo "selected_scheme scheme-full" > install.profile
echo "tlpdbopt_install_docfiles 0" >> install.profile
echo "tlpdbopt_install_srcfiles 0" >> install.profile
echo "tlpdbopt_autobackup 0" >> install.profile
echo "tlpdbopt_sys_bin /usr/bin" >> install.profile
export TEXLIVE_INSTALL_NO_CONTEXT_CACHE=1
export NOPERLDOC=1
./install-tl -profile install.profile
cd ..
rm -rf texlive



# Finalize TeX Live setup: add to PATH, patch ConTeXt, generate caches
echo "Adding TeX Live binaries to system PATH"
$(find /usr/local/texlive -name tlmgr) path add
# Patch for ConTeXt (issue #30)
echo "Fixing ConTeXt path in mtxrun.lua"
(sed -i '/package.loaded\["data-ini"\]/a if os.selfpath then environment.ownbin=lfs.symlinktarget(os.selfpath..io.fileseparator..os.selfname);environment.ownpath=environment.ownbin:match("^.*"..io.fileseparator) else environment.ownpath=kpse.new("luatex"):var_value("SELFAUTOLOC");environment.ownbin=environment.ownpath..io.fileseparator..(arg[-2] or arg[-1] or arg[0] or "luatex"):match("[^"..io.fileseparator.."]*$") end' /usr/bin/mtxrun.lua || true)
echo "Generating font and ConTeXt caches..."
(luaotfload-tool -u || true)
mkdir -p /etc/fonts/conf.d
(cp "$(find /usr/local/texlive -name texlive-fontconfig.conf)" /etc/fonts/conf.d/09-texlive-fonts.conf || true)
fc-cache -fsv
if [ -f "/usr/bin/context" ]; then
    mtxrun --generate
    texlua /usr/bin/mtxrun.lua --luatex --generate
    context --make
    context --luatex --make
fi

echo "✅ LaTeX installation complete."
