#!/bin/bash

set -euo pipefail

# Default arguments
TARGET_UID="1000"
TARGET_GID="1000"
DEBUG=false
LOGFILE=""

show_help() {
    echo "==========================="
    echo "Remove UID and GID entities"
    echo "==========================="
    echo
    echo "Usage: $0 --uid <uid> --gid <gid> [--debug] [--logfile <path>]"
    echo
    echo "Options:"
    echo "    --uid <uid>         Target UID to remove (if exists)."
    echo "                        Default: $TARGET_UID"
    echo "    --gid <gid>         Target GID to remove (if exists)."
    echo "                        Default: $TARGET_GID"
    echo "    --logfile <path>    Write output to a logfile as well as console."
    echo "    --debug             Enable debug mode."
    echo "    --help              Show this help message and exit."
    echo
    echo "Example:"
    echo "    $0 --uid 1001 --gid 1001 --logfile /var/log/user_remove.log"
}

# Parse arguments
while [ "$#" -gt 0 ]; do
    case "$1" in
        --uid) TARGET_UID="$2"; shift ;;
        --gid) TARGET_GID="$2"; shift ;;
        --logfile) LOGFILE="$2"; shift ;;
        --debug) DEBUG=true ;;
        --help) show_help; exit 0 ;;
        *) echo "⛔ Unknown option: $1"; show_help; exit 1 ;;
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

if [ "$(id -u)" -ne 0 ]; then
    echo "⛔ This script must be run as root."
    exit 1
fi

if [ -z "$TARGET_UID" ] || [ -z "$TARGET_GID" ]; then
    echo "⛔ Both --uid and --gid must be provided."
    show_help
    exit 1
fi

# Step 1: Delete users with primary group GID = TARGET_GID
GROUP_LINE=$(getent group "$TARGET_GID" || true)
GROUP_NAME=$(echo "$GROUP_LINE" | cut -d: -f1)

if [ -n "$GROUP_NAME" ]; then
    echo "🔍 Found group '$GROUP_NAME' with GID '$TARGET_GID'."

    USERS=$(awk -F: -v gid="$TARGET_GID" '$4 == gid {print $1}' /etc/passwd)
    for user in $USERS; do
        echo "🧑 Deleting user '$user' from group."
        userdel -r "$user" 2>/dev/null || echo "⚠️ Failed to delete user '$user'."
    done

    if getent group "$GROUP_NAME" >/dev/null; then
        echo "🧺 Deleting group '$GROUP_NAME'."
        groupdel "$GROUP_NAME" 2>/dev/null || echo "⚠️  Failed to delete group '$GROUP_NAME'."
    else
        echo "ℹ️  Group '$GROUP_NAME' deleted."
    fi
else
    echo "ℹ️ No group found with GID '$TARGET_GID'."
fi

# Step 2: Delete user with UID = TARGET_UID (if still exists)
USER_LINE=$(awk -F: -v uid="$TARGET_UID" '$3 == uid {print $0}' /etc/passwd)
USER_NAME=$(echo "$USER_LINE" | cut -d: -f1)

if [ -n "$USER_NAME" ]; then
    echo "🔍 Found user '$USER_NAME' with UID '$TARGET_UID'."
    userdel -r "$USER_NAME" 2>/dev/null || echo "⚠️ Failed to delete user '$USER_NAME'."
else
    echo "ℹ️  No additional user found with UID $TARGET_UID to delete."
fi

echo "✅ Removal process completed."
