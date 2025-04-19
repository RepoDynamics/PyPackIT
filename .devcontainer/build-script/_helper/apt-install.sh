#!/usr/bin/env bash

set -euxo pipefail

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
                          If not specified, output is not logged.
  --no-update             Skip 'apt-get update' step before installation.
  --no-clean              Skip 'apt-get dist-clean' step after installation.
  --interactive           Allow apt to prompt the user (default is non-interactive).
  --help                  Show this help message and exit.

Example:
  $0 apt.txt --logfile /tmp/install.log --no-clean
EOF
}

# ------------------------------
# Parse arguments
# ------------------------------

LOGFILE=""
DO_UPDATE=true
DO_CLEAN=true
NONINTERACTIVE=true

# Check for at least one argument
if [[ $# -lt 1 ]]; then
  show_help >&2
  exit 1
fi

# Check for help option
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

# Logging setup
if [[ -n "$LOGFILE" ]]; then
  echo "Initializing log..."
  mkdir -p "$(dirname "$LOGFILE")"
  exec > >(tee -a "$LOGFILE") 2>&1
fi

# ------------------------------
# Install packages
# ------------------------------

if [[ ! -f "$PACKAGE_LIST_FILE" ]]; then
  echo "Error: Package list file '$PACKAGE_LIST_FILE' does not exist." >&2
  exit 1
fi

mapfile -t PACKAGES < "$PACKAGE_LIST_FILE"

if [[ ${#PACKAGES[@]} -eq 0 ]]; then
  echo "Error: No packages found in file '$PACKAGE_LIST_FILE'." >&2
  exit 1
fi

echo "Installing packages: ${PACKAGES[*]}"

APT_ENV=()
if [[ "$NONINTERACTIVE" == true ]]; then
  APT_ENV=(DEBIAN_FRONTEND=noninteractive)
fi

if "$DO_UPDATE"; then
  echo "Updating package lists..."
  sudo "${APT_ENV[@]}" apt-get update -y
fi

sudo "${APT_ENV[@]}" apt-get install -y --no-install-recommends "${PACKAGES[@]}"

if "$DO_CLEAN"; then
  echo "Cleaning up..."
  sudo "${APT_ENV[@]}" apt-get clean
fi

echo "Done."
