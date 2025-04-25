#!/bin/bash

set -euo pipefail

# Default arguments
SOURCE=""
MANIFEST=""
ACTION="write"
LOGFILE=""
DEBUG=false
HANDLED_PATHS=""

show_help() {
    echo "============"
    echo "Volume Setup"
    echo "============"
    echo "Set up files and directories in the root of the system."
    echo
    echo "Usage: $0 <source-dir> [--manifest <filepath>] [--action append|prepend|write]"
    echo
    echo "Positional arguments:"
    echo "    <source-dir>            Directory containing source files to be set up."
    echo
    echo "Options:"
    echo "    --manifest <filepath>   Path to a manifest file."
    echo "                            This is a plain text file containing additional instructions."
    echo "    --action <action>       Default action to perform on files in source-dir."
    echo "                            Options: append, prepend, write."
    echo "                            Default: '$ACTION'"
    echo "    --logfile <path>        Log all output (stdout + stderr) to this file in addition to console."
    echo "                            Otherwise output is only printed to the console."
    echo "    --debug                 Enable debug mode."
    echo "    --help                  Show this help message and exit."
    echo
    echo "Example:"
    echo "    $0 /path/to/source/dir --manifest /path/to/manifest.txt --action append"
}

execute() {
    action="$1"
    relpath="$2"
    chmod_mode="${3:-}"

    abs_path="$(normalize_path "$relpath")"
    src_path="$SOURCE/$relpath"

    case "$action" in
        write)
            if [ "${abs_path%/}" != "$abs_path" ]; then
                mkdir -p "$abs_path"
                log_info "📁 Created directory: $abs_path"
            else
                make_parent_dirs "$abs_path"
                cp -fL "$src_path" "$abs_path"
                log_info "📄 Wrote file to: $abs_path"
            fi
            ;;
        delete)
            if [ -d "$abs_path" ]; then
                rm -rf "$abs_path"
                log_info "🗑️ Removed directory: $abs_path"
            elif [ -e "$abs_path" ]; then
                rm -f "$abs_path"
                log_info "🗑️ Removed file: $abs_path"
            else
                log_warn "Path does not exist for deletion: $abs_path"
            fi
            return 0
            ;;
        append)
            make_parent_dirs "$abs_path"
            cat "$src_path" >> "$abs_path"
            log_info "➕ Appended to: $abs_path"
            ;;
        prepend)
            make_parent_dirs "$abs_path"
            tmpf=$(mktemp)
            cat "$src_path" > "$tmpf"
            [ -f "$abs_path" ] && cat "$abs_path" >> "$tmpf"
            mv "$tmpf" "$abs_path"
            log_info "🔼 Prepended to: $abs_path"
            ;;
        *)
            log_error "Unknown action: $action"
            exit 1
            ;;
    esac

    if [ -n "$chmod_mode" ] && [ "$action" != "delete" ]; then
        if echo "$chmod_mode" | grep -q '[[:space:]]'; then
            log_error "⚠️  Invalid chmod mode (contains spaces): '$chmod_mode'"
            exit 1
        else
            chmod "$chmod_mode" "$abs_path"
            log_info "🔐 Set permissions '$chmod_mode' on: $abs_path"
        fi
    fi

    HANDLED_PATHS="$HANDLED_PATHS\n$relpath"
}

make_parent_dirs() {
    dir_path=$(dirname "$1")
    if [ ! -d "$dir_path" ]; then
        mkdir -p "$dir_path"
        log_info "Created parent directory: $dir_path"
    fi
}

normalize_path() {
    case "$1" in
        /*) printf "%s" "$1" ;;
        *)  printf "/%s" "$1" ;;
    esac
}

trim() {
    # Removes leading and trailing whitespace
    echo "$1" | sed 's/^\s*//;s/\s*$//'
}

log_info()  { printf '\033[1;34m🔍 INFO:\033[0m %s\n' "$1"; }
log_warn()  { printf '\033[1;33m⚠️  WARN:\033[0m %s\n' "$1"; }
log_error() { printf '\033[1;31m❌ ERROR:\033[0m %s\n' "$1" >&2; }
log_success() { printf '\033[1;32m✅ DONE:\033[0m %s\n' "$1"; }


if [ $# -lt 1 ]; then
    show_help
fi

SOURCE="${1%/}"  # Remove trailing slash if present
shift

while [ "$#" -gt 0 ]; do
    case "$1" in
        --manifest) MANIFEST="$2"; shift ;;
        --action) ACTION="$2"; shift ;;
        --logfile) LOGFILE="$2"; shift ;;
        --debug) DEBUG=true ;;
        --help) show_help; exit 0 ;;
        *) show_help; exit 1 ;;
    esac
    shift
done

echo "📩 Input Arguments:"
echo "   - source-dir: $SOURCE"
echo "   - manifest: $MANIFEST"
echo "   - action: $ACTION"
echo "   - logfile: $LOGFILE"
echo "   - debug: $DEBUG"

if [[ "$DEBUG" == true ]]; then
    set -x
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

if [ ! -d "$SOURCE" ]; then
    log_error "Source directory '$SOURCE' does not exist."
    exit 1
fi

if [ -n "$MANIFEST" ] && [ ! -f "$MANIFEST" ]; then
    log_error "Manifest file '$MANIFEST' does not exist."
    exit 1
fi

case "$ACTION" in
    append|prepend|write) : ;; # OK
    *) log_error "Invalid default action: $ACTION"; exit 1 ;;
esac

# Process manifest file entries.
if [ -n "$MANIFEST" ] && [ -f "$MANIFEST" ]; then
    log_info "📜 Reading manifest: $MANIFEST"
    while IFS= read -r line || [ -n "$line" ]; do
        # Skip empty lines and comments
        case "$line" in
            ''|[[:space:]]*\#*) continue ;;
        esac

        chmod_mode=""
        if echo "$line" | grep -qE '[[:space:]]chmod=[^[:space:]]+$'; then
            chmod_mode=$(echo "$line" | sed -nE 's/.*[[:space:]]chmod=([^[:space:]]+)$/\1/p')
            line=$(echo "$line" | sed -E 's/[[:space:]]chmod=[^[:space:]]+$//')
        fi

        # Parse action and quoted path (handles spacing)
        action=$(echo "$line" | awk '{print $1}')
        path=$(echo "$line" | sed -nE 's/^[^[:space:]]+[[:space:]]+"([^"]+)"[[:space:]]*$/\1/p')

        if [ -z "$action" ] || [ -z "$path" ]; then
            log_error "Invalid manifest line '$line'."
            exit 1
        fi

        execute "$action" "$path" "$chmod_mode"
    done < "$MANIFEST"
fi


# Apply default action to all remaining files in the source directory.
log_info "🔍 Scanning source directory for remaining files"
find "$SOURCE" -type f | while read -r filepath; do
    relpath="${filepath#$SOURCE/}"
    printf "%s\n" "$HANDLED_PATHS" | grep -qxF "$relpath" && continue
    execute "$ACTION" "$relpath"
done

log_success "Volume setup completed successfully."
