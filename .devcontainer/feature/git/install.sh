#!/usr/bin/env bash
set -euo pipefail
__cleanup__() {
  echo "↪️ Function entry: __cleanup__" >&2
  [[ "$NO_CLEAN" == false ]] && (cd / && rm -rf "$INSTALLER_DIR/git-$VERSION")
  if [ -n "${LOGFILE-}" ]; then
    echo "ℹ️ Write logs to file '$LOGFILE'" >&2
    mkdir -p "$(dirname "$LOGFILE")"
    cat "$_LOGFILE_TMP" >> "$LOGFILE"
    rm -f "$_LOGFILE_TMP"
  fi
  echo "↩️ Function exit: __cleanup__" >&2
}
exit_if_not_root() {
  echo "↪️ Function entry: exit_if_not_root" >&2
  if [ "$(id -u)" -ne 0 ]; then
      echo '⛔ This script must be run as root. Use sudo, su, or add "USER root" to your Dockerfile before running this script.' >&2
      exit 1
  fi
  echo "↩️ Function exit: exit_if_not_root" >&2
}
get_script_dir() {
  echo "↪️ Function entry: get_script_dir" >&2
  local script_dir="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"
  echo "📤 Write output 'script_dir': '"$script_dir"'" >&2
  echo "${script_dir}"
  echo "↩️ Function exit: get_script_dir" >&2
}
_LOGFILE_TMP="$(mktemp)"
exec > >(tee -a "$_LOGFILE_TMP") 2>&1
echo "↪️ Script entry: Git Installation" >&2
trap __cleanup__ EXIT
if [ "$#" -gt 0 ]; then
  echo "ℹ️ Script called with arguments: $@" >&2
  DEBUG=""
  INSTLLER_DIR=""
  LOGFILE=""
  NO_CLEAN=""
  PREFIX=""
  SOURCE=""
  SYSCONFDIR=""
  VERSION=""
  while [[ $# -gt 0 ]]; do
    case $1 in
      --debug) shift; DEBUG=true; echo "📩 Read argument 'debug': '"$DEBUG"'" >&2;;
      --instller_dir) shift; INSTLLER_DIR="$1"; echo "📩 Read argument 'instller_dir': '"$INSTLLER_DIR"'" >&2; shift;;
      --logfile) shift; LOGFILE="$1"; echo "📩 Read argument 'logfile': '"$LOGFILE"'" >&2; shift;;
      --no_clean) shift; NO_CLEAN=true; echo "📩 Read argument 'no_clean': '"$NO_CLEAN"'" >&2;;
      --prefix) shift; PREFIX="$1"; echo "📩 Read argument 'prefix': '"$PREFIX"'" >&2; shift;;
      --source) shift; SOURCE="$1"; echo "📩 Read argument 'source': '"$SOURCE"'" >&2; shift;;
      --sysconfdir) shift; SYSCONFDIR="$1"; echo "📩 Read argument 'sysconfdir': '"$SYSCONFDIR"'" >&2; shift;;
      --version) shift; VERSION="$1"; echo "📩 Read argument 'version': '"$VERSION"'" >&2; shift;;
      --*) echo "⛔ Unknown option: "$1"" >&2; exit 1;;
      *) echo "⛔ Unexpected argument: "$1"" >&2; exit 1;;
    esac
  done
else
  echo "ℹ️ Script called with no arguments. Read environment variables." >&2
  [ "${DEBUG+defined}" ] && echo "📩 Read argument 'debug': '"$DEBUG"'" >&2
  [ "${INSTLLER_DIR+defined}" ] && echo "📩 Read argument 'instller_dir': '"$INSTLLER_DIR"'" >&2
  [ "${LOGFILE+defined}" ] && echo "📩 Read argument 'logfile': '"$LOGFILE"'" >&2
  [ "${NO_CLEAN+defined}" ] && echo "📩 Read argument 'no_clean': '"$NO_CLEAN"'" >&2
  [ "${PREFIX+defined}" ] && echo "📩 Read argument 'prefix': '"$PREFIX"'" >&2
  [ "${SOURCE+defined}" ] && echo "📩 Read argument 'source': '"$SOURCE"'" >&2
  [ "${SYSCONFDIR+defined}" ] && echo "📩 Read argument 'sysconfdir': '"$SYSCONFDIR"'" >&2
  [ "${VERSION+defined}" ] && echo "📩 Read argument 'version': '"$VERSION"'" >&2
fi
[[ "$DEBUG" == true ]] && set -x
[ -z "${DEBUG-}" ] && { echo "ℹ️ Argument 'DEBUG' set to default value 'false'." >&2; DEBUG=false; }
[ -z "${INSTLLER_DIR-}" ] && { echo "ℹ️ Argument 'INSTLLER_DIR' set to default value '/tmp/git-installer'." >&2; INSTLLER_DIR="/tmp/git-installer"; }
[ -z "${LOGFILE-}" ] && { echo "ℹ️ Argument 'LOGFILE' set to default value ''." >&2; LOGFILE=""; }
[ -z "${NO_CLEAN-}" ] && { echo "ℹ️ Argument 'NO_CLEAN' set to default value 'false'." >&2; NO_CLEAN=false; }
[ -z "${PREFIX-}" ] && { echo "ℹ️ Argument 'PREFIX' set to default value '/usr/local/git'." >&2; PREFIX="/usr/local/git"; }
[ -z "${SOURCE-}" ] && { echo "ℹ️ Argument 'SOURCE' set to default value 'https://www.kernel.org/pub/software/scm/git/git-'." >&2; SOURCE="https://www.kernel.org/pub/software/scm/git/git-"; }
[ -z "${SYSCONFDIR-}" ] && { echo "ℹ️ Argument 'SYSCONFDIR' set to default value '/etc'." >&2; SYSCONFDIR="/etc"; }
[ -z "${VERSION-}" ] && { echo "ℹ️ Argument 'VERSION' set to default value ''." >&2; VERSION=""; }
exit_if_not_root
"$SYSPKG_INSTALL_SCRIPT" \
  --apt "$(get_script_dir)/requirements/apt.txt" \
  --logfile "$LOGFILE" \
  $( [ "$DEBUG" = "true" ] && echo --debug )
VERSION=$(
    get_matching_github_refs \
        --owner git \
        --repo git \
        --ref "tags/v" \
        --remove_prefix "tags/v" \
        --regex "$VERSION"
)
mkdir -p "$INSTALLER_DIR"
echo "📥 Download source code for Git v${VERSION}."
curl -sL "${SOURCE}${VERSION}.tar.gz" | tar -xzC "$INSTALLER_DIR" 2>&1
echo "🏗 Build Git."
cd "$INSTALLER_DIR/git-$VERSION"
git_options=("prefix=$PREFIX")
git_options+=("sysconfdir=$SYSCONFDIR")
git_options+=("USE_LIBPCRE=YesPlease")
make -s "${git_options[@]}" all && make -s "${git_options[@]}" install 2>&1
echo "✅ Git v${VERSION} installed successfully."
echo "↩️ Script exit: Git Installation" >&2
