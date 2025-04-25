#!/usr/bin/env bash

set -euxo pipefail

# Default arguments
INSTALL_DIR="/usr/local/oh-my-zsh"

show_help() {
    echo "================="
    echo "Install Oh My Zsh"
    echo "================="
    echo "Usage: $0 [OPTIONS]"
    echo
    echo "Install Oh My Zsh from source."
    echo
    echo "Options:"
    echo "    --install-dir <path>    Path to directory to install Oh My Zsh to."
    echo "                            Default: '$INSTALL_DIR'"
    echo "    --logfile <path>        Log all output (stdout + stderr) to this file in addition to console."
    echo "                            Otherwise output is only printed to the console."
    echo "    --debug                 Enable debug mode."
    echo "    --help                  Show this help message and exit."
    echo
    echo "Example:"
    echo "    $0 --version 2.49.0"
}

while [ "$#" -gt 0 ]; do
    case "$1" in
        --install-dir) INSTALL_DIR="$2"; shift ;;
        --logfile) LOGFILE="$2"; shift ;;
        --debug) DEBUG=true ;;
        --help) show_help; exit 0 ;;
        *) echo "Unknown option: $1" >&2; show_help >&2; exit 1 ;;
    esac
    shift
done

if [ "$DEBUG" = true ]; then
    set -x
fi

if [[ -n "$LOGFILE" ]]; then
    echo "📝 Initializing logging to '$LOGFILE'."
    mkdir -p "$(dirname "$LOGFILE")"
    exec > >(tee -a "$LOGFILE") 2>&1
fi

echo "📩 Input Arguments:"
echo "   - install-dir: $INSTALL_DIR"
echo "   - logfile: $LOGFILE"
echo "   - debug: $DEBUG"


umask g-w,o-w
mkdir -p "$INSTALL_DIR"
git clone --depth=1 \
    -c core.eol=lf \
    -c core.autocrlf=false \
    -c fsck.zeroPaddedFilemode=ignore \
    -c fetch.fsck.zeroPaddedFilemode=ignore \
    -c receive.fsck.zeroPaddedFilemode=ignore \
    "https://github.com/ohmyzsh/ohmyzsh" \
    "$INSTALL_DIR" 2>&1
cd "$INSTALL_DIR"
git repack -a -d -f --depth=1 --window=1



# Download fonts
# - https://github.com/romkatv/powerlevel10k?tab=readme-ov-file#meslo-nerd-font-patched-for-powerlevel10k
# - https://github.com/romkatv/powerlevel10k/issues/671
# - https://github.com/romkatv/powerlevel10k?tab=readme-ov-file#fonts

# Target directory
FONT_DIR="/usr/share/fonts/MesloLGS"
mkdir -p "$FONT_DIR"

# Base URL
BASE_URL="https://github.com/romkatv/powerlevel10k-media/raw/master"

# Font files to download
FONT_FILES="
MesloLGS%20NF%20Regular.ttf
MesloLGS%20NF%20Bold.ttf
MesloLGS%20NF%20Italic.ttf
MesloLGS%20NF%20Bold%20Italic.ttf
"

echo "Installing MesloLGS Nerd Fonts to $FONT_DIR..."

for FONT in $FONT_FILES; do
  # Decode filename for local file
  LOCAL_NAME=$(printf '%b' "${FONT//%/\\x}")
  echo "Downloading $LOCAL_NAME..."
  curl -fsSL "$BASE_URL/$FONT" -o "$FONT_DIR/$LOCAL_NAME"
done

# Set proper permissions
chmod 644 "$FONT_DIR"/*.ttf

echo "Fonts installed."


# https://github.com/romkatv/powerlevel10k
THEME_INSTALL_DIR="$INSTALL_DIR/custom/themes/powerlevel10k"
mkdir -p "$THEME_INSTALL_DIR"
git clone --depth=1 \
    -c core.eol=lf \
    -c core.autocrlf=false \
    -c fsck.zeroPaddedFilemode=ignore \
    -c fetch.fsck.zeroPaddedFilemode=ignore \
    -c receive.fsck.zeroPaddedFilemode=ignore \
    "https://github.com/romkatv/powerlevel10k" \
    "$THEME_INSTALL_DIR" 2>&1
cd "$THEME_INSTALL_DIR"
git repack -a -d -f --depth=1 --window=1


# https://github.com/zsh-users/zsh-syntax-highlighting/blob/master/INSTALL.md#oh-my-zsh
PLUGIN_INSTALL_DIR="$INSTALL_DIR/custom/plugins/zsh-syntax-highlighting"
git clone --depth=1 \
    -c core.eol=lf \
    -c core.autocrlf=false \
    -c fsck.zeroPaddedFilemode=ignore \
    -c fetch.fsck.zeroPaddedFilemode=ignore \
    -c receive.fsck.zeroPaddedFilemode=ignore \
    "https://github.com/zsh-users/zsh-syntax-highlighting" \
    "$PLUGIN_INSTALL_DIR" 2>&1
cd "$PLUGIN_INSTALL_DIR"
git repack -a -d -f --depth=1 --window=1

