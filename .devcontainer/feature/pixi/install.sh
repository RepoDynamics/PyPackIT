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
_LOGFILE_TMP="$(mktemp)"
exec > >(tee -a "$_LOGFILE_TMP") 2>&1
echo "↪️ Script entry: Pixi Installation Devcontainer Feature Installer" >&2
trap __cleanup__ EXIT
if [ "$#" -gt 0 ]; then
  echo "ℹ️ Script called with arguments: $@" >&2
  DEBUG=""
  INSTALL_PATH=""
  LOGFILE=""
  VERSION=""
  while [[ $# -gt 0 ]]; do
    case $1 in
      --debug) shift; DEBUG=true; echo "📩 Read argument 'debug': '"$DEBUG"'" >&2;;
      --install_path) shift; INSTALL_PATH="$1"; echo "📩 Read argument 'install_path': '"$INSTALL_PATH"'" >&2; shift;;
      --logfile) shift; LOGFILE="$1"; echo "📩 Read argument 'logfile': '"$LOGFILE"'" >&2; shift;;
      --version) shift; VERSION="$1"; echo "📩 Read argument 'version': '"$VERSION"'" >&2; shift;;
      --*) echo "⛔ Unknown option: "$1"" >&2; exit 1;;
      *) echo "⛔ Unexpected argument: "$1"" >&2; exit 1;;
    esac
  done
else
  echo "ℹ️ Script called with no arguments. Read environment variables." >&2
  [ "${DEBUG+defined}" ] && echo "📩 Read argument 'debug': '"$DEBUG"'" >&2
  [ "${INSTALL_PATH+defined}" ] && echo "📩 Read argument 'install_path': '"$INSTALL_PATH"'" >&2
  [ "${LOGFILE+defined}" ] && echo "📩 Read argument 'logfile': '"$LOGFILE"'" >&2
  [ "${VERSION+defined}" ] && echo "📩 Read argument 'version': '"$VERSION"'" >&2
fi
[[ "$DEBUG" == true ]] && set -x
[ -z "${INSTALL_PATH-}" ] && { echo "ℹ️ Argument 'INSTALL_PATH' set to default value '/usr/local/bin'." >&2; INSTALL_PATH="/usr/local/bin"; }
[ -z "${LOGFILE-}" ] && { echo "ℹ️ Argument 'LOGFILE' set to default value ''." >&2; LOGFILE=""; }
[ -z "${VERSION-}" ] && { echo "ℹ️ Argument 'VERSION' set to default value '0.46.0'." >&2; VERSION="0.46.0"; }
pixi_bin="${INSTALL_PATH}/pixi"
curl \
  --compressed \
  -fsSLo "$pixi_bin" \
  "https://github.com/prefix-dev/pixi/releases/download/v${VERSION}/pixi-$(uname -m)-unknown-linux-musl"
chmod +x "$pixi_bin"
pixi info
echo "↩️ Script exit: Pixi Installation Devcontainer Feature Installer" >&2
