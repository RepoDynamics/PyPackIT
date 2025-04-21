#!/usr/bin/env bash

# Refs:
# - https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
# - https://github.com/devcontainers/features/tree/main/src/git/

set -euxo pipefail

# Default arguments
VERSION="latest"
SOURCE="https://www.kernel.org/pub/software/scm/git/git-"
PREFIX="/usr/local/git"
SYSCONFDIR="/etc"
NO_CLEAN=false
INSTALLER_DIR="/tmp/git-installer"
LOGFILE=""
DEBUG=false

show_help() {
echo "==========="
echo "Install Git"
echo "==========="
echo "Usage: $0 [OPTIONS]"
echo
echo "Install Git from source."
echo
echo "Options:"
echo "    --version <ver>         Version of Git to install."
echo "                            Can be either 'latest', a full version number, or a partial version."
echo "                            Default: '$VERSION'"
echo "    --source <URL>          URL to download the Git source code from."
echo "                            The full URL is built by appending the resolved version to this URL."
echo "                            Example: https://github.com/git/git/archive/v"
echo "                            Default: '$SOURCE'"
echo "    --prefix <path>         Path to install Git to."
echo "                            Default: '$PREFIX'"
echo "    --sysconfdir <path>     Path to the system configuration directory."
echo "                            Default: '$SYSCONFDIR'"
echo "    --no-clean              Skip removing installer artifacts after installation."
echo "    --installer-dir <path>  Path to directory to download the installer to."
echo "                            Default: '$INSTALLER_DIR'"
echo "    --logfile <path>        Log all output (stdout + stderr) to this file in addition to console."
echo "                            Otherwise output is only printed to the console."
echo "    --debug                 Enable debug mode."
echo "    --help                  Show this help message and exit."
echo
echo "Example:"
echo "    $0 --version 2.49.0"
}

# Resolve $VERSION to a full semver version.
resolve_version() {
    local requested_version version_list

    # Only resolve if VERSION is not a full semver (i.e., doesn't contain two dots)
    if [ "$(echo "${VERSION}" | grep -o '\.' | wc -l)" = "2" ]; then
        echo "Version is already a full version: $VERSION"
        return
    fi

    echo "Resolving partial VERSION: ${VERSION}"

    requested_version="${VERSION}"

    # Fetch Git tags from GitHub and extract semver versions
    echo "Fetching Git version tags from GitHub..."
    version_list="$(curl -sSL -H "Accept: application/vnd.github.v3+json" \
        "https://api.github.com/repos/git/git/tags" | \
        grep -oP '"name":\s*"v\K[0-9]+\.[0-9]+\.[0-9]+"' | \
        tr -d '"' | sort -rV )"

    # Handle special cases like "latest", "lts", "current"
    if [ "${requested_version}" = "latest" ]; then
        VERSION="$(echo "${version_list}" | head -n 1)"
        echo "Mapped '${requested_version}' to latest Git version: ${VERSION}"
    else
        # Match the first version that starts with the given prefix
        echo "Attempting to match partial version '${requested_version}'..."
        set +e
        VERSION="$(echo "${version_list}" | grep -E -m 1 "^${requested_version//./\\.}([\\.\\s]|$)")"
        set -e
        echo "Matched to full version: ${VERSION}"
    fi

    # Validate the resolved version exists in the list
    if [ -z "${VERSION}" ] ||
       ! echo "${version_list}" | grep "^${VERSION//./\\.}$" > /dev/null 2>&1; then
        echo "Error: Invalid git version: ${requested_version}" >&2
        exit 1
    fi

    echo "Final resolved Git version: ${VERSION}"
}

OPTS=$(
    getopt \
        --longoptions version:,source:,prefix:,sysconfdir:,no-clean,installer-dir:,logfile:,debug,help \
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
        --version) VERSION="$2"; shift 2;;
        --source) SOURCE="$2"; shift 2;;
        --prefix) PREFIX="$2"; shift 2;;
        --sysconfdir) SYSCONFDIR="$2"; shift 2;;
        --no-clean) NO_CLEAN=true; shift;;
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


mkdir -p "$INSTALLER_DIR"

# - https://github.com/devcontainers/features/blob/8895eb3d161d28ada3a8de761a83135e811cae3d/src/git/install.sh#L299-L312
echo "Downloading source code for Git v${VERSION}..."
curl -sL "${SOURCE}${VERSION}.tar.gz" | tar -xzC "$INSTALLER_DIR" 2>&1
echo "Building Git..."
cd "$INSTALLER_DIR/git-$VERSION"
git_options=("prefix=$PREFIX")
git_options+=("sysconfdir=$SYSCONFDIR")
git_options+=("USE_LIBPCRE=YesPlease")
make -s "${git_options[@]}" all && make -s "${git_options[@]}" install 2>&1

if [[ "$NO_CLEAN" == false ]]; then
    cd /
    rm -rf "$INSTALLER_DIR/git-$VERSION"
fi

echo "✅ Git v${VERSION} installed successfully."
