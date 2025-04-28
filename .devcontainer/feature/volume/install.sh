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
execute() {
  echo "↪️ Function entry: execute" >&2
  local action=""
  local chmod_mode=""
  local path=""
  while [[ $# -gt 0 ]]; do
    case $1 in
      --action) shift; action="$1"; echo "📩 Read argument 'action': '"$action"'" >&2; shift;;
      --chmod_mode) shift; chmod_mode="$1"; echo "📩 Read argument 'chmod_mode': '"$chmod_mode"'" >&2; shift;;
      --path) shift; path="$1"; echo "📩 Read argument 'path': '"$path"'" >&2; shift;;
      --*) echo "⛔ Unknown option: "$1"" >&2; exit 1;;
      *) echo "⛔ Unexpected argument: "$1"" >&2; exit 1;;
    esac
  done
  [ -z "${action-}" ] && { echo "⛔ Missing required argument 'action'." >&2; exit 1; }
  [ -z "${chmod_mode-}" ] && { echo "ℹ️ Argument 'chmod_mode' set to default value ''." >&2; chmod_mode=""; }
  [ -z "${path-}" ] && { echo "⛔ Missing required argument 'path'." >&2; exit 1; }
  abs_path="$(prepend_slash "$path")"
  src_path="$SOURCE_DIR/$path"
  case "$action" in
      write)
          if [ "${abs_path%/}" != "$abs_path" ]; then
              mkdir -p "$abs_path"
              echo "📁 Created directory: $abs_path"
          else
              make_parent_dirs "$abs_path"
              cp -fL "$src_path" "$abs_path"
              echo "📄 Wrote file to: $abs_path"
          fi
          ;;
      delete)
          if [ -d "$abs_path" ]; then
              rm -rf "$abs_path"
              echo "🗑️ Removed directory: $abs_path"
          elif [ -e "$abs_path" ]; then
              rm -f "$abs_path"
              echo "🗑️ Removed file: $abs_path"
          else
              echo "Path does not exist for deletion: $abs_path"
          fi
          return 0
          ;;
      append)
          make_parent_dirs "$abs_path"
          cat "$src_path" >> "$abs_path"
          echo "➕ Appended to: $abs_path"
          ;;
      prepend)
          make_parent_dirs "$abs_path"
          tmpf=$(mktemp)
          cat "$src_path" > "$tmpf"
          [ -f "$abs_path" ] && cat "$abs_path" >> "$tmpf"
          mv "$tmpf" "$abs_path"
          echo "🔼 Prepended to: $abs_path"
          ;;
      *)
          echo "Unknown action: $action"
          exit 1
          ;;
  esac
  if [ -n "$chmod_mode" ] && [ "$action" != "delete" ]; then
      if echo "$chmod_mode" | grep -q '[[:space:]]'; then
          echo "⚠️  Invalid chmod mode (contains spaces): '$chmod_mode'"
          exit 1
      else
          chmod "$chmod_mode" "$abs_path"
          echo "🔐 Set permissions '$chmod_mode' on: $abs_path"
      fi
  fi
  HANDLED_PATHS="${HANDLED_PATHS-}\n$path"
  echo "↩️ Function exit: execute" >&2
}
exit_if_not_root() {
  echo "↪️ Function entry: exit_if_not_root" >&2
  if [ "$(id -u)" -ne 0 ]; then
      echo '⛔ This script must be run as root. Use sudo, su, or add "USER root" to your Dockerfile before running this script.' >&2
      exit 1
  fi
  echo "↩️ Function exit: exit_if_not_root" >&2
}
make_parent_dirs() {
  echo "↪️ Function entry: make_parent_dirs" >&2
  local filepath=""
  while [[ $# -gt 0 ]]; do
    case $1 in
      --filepath) shift; filepath="$1"; echo "📩 Read argument 'filepath': '"$filepath"'" >&2; shift;;
      --*) echo "⛔ Unknown option: "$1"" >&2; exit 1;;
      *) echo "⛔ Unexpected argument: "$1"" >&2; exit 1;;
    esac
  done
  [ -z "${filepath-}" ] && { echo "⛔ Missing required argument 'filepath'." >&2; exit 1; }
  local dir_path=$(dirname "$filepath")
  if [ ! -d "$dir_path" ]; then
      mkdir -p "$dir_path"
      echo "Created parent directory: $dir_path"
  fi
  echo "↩️ Function exit: make_parent_dirs" >&2
}
prepend_slash() {
  echo "↪️ Function entry: prepend_slash" >&2
  local path=""
  while [[ $# -gt 0 ]]; do
    case $1 in
      --path) shift; path="$1"; echo "📩 Read argument 'path': '"$path"'" >&2; shift;;
      --*) echo "⛔ Unknown option: "$1"" >&2; exit 1;;
      *) echo "⛔ Unexpected argument: "$1"" >&2; exit 1;;
    esac
  done
  [ -z "${path-}" ] && { echo "⛔ Missing required argument 'path'." >&2; exit 1; }
  local modified_path="$path"
  if [[ "$modified_path" != /* ]]; then
      modified_path="/$modified_path"
  fi
  echo "📤 Write output 'modified_path': '"$modified_path"'" >&2
  echo "${modified_path}"
  echo "↩️ Function exit: prepend_slash" >&2
}
process_manifest() {
  echo "↪️ Function entry: process_manifest" >&2
  echo "📜 Reading manifest: $MANIFEST_FILE"
  while IFS= read -r line || [ -n "$line" ]; do
      case "$line" in
          ''|[[:space:]]*\#*) continue ;;
      esac
      local chmod_mode=""
      if echo "$line" | grep -qE '[[:space:]]chmod=[^[:space:]]+$'; then
          chmod_mode=$(echo "$line" | sed -nE 's/.*[[:space:]]chmod=([^[:space:]]+)$/\1/p')
          local line=$(echo "$line" | sed -E 's/[[:space:]]chmod=[^[:space:]]+$//')
      fi
      local action=$(echo "$line" | awk '{print $1}')
      local path=$(echo "$line" | sed -nE 's/^[^[:space:]]+[[:space:]]+"([^"]+)"[[:space:]]*$/\1/p')
      if [ -z "$action" ] || [ -z "$path" ]; then
          echo "Invalid manifest line '$line'."
          exit 1
      fi
      execute "$action" "$path" "$chmod_mode"
  done < "$MANIFEST_FILE"
  echo "↩️ Function exit: process_manifest" >&2
}
_LOGFILE_TMP="$(mktemp)"
exec > >(tee -a "$_LOGFILE_TMP") 2>&1
echo "↪️ Script entry: Volume Setup" >&2
trap __cleanup__ EXIT
if [ "$#" -gt 0 ]; then
  echo "ℹ️ Script called with arguments: $@" >&2
  DEBUG=""
  DEFAULT_ACTION=""
  LOGFILE=""
  MANIFEST_FILE=""
  SOURCE_DIR=""
  while [[ $# -gt 0 ]]; do
    case $1 in
      --debug) shift; DEBUG=true; echo "📩 Read argument 'debug': '"$DEBUG"'" >&2;;
      --default_action) shift; DEFAULT_ACTION="$1"; echo "📩 Read argument 'default_action': '"$DEFAULT_ACTION"'" >&2; shift;;
      --logfile) shift; LOGFILE="$1"; echo "📩 Read argument 'logfile': '"$LOGFILE"'" >&2; shift;;
      --manifest_file) shift; MANIFEST_FILE="$1"; echo "📩 Read argument 'manifest_file': '"$MANIFEST_FILE"'" >&2; shift;;
      --source_dir) shift; SOURCE_DIR="$1"; echo "📩 Read argument 'source_dir': '"$SOURCE_DIR"'" >&2; shift;;
      --*) echo "⛔ Unknown option: "$1"" >&2; exit 1;;
      *) echo "⛔ Unexpected argument: "$1"" >&2; exit 1;;
    esac
  done
else
  echo "ℹ️ Script called with no arguments. Read environment variables." >&2
  [ "${DEBUG+defined}" ] && echo "📩 Read argument 'debug': '"$DEBUG"'" >&2
  [ "${DEFAULT_ACTION+defined}" ] && echo "📩 Read argument 'default_action': '"$DEFAULT_ACTION"'" >&2
  [ "${LOGFILE+defined}" ] && echo "📩 Read argument 'logfile': '"$LOGFILE"'" >&2
  [ "${MANIFEST_FILE+defined}" ] && echo "📩 Read argument 'manifest_file': '"$MANIFEST_FILE"'" >&2
  [ "${SOURCE_DIR+defined}" ] && echo "📩 Read argument 'source_dir': '"$SOURCE_DIR"'" >&2
fi
[[ "$DEBUG" == true ]] && set -x
[ -z "${DEFAULT_ACTION-}" ] && { echo "ℹ️ Argument 'DEFAULT_ACTION' set to default value 'write'." >&2; DEFAULT_ACTION="write"; }
case "$DEFAULT_ACTION" in
  "append"|"prepend"|"write"|"");;
  *) echo "⛔ Invalid value for argument '--DEFAULT_ACTION': '$DEFAULT_ACTION'" >&2; exit 1;;
esac
[ -z "${LOGFILE-}" ] && { echo "ℹ️ Argument 'LOGFILE' set to default value ''." >&2; LOGFILE=""; }
[ -z "${MANIFEST_FILE-}" ] && { echo "⛔ Missing required argument 'MANIFEST_FILE'." >&2; exit 1; }
[ -n ${MANIFEST_FILE-} ] && [ ! -f "$MANIFEST_FILE" ] && { echo "⛔ File argument to parameter 'MANIFEST_FILE' not found: '$MANIFEST_FILE'" >&2; exit 1; }
[ -z "${SOURCE_DIR-}" ] && { echo "⛔ Missing required argument 'SOURCE_DIR'." >&2; exit 1; }
[ -n ${SOURCE_DIR-} ] && [ ! -d "$SOURCE_DIR" ] && { echo "⛔ Directory argument to parameter 'SOURCE_DIR' not found: '$SOURCE_DIR'" >&2; exit 1; }
exit_if_not_root
SOURCE_DIR="${SOURCE_DIR%/}"
if [ -n "$MANIFEST_FILE" ] && [ -f "$MANIFEST_FILE" ]; then
    process_manifest
fi
echo "🔍 Scanning source directory for remaining files"
find "$SOURCE_DIR" -type f | while read -r filepath; do
    relpath="${filepath#$SOURCE_DIR/}"
    printf "%s\n" "$HANDLED_PATHS" | grep -qxF "$relpath" && continue
    execute "$DEFAULT_ACTION" "$relpath"
done
echo "✅ Volume setup complete."
echo "↩️ Script exit: Volume Setup" >&2
