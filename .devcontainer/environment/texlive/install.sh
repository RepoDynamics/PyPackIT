#!/usr/bin/env bash

set -euo pipefail

# Constants
DEBIAN_EQUIVS_FILENAME="debian-equivs-2023-ex.txt"
DEBIAN_EQUIVS_URL="https://tug.org/texlive/files/$DEBIAN_EQUIVS_FILENAME"
DEFAULT_TEXDIR_PREFIX="/usr/local/texlive"
DEFAULT_SYS_BIN="/usr/local/bin"

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


install_dummy_apt_package() {
    # Download and install dummy TeX Live APT package.
    #
    # This tells apt-get that all TeX Live packages are installed,
    # so that it doesn't try to install them again later.
    #
    # References
    # ----------
    # - https://gitlab.com/islandoftex/images/texlive/-/blob/72240db12e00510972aeea19cd0a08edc22c4152/Dockerfile#L21-46

    local equivs_file="$INSTALLER_DIR/$DEBIAN_EQUIVS_FILENAME"
    local dummy_version="9999.99999999-1"
    if ! command -v curl >/dev/null 2>&1; then
        echo "⛔ curl is not available." >&2
        exit 1
    fi
    echo "📥 Downloading equivs TeX Live APT package data."
    curl "$DEBIAN_EQUIVS_URL" --output "$equivs_file"
    read pkg_name pkg_version < <(
        awk -F': ' '/^Package:/{pkg=$2} /^Version:/{ver=$2} END{print pkg, ver}' "$equivs_file"
    )
    # Substitute the version number with a large dummy version to avoid updates.
    sed -i "s/${pkg_version}/${dummy_version}/" "$equivs_file"
    echo "📦 Installing equivs TeX Live APT package."
    equivs-build "$equivs_file"
    dpkg -i "${pkg_name}_${dummy_version}_all.deb"
    apt-get install -qyf --no-install-recommends
    if [[ "$NO_CACHE_CLEAN" == false ]]; then
        echo "🧹 Cleaning up APT cache."
        apt-get dist-clean
        rm -rf /var/cache/apt/
    fi
}


uninstall_texlive() {
    # Uninstall TeX Live.
    #
    # References
    # ----------
    # - https://www.tug.org/texlive/doc/texlive-en/texlive-en.html#x1-380003.6
    # - https://www.tug.org/mactex/uninstalling.html

    echo "🗑 Uninstall TeX Live."
    tlmgr uninstall --all
    rm -rf "$(kpsewhich -var-value=TEXMFVAR)"
}


download_texlive_installer() {
    # Download the TeX Live installer.
    echo "📥 Download TeX Live installer from '$MIRROR' to '$INSTALLER_DIR'."
    rsync -a --stats "$MIRROR" "$INSTALLER_DIR"
}


install_texlive() {
    # Install TeX Live using the installer.
    #
    # References
    # ----------
    # - https://www.tug.org/texlive/doc/install-tl.html
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
}


set_texdir() {
    # Get the TeX Live installation directory.
    #
    # This is needed for the finalization step.
    # The installation directory may be specified in the profile file under the TEXDIR variable.
    #
    # Outputs
    # -------
    # TEXDIR
    #   The TeX Live installation directory.

    TEXDIR=$(awk '$1=="TEXDIR"{sub(/^[^[:space:]]+[[:space:]]+/, ""); print}' "$PROFILE")
    if [[ -n "$TEXDIR" ]]; then
        echo "🎛 TEXDIR set to '$TEXDIR' from profile file '$PROFILE'."
    else
        # Default is '/usr/local/texlive/YYYY' for release 'YYYY'
        # Get LaTeX version (year, in format YYYY) from a file named LATEX_YYYY in the installer directory
        local version=$(find "$INSTALLER_DIR" -maxdepth 1 -type f -regex '.*/LATEX_[0-9]\{4\}' -exec basename {} \; | head -n1 | grep -oP '^LATEX_\K[0-9]{4}')
        if [[ -z "$version" ]]; then
            echo "⛔ No LATEX_YYYY file found in '$INSTALLER_DIR'." >&2
            exit 1
        fi
        TEXDIR="${DEFAULT_TEXDIR_PREFIX}/${version}"
        echo "🎛 TEXDIR set to default value '$TEXDIR'."
    fi
}


set_sysbin() {
    # Set the 'sys_bin' directory for TeX Live.
    #
    # Outputs
    # -------
    # SYS_BIN
    #   TeX Live 'sys_bin' directory.

    SYS_BIN=$(awk '$1=="tlpdbopt_sys_bin"{sub(/^[^[:space:]]+[[:space:]]+/, ""); print}' "$PROFILE")
    if [[ -z "$SYS_BIN" ]]; then
        echo "🎛 Set tlpdbopt_sys_bin to '$SYS_BIN' from profile file '$PROFILE'."
    else
        SYS_BIN="$DEFAULT_SYS_BIN"
        echo "🎛 Set tlpdbopt_sys_bin to default value '$SYS_BIN'."
    fi
}


add_texlive_bin_to_path() {
    # Add TeX Live bin directory to the PATH environment variable.

    local tlmgr="$(find "$TEXDIR" -name tlmgr)"
    if [[ -n "$tlmgr" ]]; then
        echo "📦 Located tlmgr at '$tlmgr'."
    else
        echo "⛔ tlmgr not found in TEXDIR '$TEXDIR'." >&2
        exit 1
    fi
    echo "🛤 Add TeX Live binaries to system PATH."
    "$tlmgr" path add
}


apply_patches() {
    # Apply patches to the TeX Live installation.

    # Patch for ConTeXt (https://gitlab.com/islandoftex/images/texlive/-/issues/30)
    echo "Fixing ConTeXt path in mtxrun.lua"
    (sed \
        -i \
        '/package.loaded\["data-ini"\]/a if os.selfpath then environment.ownbin=lfs.symlinktarget(os.selfpath..io.fileseparator..os.selfname);environment.ownpath=environment.ownbin:match("^.*"..io.fileseparator) else environment.ownpath=kpse.new("luatex"):var_value("SELFAUTOLOC");environment.ownbin=environment.ownpath..io.fileseparator..(arg[-2] or arg[-1] or arg[0] or "luatex"):match("[^"..io.fileseparator.."]*$") end' \
        "$SYS_BIN/mtxrun.lua" || true
    )
}


generate_caches() {
    # Generate ConTeXt and font caches.

    echo "💾 Generate ConTeXt and font caches."
    (luaotfload-tool -u || true)
    mkdir -p /etc/fonts/conf.d
    (cp "$(find "$TEXDIR" -name texlive-fontconfig.conf)" /etc/fonts/conf.d/09-texlive-fonts.conf || true)
    fc-cache -fsv
    if [ -f "$SYS_BIN/context" ]; then
        mtxrun --generate
        texlua "$SYS_BIN/mtxrun.lua" --luatex --generate
        context --make
        context --luatex --make
    fi
}


verify_installation() {
    # Verify TeX Live installation.

    echo "☑️ Verify TeX Live installation."
    latex --version && printf '\n'
    biber --version && printf '\n'
    xindy --version && printf '\n'
    arara --version && printf '\n'
    context --version && printf '\n'
    context --luatex --version && printf '\n'
    asy --version && printf '\n'
    python --version && printf '\n'
    pygmentize -V && printf '\n'
}


while [[ $# -gt 0 ]]; do
    case "$1" in
        --profile) PROFILE="$2"; shift;;
        --mirror) MIRROR="$2"; shift;;
        --no-clean) NO_CLEAN=true;;
        --no-cache-clean) NO_CACHE_CLEAN=true;;
        --interactive) INTERACTIVE=true;;
        --reinstall) REINSTALL=true;;
        --installer-dir) INSTALLER_DIR="$2"; shift;;
        --logfile) LOGFILE="$2"; shift;;
        --debug) DEBUG=true;;
        --help) show_help; exit 0;;
        --) shift; break;;
        *) echo "Unknown option: $1" >&2; show_help >&2; exit 1;;
    esac
    shift
done

echo "📩 Input Arguments:"
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

if command -v tlmgr >/dev/null 2>&1; then
    echo "⚠️ LaTeX installation found."
    if [[ "$REINSTALL" == true ]]; then
        uninstall_texlive
    else
        echo "⏩ LaTeX is already available; exiting installation."
        exit 0
    fi
fi

mkdir -p "$INSTALLER_DIR"
if command -v apt-get >/dev/null 2>&1; then
    install_dummy_apt_package
fi
download_texlive_installer
install_texlive
set_texdir
if [[ "$NO_CLEAN" == false ]]; then
    echo "🗑 Removing installer artifacts."
    rm -rf "$INSTALLER_DIR"
fi
set_sysbin
add_texlive_bin_to_path
apply_patches
generate_caches
verify_installation
echo "✅ LaTeX installation complete."
