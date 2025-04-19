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
    --repofile <path>       Path to file containing newline-separated arguments
                            to pass to 'add-apt-repository', one set per line.
    --keep-repos            Keep repositories added via --repofile after script ends.
                            By default, they are removed automatically.
    --no-update             Skip 'apt-get update' step before installation.
    --no-clean              Skip 'apt-get dist-clean' step after installation.
    --interactive           Allow apt to prompt the user (default is non-interactive).
    --help                  Show this help message and exit.

Example:
    $0 apt.txt --logfile /tmp/install.log --repofile repos.txt --no-clean
EOF
}

set -euxo pipefail

LOGFILE=""
REPOFILE=""
KEEP_REPOS=false
DO_UPDATE=true
DO_CLEAN=true
NONINTERACTIVE=true
ADDED_REPOS=()

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
        --repofile)
            shift
            REPOFILE=$1
            ;;
        --keep-repos)
            KEEP_REPOS=true
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

if [[ -n "$REPOFILE" ]]; then
    if [[ ! -f "$REPOFILE" ]]; then
        echo "⛔ Repo file '$REPOFILE' does not exist." >&2
        exit 1
    fi
    echo "🗃 Adding APT repositories from '$REPOFILE'."
    while IFS= read -r line; do
        [[ -z "${line:-}" || "${line}" =~ ^[[:space:]]*# ]] && continue
        echo "📦 Adding repository: $line"
        eval "add-apt-repository --yes $line"
        ADDED_REPOS+=("$line")
    done < "$REPOFILE"
fi

if "$DO_UPDATE"; then
    echo "🔄 Updating package lists."
    apt-get update -y
fi

echo "📲 Installing packages:"
printf '  - %s\n' "${PACKAGES[@]}"
apt-get install -y --no-install-recommends "${PACKAGES[@]}"

if [[ -n "$REPOFILE" && "$KEEP_REPOS" == false ]]; then
    echo "🗑️  Removing added repositories..."
    for repo_args in "${ADDED_REPOS[@]}"; do
        echo "❌ Removing repository: $repo_args"
        eval "add-apt-repository --yes --remove $repo_args" || echo "⚠️  Failed to remove repo: $repo_args" >&2
    done
fi

if "$DO_CLEAN"; then
    echo "🧹 Cleaning up."
    # Starting from APT 2.7.8, the `apt-get` command accepts the `dist-clean` option,
    # which removes list files automatically instead of "rm -rf /var/lib/apt/lists/*"
    # - https://tracker.debian.org/news/1492892/accepted-apt-278-source-into-unstable/
    # - https://github.com/docker-library/buildpack-deps/pull/157/files
    if ! apt-get dist-clean; then
        echo "⚠️  'apt-get dist-clean' failed — falling back to 'apt-get clean'."
        apt-get clean
        rm -rf /var/lib/apt/lists/*
    fi
fi

echo "🏁 Finished installing APT packages."
