#!/usr/bin/env bash
set -euxo pipefail

export DEBIAN_FRONTEND=noninteractive

# Constants
LOG_FILE_NAME="install.log"
SUDOERS_DIR="/etc/sudoers.d"

# Utility: link tool path only if source exists
link_if_exists() {
    local src="$1"
    local dest="$2"
    local label="$3"

    if [ -e "$src" ]; then
        mkdir -p "$(dirname "$dest")"
        ln -snf "$src" "$dest"
        echo "✔️ Linked $label"
    else
        echo "⏩ Skipped $label (not found: $src)"
    fi
}

get_debian_flavor() {
    local codename=""

    if [ -f /etc/os-release ]; then
        . /etc/os-release
        codename="${VERSION_CODENAME:-}"
    fi

    # Fallback to lsb_release if codename is still empty
    if [ -z "$codename" ] && command -v lsb_release >/dev/null 2>&1; then
        codename="$(lsb_release -c -s)"
    fi

    # Final fallback
    codename="${codename:-unknown}"

    echo "$codename"
}

# Redirect stdout and stderr to a file
echo "Creating log directory..."
mkdir -p "$LOG_DIRPATH"
exec > >(tee -a "${LOG_DIRPATH}/${LOG_FILE_NAME}") 2>&1

# Ensure script is run as root
if [ "$(id -u)" -ne 0 ]; then
    echo -e 'Script must be run as root. Use sudo, su, or add "USER root" to your Dockerfile before running this script.'
    exit 1
fi

# Ensure login shells get the correct path if ENV was used to modify PATH.
rm -f /etc/profile.d/00-restore-env.sh
echo "export PATH=${PATH//$(sh -lc 'echo $PATH')/\$PATH}" > /etc/profile.d/00-restore-env.sh
chmod +x /etc/profile.d/00-restore-env.sh

# Determine the appropriate non-root user
USERNAME="${USERNAME:-"${_REMOTE_USER:-"automatic"}"}"
if [ "${USERNAME}" = "automatic" ]; then
    USERNAME=""
    POSSIBLE_USERS=("vscode" "node" "codespace" "$(awk -v val=1000 -F ":" '$3==val{print $1}' /etc/passwd)")
    for CURRENT_USER in "${POSSIBLE_USERS[@]}"; do
        if id -u ${CURRENT_USER} > /dev/null 2>&1; then
            USERNAME=${CURRENT_USER}
            break
        fi
    done
    if [ "${USERNAME}" = "" ]; then
        USERNAME=root
    fi
elif [ "${USERNAME}" = "none" ] || ! id -u ${USERNAME} > /dev/null 2>&1; then
    USERNAME=root
fi

# Set common variables.
HOME_DIR="/home/${USERNAME}"
OPT_DIR="/opt"
DEBIAN_FLAVOR="$(get_debian_flavor)"

# Enable the oryx tool to generate manifest-dir which is needed for running the postcreate tool.
# Oryx expects the tool to be installed at `/opt/oryx` and looks for relevant files in there.
ORYX_DIR="/opt/oryx"
mkdir -p "$ORYX_DIR"
echo "vso-focal" > "$ORYX_DIR/.imagetype"
echo "DEBIAN|${DEBIAN_FLAVOR}-SCM" | tr '[a-z]' '[A-Z]' > "$ORYX_DIR/.ostype"
if compgen -G "/usr/local/oryx/*" > /dev/null; then
    ln -snf /usr/local/oryx/* "$ORYX_DIR"
fi

# Tool links
DOTNET_PATH="${HOME_DIR}/.dotnet"
HUGO_PATH="${HOME_DIR}/.hugo/current"
JAVA_PATH="${HOME_DIR}/java/current"
MAVEN_PATH="${HOME_DIR}/.maven/current"
NODE_PATH="${HOME_DIR}/nvm/current"
PHP_PATH="${HOME_DIR}/.php/current"
PYTHON_PATH="${HOME_DIR}/.python/current"
RUBY_PATH="${HOME_DIR}/.ruby/current"

link_if_exists "/usr/share/dotnet"                          "$DOTNET_PATH"    ".NET SDK"
link_if_exists "/usr/local/hugo"                            "$HUGO_PATH"      "Hugo"
link_if_exists "/usr/local/sdkman/candidates/java"          "$JAVA_PATH"      "Java"  #CHECK
link_if_exists "/usr/local/sdkman/candidates/maven/current" "$MAVEN_PATH"     "Maven"
link_if_exists "/usr/local/share/nvm"                       "${HOME_DIR}/nvm" "Node.js" #CHECK
link_if_exists "/usr/local/php/current"                     "$PHP_PATH"       "PHP"
link_if_exists "/usr/local/python/current"                  "$PYTHON_PATH"    "Python"
link_if_exists "/usr/local/python"                          "/opt/python"     "Python root"
link_if_exists "/usr/local/rvm/rubies/default"              "$RUBY_PATH"      "Ruby"

# .NET special setup
# Required due to https://github.com/devcontainers/features/pull/628/files#r1276659825
if [ -d /usr/share/dotnet ]; then
    DOTNET_DIR="/usr/share/dotnet"
    chown -R "$USERNAME:$USERNAME" "$DOTNET_DIR"
    chmod g+r+w+s "$DOTNET_DIR"
    chmod -R g+r+w "$DOTNET_DIR"

    mkdir -p "$OPT_DIR/dotnet/lts"
    cp -R "$DOTNET_DIR/{dotnet,LICENSE.txt,ThirdPartyNotices.txt}" "$OPT_DIR/dotnet/lts" || true
fi

# Fix permissions for home directory.
chown -R "$USERNAME:$USERNAME" "$HOME_DIR"
chmod -R g+r+w "$HOME_DIR"
find "${HOME_DIR}" -type d | xargs -n 1 chmod g+s
# Fix permissions for opt directory.
if getent group oryx > /dev/null; then
    echo "✅ Group 'oryx' exists, applying group ownership and permissions"
    chown -R "$USERNAME:oryx" "$OPT_DIR"
    chmod -R g+r+w "$OPT_DIR"
    find "$OPT_DIR" -type d | xargs -n 1 chmod g+s
else
    echo "⚠️ Group 'oryx' does not exist, skipping group-related permission setup for $OPT_DIR"
fi

# Customize secure_path for sudo
SECURE_PATH="${DOTNET_PATH}:${NODE_PATH}/bin:${PHP_PATH}/bin:${PYTHON_PATH}/bin:${JAVA_PATH}/bin:${RUBY_PATH}/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/bin:/usr/local/share:${HOME_DIR}/.local/bin:${PATH}"
echo "Defaults secure_path=\"$SECURE_PATH\"" >> "${SUDOERS_DIR}/${USERNAME}"

echo "✅ Dev container user setup complete!"
