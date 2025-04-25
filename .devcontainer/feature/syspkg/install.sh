#!/usr/bin/env bash

set -euo pipefail

# Default arguments
APT=""
APK=""
DNF=""
MICRODNF=""
YUM=""
REPOFILE=""
KEEP_REPOS=false
DO_UPDATE=true
DO_CLEAN=true
NONINTERACTIVE=true
LOGFILE=""
DEBUG=false
ADDED_REPOS=()

show_help() {
    cat <<EOF
====================
Install APT Packages
====================
Usage: $0 [OPTIONS]

Install packages listed in a file using the system's package manager.

Options:
    --apt <path>            Path to a file containing newline-separated
                            package specifications for apt-get.
    --apk <path>            Path to a file containing newline-separated
                            package specifications for apk.
    --dnf <path>            Path to a file containing newline-separated
                            package specifications for dnf.
    --microdnf <path>       Path to a file containing newline-separated
                            package specifications for microdnf.
    --yum <path>            Path to a file containing newline-separated
                            package specifications for yum.
    --repofile <path>       Path to file containing newline-separated arguments
                            to pass to 'add-apt-repository', one set per line.
    --keep-repos            Keep repositories added via --repofile after script ends.
                            By default, they are removed automatically.
    --no-update             Skip 'apt-get update' step before installation.
    --no-clean              Skip 'apt-get dist-clean' step after installation.
    --interactive           Allow apt to prompt the user (default is non-interactive).
    --logfile <path>        Log all output (stdout + stderr) to this file.
                            If not specified, output is only printed to the console.
    --debug                 Enable debug mode.
    --help                  Show this help message and exit.

Example:
    $0 --apt apt.txt --repofile repos.txt --logfile /tmp/install.log --no-clean
EOF
}

# Refs:
# - https://github.com/devcontainers/features/blob/6654579de4c31cd9f9f9e19e873521f502403929/src/git/install.sh

# Install packages using the appropriate package manager.
install() {
    if [ ${PKG_MNGR} = "apt-get" ]; then
        if dpkg -s "$@" > /dev/null 2>&1; then
            echo "Packages already installed: $@"
            return 0
        fi
    elif [ ${INSTALL_CMD} = "dnf" ] || [ ${INSTALL_CMD} = "yum" ]; then
        _num_pkgs=$(echo "$@" | tr ' ' \\012 | wc -l)
        _num_installed=$(${INSTALL_CMD} -C list installed "$@" | sed '1,/^Installed/d' | wc -l)
        if [ ${_num_pkgs} == ${_num_installed} ]; then
            echo "Packages already installed: $@"
            return 0
        fi
    fi
    echo "📲 Installing packages:"
    printf '  - %s\n' "${PACKAGES[@]}"
    "${INSTALL[@]}" "$@"
}

clean_apt() {
    # Starting from APT 2.7.8, the `apt-get` command accepts the `dist-clean` option,
    # which removes list files automatically instead of "rm -rf /var/lib/apt/lists/*"
    # - https://tracker.debian.org/news/1492892/accepted-apt-278-source-into-unstable/
    # - https://github.com/docker-library/buildpack-deps/pull/157/files
    if ! apt-get dist-clean; then
        echo "⚠️  'apt-get dist-clean' failed — falling back to 'apt-get clean'."
        apt-get clean
        rm -rf /var/lib/apt/lists/*
    fi
}

clean_apk() {
    rm -rf /var/cache/apk/*
}

clean_dnf() {
    dnf clean all
    rm -rf /var/cache/dnf/*
}

clean_microdnf() {
    microdnf clean all
    rm -rf /var/cache/dnf/*
}

clean_yum() {
    yum clean all
    rm -rf /var/cache/yum/*
}

while [ "$#" -gt 0 ]; do
    case "$1" in
        --apt) APT="$2"; shift ;;
        --apk) APK="$2"; shift ;;
        --dnf) DNF="$2"; shift ;;
        --microdnf) MICRODNF="$2"; shift ;;
        --yum) YUM="$2"; shift ;;
        --repofile) REPOFILE="$2"; shift ;;
        --keep-repos) KEEP_REPOS=true ;;
        --no-update) DO_UPDATE=false ;;
        --no-clean) DO_CLEAN=false ;;
        --interactive) NONINTERACTIVE=false ;;
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
echo "   - apt: $APT"
echo "   - apk: $APK"
echo "   - dnf: $DNF"
echo "   - microdnf: $MICRODNF"
echo "   - yum: $YUM"
echo "   - repofile: $REPOFILE"
echo "   - keep-repos: $KEEP_REPOS"
echo "   - no-update: $DO_UPDATE"
echo "   - no-clean: $DO_CLEAN"
echo "   - interactive: $NONINTERACTIVE"
echo "   - logfile: $LOGFILE"
echo "   - debug: $DEBUG"

if [ "$(id -u)" -ne 0 ]; then
    echo -e '⛔ This script must be run as root. Use sudo, su, or add "USER root" to your Dockerfile before running this script.' >&2
    exit 1
fi

if [[ -z "$APT" && -z "$APK" && -z "$DNF" && -z "$MICRODNF" && -z "$YUM" ]]; then
    echo "⛔ No package list file provided. Use --apt, --apk, --dnf, --microdnf, or --yum." >&2
    exit 1
fi

if type apt-get > /dev/null 2>&1; then
    echo "🛠️  Using APT package manager."
    PKG_FILE="$APT"
    PKG_MNGR="apt-get"
    UPDATE=($PKG_MNGR update -y)
    INSTALL=($PKG_MNGR -y install --no-install-recommends)
    CLEAN=(clean_apt)
elif type apk > /dev/null 2>&1; then
    echo "🛠️  Using APK package manager."
    PKG_FILE="$APK"
    PKG_MNGR="apk"
    UPDATE=($PKG_MNGR update)
    INSTALL=($PKG_MNGR add --no-cache)
    CLEAN=(clean_apk)
elif type microdnf > /dev/null 2>&1; then
    echo "🛠️  Using MicroDNF package manager."
    PKG_FILE="$MICRODNF"
    PKG_MNGR=microdnf
    UPDATE=()
    INSTALL=($PKG_MNGR -y install --refresh --best --nodes --noplugins --setopt=install_weak_deps=0)
    CLEAN=(clean_microdnf)
elif type dnf > /dev/null 2>&1; then
    echo "🛠️  Using DNF package manager."
    PKG_FILE="$DNF"
    PKG_MNGR=dnf
    UPDATE=($PKG_MNGR check-update)
    INSTALL=($PKG_MNGR -y install)
    CLEAN=(clean_dnf)
elif type yum > /dev/null 2>&1; then
    echo "🛠️  Using YUM package manager."
    PKG_FILE="$YUM"
    PKG_MNGR=yum
    UPDATE="$PKG_MNGR check-update"
    INSTALL=($PKG_MNGR -y install)
    CLEAN=(clean_yum)
else
    echo "(Error) Unable to find a supported package manager."
    exit 1
fi


if [[ ! -f "$PKG_FILE" ]]; then
    echo "⛔ Package list file '$PKG_FILE' does not exist." >&2
    exit 1
fi

# Read the package list file and filter out comments and empty lines
mapfile -t PACKAGES < <(grep -Ev '^\s*(#|$)' "$PKG_FILE")
if [[ ${#PACKAGES[@]} -eq 0 ]]; then
    echo "⛔ No packages found in file '$PKG_FILE'." >&2
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
    "${UPDATE[@]}"
    if [[ $? -ne 0 ]]; then
        echo "⚠️  Failed to update package lists." >&2
        exit 1
    fi
fi

install "${PACKAGES[@]}"

if [[ -n "$REPOFILE" && "$KEEP_REPOS" == false ]]; then
    echo "🗑️  Removing added repositories..."
    for repo_args in "${ADDED_REPOS[@]}"; do
        echo "❌ Removing repository: $repo_args"
        eval "add-apt-repository --yes --remove $repo_args" || echo "⚠️  Failed to remove repo: $repo_args" >&2
    done
fi

if "$DO_CLEAN"; then
    echo "🧹 Cleaning up."
    "${CLEAN[@]}"
fi

echo "🏁 Finished installing APT packages."
