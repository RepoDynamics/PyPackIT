#!/usr/bin/env bash

show_help() {
    cat <<EOF
====================
Install APT Packages
====================
Usage: $0 <package-list-file> [OPTIONS]

Install APT packages listed in a file using 'apt-get install'.

Positional arguments:
    <package-list-file>     Path to a file containing newline-separated
                            package specifications.

Options:
    --logfile <path>        Log all output (stdout + stderr) to this file.
                            If not specified, output is only printed to the console.
    --no-update             Skip 'apt-get update' step before installation.
    --no-clean              Skip 'apt-get dist-clean' step after installation.
    --interactive           Allow apt to prompt the user (default is non-interactive).
    --help                  Show this help message and exit.

Example:
    $0 apt.txt --logfile /tmp/install.log --no-clean
EOF
}

set -euxo pipefail

LOGFILE=""
DO_UPDATE=true
DO_CLEAN=true
NONINTERACTIVE=true

if [[ $# -lt 1 ]]; then
    show_help >&2
    exit 1
fi

if [[ "$1" == "--help" ]]; then
    show_help
    exit 0
fi

PACKAGE_LIST_FILE=$1
shift

while [[ $# -gt 0 ]]; do
    case "$1" in
        --logfile)
            shift
            LOGFILE=$1
            ;;
        --no-update)
            DO_UPDATE=false
            ;;
        --no-clean)
            DO_CLEAN=false
            ;;
        --interactive)
            NONINTERACTIVE=false
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

if [[ ! -f "$PACKAGE_LIST_FILE" ]]; then
    echo "⛔ Package list file '$PACKAGE_LIST_FILE' does not exist." >&2
    exit 1
fi

# Read the package list file and filter out comments and empty lines
mapfile -t PACKAGES < <(grep -Ev '^\s*(#|$)' "$PACKAGE_LIST_FILE")
if [[ ${#PACKAGES[@]} -eq 0 ]]; then
    echo "⛔ No packages found in file '$PACKAGE_LIST_FILE'." >&2
    exit 1
fi

if [[ "$NONINTERACTIVE" == true ]]; then
    echo "🆗 Setting APT to non-interactive mode."
    export DEBIAN_FRONTEND=noninteractive
fi

# add-apt-repository

if "$DO_UPDATE"; then
    echo "🔄 Updating package lists."
    apt-get update -y
fi

echo "📲 Installing packages:"
printf '  - %s\n' "${PACKAGES[@]}"
apt-get install -y --no-install-recommends "${PACKAGES[@]}"

if "$DO_CLEAN"; then
    echo "🧹 Cleaning up."
    # Starting from APT 2.7.8, the `apt-get` command accepts the `dist-clean` option,
    # which removes list files automatically instead of "rm -rf /var/lib/apt/lists/*"
    # - https://tracker.debian.org/news/1492892/accepted-apt-278-source-into-unstable/
    # - https://github.com/docker-library/buildpack-deps/pull/157/files
    apt-get dist-clean
fi

echo "🏁 Finished installing APT packages."
