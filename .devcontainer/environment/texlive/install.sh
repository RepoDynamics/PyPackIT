#!/usr/bin/env bash

set -euo pipefail

# Constants
DEBIAN_EQUIVS_FILENAME="debian-equivs-2023-ex.txt"
DEBIAN_EQUIVS_URL="https://tug.org/texlive/files/$DEBIAN_EQUIVS_FILENAME"

# Default arguments
PROFILE=""
MIRROR="rsync://rsync.dante.ctan.org/CTAN/systems/texlive/tlnet/"
NO_CLEAN=false
NO_CACHE_CLEAN=false
INTERACTIVE=false
REINSTALL=false
INSTALLER_DIR="/tmp/texlive-installer"
LOGFILE=""
DEBUG=false

show_help() {
echo "==============="
echo "Install TexLive"
echo "==============="
echo "Usage: $0 [OPTIONS]"
echo
echo "Install TexLive using the TeXlive installer."
echo
echo "Options:"
echo "    --profile <path>        Path to an installation profile file."
echo "                            If not provided, an interactive installation will be performed."
echo "    --mirror <URI>          URI of the TeX Live mirror to use for installation."
echo "                            Default: '$MIRROR'"
echo "    --no-clean              Skip removing installer artifacts after installation."
echo "    --no-cache-clean        Skip 'apt-get dist-clean' command after installation of dummy package."
echo "    --interactive           Start an interactive installation even when profile is provided."
echo "    --reinstall             If TeX is already installed, uninstall it and continue with the installation."
echo "    --installer-dir <path>  Path to directory to download the installer to."
echo "                            Default: '$INSTALLER_DIR'"
echo "    --logfile <path>        Log all output (stdout + stderr) to this file in addition to console."
echo "                            Otherwise output is only printed to the console."
echo "    --debug                 Enable debug mode."
echo "    --help                  Show this help message and exit."
echo
echo "Example:"
echo "    $0 --profile /path/to/texlive/install.profile"
}


while [[ $# -gt 0 ]]; do
    case "$1" in
        --profile) PROFILE="$2"; shift 2 ;;
        --mirror) MIRROR="$2"; shift 2 ;;
        --no-clean) NO_CLEAN=true; shift ;;
        --no-cache-clean) NO_CACHE_CLEAN=true; shift ;;
        --interactive) INTERACTIVE=true; shift ;;
        --reinstall) REINSTALL=true; shift ;;
        --installer-dir) INSTALLER_DIR="$2"; shift 2 ;;
        --logfile) LOGFILE="$2"; shift 2 ;;
        --debug) DEBUG=true; shift ;;
        --help) show_help; exit 0 ;;
        --) shift; break ;;
        *) echo "Unknown option: $1" >&2; show_help >&2; exit 1 ;;
    esac
done

echo "📥 Input Arguments:"
echo "   - profile: $PROFILE"
echo "   - mirror: $MIRROR"
echo "   - no-clean: $NO_CLEAN"
echo "   - no-cache-clean: $NO_CACHE_CLEAN"
echo "   - interactive: $INTERACTIVE"
echo "   - reinstall: $REINSTALL"
echo "   - installer-dir: $INSTALLER_DIR"
echo "   - logfile: $LOGFILE"
echo "   - debug: $DEBUG"

if [[ "$DEBUG" == true ]]; then
    set -x
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


if command -v apt-get >/dev/null 2>&1; then
    # Download and install equivs file for dummy package.
    # This tells apt that all TeX Live packages are installed.
    # - https://gitlab.com/islandoftex/images/texlive/-/blob/72240db12e00510972aeea19cd0a08edc22c4152/Dockerfile#L21-46
    DEBIAN_EQUIVS="$INSTALLER_DIR/$DEBIAN_EQUIVS_FILENAME"
    curl "$DEBIAN_EQUIVS_URL" --output "$DEBIAN_EQUIVS"
    read DEBIAN_EQUIVS_PKG DEBIAN_EQUIVS_VERSION < <(
        awk -F': ' '/^Package:/{pkg=$2} /^Version:/{ver=$2} END{print pkg, ver}' "$DEBIAN_EQUIVS"
    )
    # Substitute the version number with a large dummy version to avoid update
    DEBIAN_EQUIVS_DUMMY_VERSION="9999.99999999-1"
    sed -i "s/$DEBIAN_EQUIVS_VERSION/$DEBIAN_EQUIVS_DUMMY_VERSION/" "$DEBIAN_EQUIVS"
    equivs-build "$DEBIAN_EQUIVS"
    dpkg -i "${DEBIAN_EQUIVS_PKG}_${DEBIAN_EQUIVS_DUMMY_VERSION}_all.deb"
    apt-get install -qyf --no-install-recommends
    if [[ "$NO_CACHE_CLEAN" == false ]]; then
        apt-get dist-clean
        rm -rf /var/cache/apt/
    fi
fi


echo "Fetching installation from mirror $MIRROR"
rsync -a --stats "$MIRROR" "$INSTALLER_DIR"


export TEXLIVE_INSTALL_NO_CONTEXT_CACHE=1
export NOPERLDOC=1
if [[ -z "$PROFILE" ]]; then
    echo "📦 Installing TeXLive in interactive mode without a profile."
    "$INSTALLER_DIR/install-tl"
elif [[ "$INTERACTIVE" == "true" ]]; then
    echo "📦 Installing TeXLive in interactive mode with initial profile '$PROFILE'."
    "$INSTALLER_DIR/install-tl" -init-from-profile "$PROFILE"
else
    echo "📦 Installing TeXLive in non-interactive mode with profile '$PROFILE'."
    "$INSTALLER_DIR/install-tl" -profile "$PROFILE"
fi


if [[ "$NO_CLEAN" == false ]]; then
    rm -rf "$INSTALLER_DIR"
fi


SYS_BIN=$(grep -E '^\s*tlpdbopt_sys_bin' "$PROFILE" | sed -E 's/^\s*tlpdbopt_sys_bin\s*//; s/\s*$//')
if [[ -z "$SYS_BIN" ]]; then
  SYS_BIN="/usr/local/bin"
  echo "tlpdbopt_sys_bin not found in $PROFILE. Using default: $SYS_BIN"
else
  echo "Found tlpdbopt_sys_bin in $PROFILE: $SYS_BIN"
fi


# Finalize TeX Live setup: add to PATH, patch ConTeXt, generate caches
echo "Adding TeX Live binaries to system PATH"
$(find "$SYS_BIN/texlive" -name tlmgr) path add
# Patch for ConTeXt (issue #30)
echo "Fixing ConTeXt path in mtxrun.lua"
(sed \
    -i \
    '/package.loaded\["data-ini"\]/a if os.selfpath then environment.ownbin=lfs.symlinktarget(os.selfpath..io.fileseparator..os.selfname);environment.ownpath=environment.ownbin:match("^.*"..io.fileseparator) else environment.ownpath=kpse.new("luatex"):var_value("SELFAUTOLOC");environment.ownbin=environment.ownpath..io.fileseparator..(arg[-2] or arg[-1] or arg[0] or "luatex"):match("[^"..io.fileseparator.."]*$") end' \
    "$SYS_BIN/mtxrun.lua" || true
)
echo "Generating font and ConTeXt caches..."
(luaotfload-tool -u || true)
mkdir -p /etc/fonts/conf.d
(cp "$(find "$SYS_BIN/texlive" -name texlive-fontconfig.conf)" /etc/fonts/conf.d/09-texlive-fonts.conf || true)
fc-cache -fsv
if [ -f "$SYS_BIN/context" ]; then
    mtxrun --generate
    texlua "$SYS_BIN/mtxrun.lua" --luatex --generate
    context --make
    context --luatex --make
fi


latex --version && printf '\n'
biber --version && printf '\n'
xindy --version && printf '\n'
arara --version && printf '\n'
context --version && printf '\n'
context --luatex --version && printf '\n'
asy --version && printf '\n'
python --version && printf '\n'
pygmentize -V && printf '\n'


echo "✅ LaTeX installation complete."
