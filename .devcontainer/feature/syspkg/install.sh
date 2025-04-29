#!/usr/bin/env bash
set -euo pipefail
__cleanup__() {
  echo "↪️ Function entry: __cleanup__" >&2
  if [ -n "${LOGFILE-}" ]; then
    echo "ℹ️ Write logs to file '$LOGFILE'" >&2
    mkdir -p "$(dirname "$LOGFILE")"
    cat "$_LOGFILE_TMP" >> "$LOGFILE"
    rm -f "$_LOGFILE_TMP"
  fi
  echo "↩️ Function exit: __cleanup__" >&2
}
clean_apk() {
  echo "↪️ Function entry: clean_apk" >&2
  rm -rf /var/cache/apk/*
  echo "↩️ Function exit: clean_apk" >&2
}
clean_apt() {
  echo "↪️ Function entry: clean_apt" >&2
  if ! apt-get dist-clean; then
      echo "⚠️  'apt-get dist-clean' failed — falling back to 'apt-get clean'."
      apt-get clean
      rm -rf /var/lib/apt/lists/*
  fi
  echo "↩️ Function exit: clean_apt" >&2
}
clean_dnf() {
  echo "↪️ Function entry: clean_dnf" >&2
  dnf clean all
  rm -rf /var/cache/dnf/*
  echo "↩️ Function exit: clean_dnf" >&2
}
clean_microdnf() {
  echo "↪️ Function entry: clean_microdnf" >&2
  microdnf clean all
  rm -rf /var/cache/dnf/*
  echo "↩️ Function exit: clean_microdnf" >&2
}
clean_yum() {
  echo "↪️ Function entry: clean_yum" >&2
  yum clean all
  rm -rf /var/cache/yum/*
  echo "↩️ Function exit: clean_yum" >&2
}
exit_if_not_root() {
  echo "↪️ Function entry: exit_if_not_root" >&2
  if [ "$(id -u)" -ne 0 ]; then
      echo '⛔ This script must be run as root. Use sudo, su, or add "USER root" to your Dockerfile before running this script.' >&2
      exit 1
  fi
  echo "↩️ Function exit: exit_if_not_root" >&2
}
install() {
  echo "↪️ Function entry: install" >&2
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
  echo "↩️ Function exit: install" >&2
}
_LOGFILE_TMP="$(mktemp)"
exec > >(tee -a "$_LOGFILE_TMP") 2>&1
echo "↪️ Script entry: System Package Installation" >&2
trap __cleanup__ EXIT
if [ "$#" -gt 0 ]; then
  echo "ℹ️ Script called with arguments: $@" >&2
  APK=""
  APT=""
  APT_REPOS=""
  DEBUG=""
  DNF=""
  INTERACTIVE="false"
  KEEP_REPOS="false"
  LOGFILE=""
  MICRODNF=""
  NO_CLEAN="false"
  NO_UPDATE="false"
  YUM=""
  while [[ $# -gt 0 ]]; do
    case $1 in
      --apk) shift; APK="$1"; echo "📩 Read argument 'apk': '"$APK"'" >&2; shift;;
      --apt) shift; APT="$1"; echo "📩 Read argument 'apt': '"$APT"'" >&2; shift;;
      --apt_repos) shift; APT_REPOS="$1"; echo "📩 Read argument 'apt_repos': '"$APT_REPOS"'" >&2; shift;;
      --debug) shift; DEBUG=true; echo "📩 Read argument 'debug': '"$DEBUG"'" >&2;;
      --dnf) shift; DNF="$1"; echo "📩 Read argument 'dnf': '"$DNF"'" >&2; shift;;
      --interactive) shift; INTERACTIVE=true; echo "📩 Read argument 'interactive': '"$INTERACTIVE"'" >&2;;
      --keep_repos) shift; KEEP_REPOS=true; echo "📩 Read argument 'keep_repos': '"$KEEP_REPOS"'" >&2;;
      --logfile) shift; LOGFILE="$1"; echo "📩 Read argument 'logfile': '"$LOGFILE"'" >&2; shift;;
      --microdnf) shift; MICRODNF="$1"; echo "📩 Read argument 'microdnf': '"$MICRODNF"'" >&2; shift;;
      --no_clean) shift; NO_CLEAN=true; echo "📩 Read argument 'no_clean': '"$NO_CLEAN"'" >&2;;
      --no_update) shift; NO_UPDATE=true; echo "📩 Read argument 'no_update': '"$NO_UPDATE"'" >&2;;
      --yum) shift; YUM="$1"; echo "📩 Read argument 'yum': '"$YUM"'" >&2; shift;;
      --*) echo "⛔ Unknown option: "$1"" >&2; exit 1;;
      *) echo "⛔ Unexpected argument: "$1"" >&2; exit 1;;
    esac
  done
else
  echo "ℹ️ Script called with no arguments. Read environment variables." >&2
  [ "${APK+defined}" ] && echo "📩 Read argument 'apk': '"$APK"'" >&2
  [ "${APT+defined}" ] && echo "📩 Read argument 'apt': '"$APT"'" >&2
  [ "${APT_REPOS+defined}" ] && echo "📩 Read argument 'apt_repos': '"$APT_REPOS"'" >&2
  [ "${DEBUG+defined}" ] && echo "📩 Read argument 'debug': '"$DEBUG"'" >&2
  [ "${DNF+defined}" ] && echo "📩 Read argument 'dnf': '"$DNF"'" >&2
  [ "${INTERACTIVE+defined}" ] && echo "📩 Read argument 'interactive': '"$INTERACTIVE"'" >&2
  [ "${KEEP_REPOS+defined}" ] && echo "📩 Read argument 'keep_repos': '"$KEEP_REPOS"'" >&2
  [ "${LOGFILE+defined}" ] && echo "📩 Read argument 'logfile': '"$LOGFILE"'" >&2
  [ "${MICRODNF+defined}" ] && echo "📩 Read argument 'microdnf': '"$MICRODNF"'" >&2
  [ "${NO_CLEAN+defined}" ] && echo "📩 Read argument 'no_clean': '"$NO_CLEAN"'" >&2
  [ "${NO_UPDATE+defined}" ] && echo "📩 Read argument 'no_update': '"$NO_UPDATE"'" >&2
  [ "${YUM+defined}" ] && echo "📩 Read argument 'yum': '"$YUM"'" >&2
fi
[[ "$DEBUG" == true ]] && set -x
[ -z "${APK-}" ] && { echo "ℹ️ Argument 'APK' set to default value ''." >&2; APK=""; }
[ -n "${APK-}" ] && [ ! -f "$APK" ] && { echo "⛔ File argument to parameter 'APK' not found: '$APK'" >&2; exit 1; }
[ -z "${APT-}" ] && { echo "ℹ️ Argument 'APT' set to default value ''." >&2; APT=""; }
[ -n "${APT-}" ] && [ ! -f "$APT" ] && { echo "⛔ File argument to parameter 'APT' not found: '$APT'" >&2; exit 1; }
[ -z "${APT_REPOS-}" ] && { echo "ℹ️ Argument 'APT_REPOS' set to default value ''." >&2; APT_REPOS=""; }
[ -n "${APT_REPOS-}" ] && [ ! -f "$APT_REPOS" ] && { echo "⛔ File argument to parameter 'APT_REPOS' not found: '$APT_REPOS'" >&2; exit 1; }
[ -z "${DNF-}" ] && { echo "ℹ️ Argument 'DNF' set to default value ''." >&2; DNF=""; }
[ -n "${DNF-}" ] && [ ! -f "$DNF" ] && { echo "⛔ File argument to parameter 'DNF' not found: '$DNF'" >&2; exit 1; }
[ -z "${LOGFILE-}" ] && { echo "ℹ️ Argument 'LOGFILE' set to default value ''." >&2; LOGFILE=""; }
[ -z "${MICRODNF-}" ] && { echo "ℹ️ Argument 'MICRODNF' set to default value ''." >&2; MICRODNF=""; }
[ -n "${MICRODNF-}" ] && [ ! -f "$MICRODNF" ] && { echo "⛔ File argument to parameter 'MICRODNF' not found: '$MICRODNF'" >&2; exit 1; }
[ -z "${YUM-}" ] && { echo "ℹ️ Argument 'YUM' set to default value ''." >&2; YUM=""; }
[ -n "${YUM-}" ] && [ ! -f "$YUM" ] && { echo "⛔ File argument to parameter 'YUM' not found: '$YUM'" >&2; exit 1; }
exit_if_not_root
if [[ -z "$APT" && -z "$APK" && -z "$DNF" && -z "$MICRODNF" && -z "$YUM" ]]; then
    echo "⛔ No package list file provided." >&2
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
mapfile -t PACKAGES < <(grep -Ev '^\s*(#|$)' "$PKG_FILE")
if [[ ${#PACKAGES[@]} -eq 0 ]]; then
    echo "⛔ No packages found in file '$PKG_FILE'." >&2
    exit 1
fi
if [[ "$INTERACTIVE" == false ]]; then
    echo "🆗 Setting APT to non-interactive mode."
    export DEBIAN_FRONTEND=noninteractive
fi
ADDED_REPOS=()
if [[ -n "$APT_REPOS" ]]; then
    if [[ ! -f "$APT_REPOS" ]]; then
        echo "⛔ Repo file '$APT_REPOS' does not exist." >&2
        exit 1
    fi
    echo "🗃 Adding APT repositories from '$APT_REPOS'."
    while IFS= read -r line; do
        [[ -z "${line:-}" || "${line}" =~ ^[[:space:]]*# ]] && continue
        echo "📦 Adding repository: $line"
        eval "add-apt-repository --yes $line"
        ADDED_REPOS+=("$line")
    done < "$APT_REPOS"
fi
if [[ "$NO_UPDATE" == false ]]; then
    echo "🔄 Updating package lists."
    "${UPDATE[@]}"
    if [[ $? -ne 0 ]]; then
        echo "⚠️  Failed to update package lists." >&2
        exit 1
    fi
fi
install "${PACKAGES[@]}"
if [[ -n "$APT_REPOS" && "$KEEP_REPOS" == false ]]; then
    echo "🗑️  Removing added repositories..."
    for repo_args in "${ADDED_REPOS[@]}"; do
        echo "❌ Removing repository: $repo_args"
        eval "add-apt-repository --yes --remove $repo_args" || echo "⚠️  Failed to remove repo: $repo_args" >&2
    done
fi
if [[ "$NO_CLEAN" == false ]]; then
    echo "🧹 Cleaning up."
    "${CLEAN[@]}"
fi
echo "✅ Package installation complete."
echo "↩️ Script exit: System Package Installation" >&2
