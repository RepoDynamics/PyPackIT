#!/usr/bin/env bash
set -euxo pipefail

export DEBIAN_FRONTEND=noninteractive

# Constants
BASHRC_FILEPATH="/etc/bash.bashrc"
ENV_FILEPATH="/etc/environment"
ENV_SCRIPT_FILEPATH="/etc/profile.d/devcontainer-envs.sh"
LOCAL_DIR="/usr/local"
OPT_DIR="/opt"
ORYX_DIR="/opt/oryx"
RESTORE_ENV_FILEPATH="/etc/profile.d/00-restore-env.sh"
SUDOERS_DIR="/etc/sudoers.d"
ZSHRC_FILEPATH="/etc/zsh/zshrc"

LOG_FILE_NAME="install.log"

# Set tool path and environment variables only if source exists.
setup_app() {
    local label="$1"
    local src="$2"
    local src_env_var="${3:-}"
    local dest="${4:-}"
    local dest_env_var="${5:-}"
    local path_mode="${6:-}"
    shift $(( $# > 6 ? 6 : $# ))
    local extra_pairs=("$@")

    if [ -e "$src" ]; then
        echo "✔️ Found $label"
        # Export src_env_var if provided
        if [ -n "$src_env_var" ]; then
            echo "export $src_env_var=\"$src\"" >> "$ENV_SCRIPT_FILEPATH"
            [[ "$src" != *'$'* ]] && echo "$src_env_var=\"$src\"" >> "$ENV_FILEPATH"
            echo "✔️ exported env var $src_env_var"
        fi
        # Create link and export and set path if dest provided
        if [ -n "$dest" ]; then
            mkdir -p "$(dirname "$dest")"
            ln -snf "$src" "$dest"
            echo "✔️ Linked $label from $dest"
            # Export dest_env_var if provided
            if [ -n "$dest_env_var" ]; then
                # remove trailing "/current"
                local export_path="${dest%/current}"
                echo "export $dest_env_var=\"$export_path\"" >> "$ENV_SCRIPT_FILEPATH"
                [[ "$export_path" != *'$'* ]] && echo "$dest_env_var=\"$export_path\"" >> "$ENV_FILEPATH"
                echo "✔️ exported env var $dest_env_var"
            fi
            # Handle path_mode logic
            if [ -n "$path_mode" ]; then
                local path_entry=""
                if [ "$path_mode" = "1" ]; then
                    path_entry="$dest"
                elif [ "$path_mode" = "2" ]; then
                    # make sure the path ends with "/current/bin"
                    if [[ "$dest" == */current ]]; then
                        path_entry="${dest}/bin"
                    else
                        path_entry="${dest}/current/bin"
                    fi
                fi
                if [ -n "$path_entry" ]; then
                    PATH_ENTRIES+=("$path_entry")
                fi
            fi
        fi
        # Process extra var-value pairs
        local i=0
        while [ $i -lt ${#extra_pairs[@]} ]; do
            local val="${extra_pairs[$i]}"
            local var="${extra_pairs[$((i + 1))]}"
            echo "export $var=\"$val\"" >> "$ENV_SCRIPT_FILEPATH"
            [[ "$val" != *'$'* ]] && echo "$var=\"$val\"" >> "$ENV_FILEPATH"
            echo "✔️ exported env var $var"
            i=$((i + 2))
        done
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
rm -f "$RESTORE_ENV_FILEPATH"
echo "export PATH=${PATH//$(sh -lc 'echo $PATH')/\$PATH}" > "$RESTORE_ENV_FILEPATH"
chmod +x "$RESTORE_ENV_FILEPATH"

# Determine the appropriate non-root user
USERNAME="${USERNAME:-"${_REMOTE_USER:-"automatic"}"}"
if [ "$USERNAME" = "automatic" ]; then
    USERNAME=""
    POSSIBLE_USERS=("vscode" "node" "codespace" "$(awk -v val=1000 -F ":" '$3==val{print $1}' /etc/passwd)")
    for CURRENT_USER in "${POSSIBLE_USERS[@]}"; do
        if id -u "$CURRENT_USER" > /dev/null 2>&1; then
            USERNAME="$CURRENT_USER"
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
DEBIAN_FLAVOR="$(get_debian_flavor)"

# Enable the oryx tool to generate manifest-dir which is needed for running the postcreate tool.
# Oryx expects the tool to be installed at `/opt/oryx` and looks for relevant files in there.
mkdir -p "$ORYX_DIR"
echo "vso-focal" > "$ORYX_DIR/.imagetype"
echo "DEBIAN|${DEBIAN_FLAVOR}-SCM" | tr '[a-z]' '[A-Z]' > "$ORYX_DIR/.ostype"
if compgen -G "/usr/local/oryx/*" > /dev/null; then
    ln -snf /usr/local/oryx/* "$ORYX_DIR"
fi

# Create script to write environment variables to source.
{
  echo '#!/usr/bin/env bash'
  echo ''
  echo '# Auto-generated devcontainer env vars set by the setup-user feature.'
} > "$ENV_SCRIPT_FILEPATH"
chmod +x "$ENV_SCRIPT_FILEPATH"

# Tool links
DOTNET_HOME="/usr/share/dotnet"
HUGO_HOME="$LOCAL_DIR/hugo"
JAVA_HOME="$LOCAL_DIR/sdkman/candidates/java"
MAVEN_HOME="$LOCAL_DIR/sdkman/candidates/maven/current"
NVM_HOME="$LOCAL_DIR/share/nvm"
PHP_HOME="$LOCAL_DIR/php/current"
PYTHON_HOME="$LOCAL_DIR/python/current"
PYTHON_HOME_ROOT="$LOCAL_DIR/python"
RVM_HOME="$LOCAL_DIR/rvm"
RUBY_HOME="$RVM_HOME/rubies/default"

DOTNET_PATH="$HOME_DIR/.dotnet"
HUGO_PATH="$HOME_DIR/.hugo/current"
JAVA_PATH="$HOME_DIR/java/current"
MAVEN_PATH="$HOME_DIR/.maven/current"
NODE_PATH="$HOME_DIR/nvm"
NPM_PATH="$HOME_DIR/.npm-global"
NVS_PATH="$HOME_DIR/.nvs"
PHP_PATH="$HOME_DIR/.php/current"
PYTHON_PATH="$HOME_DIR/.python/current"
RUBY_PATH="$HOME_DIR/.ruby/current"

# Accumulate PATH entries here
PATH_ENTRIES=()

#         label         src                 src_env_var  dest            dest_env_var  path_mde  extra_pairs
setup_app ".NET SDK"    "$DOTNET_HOME"      ""           "$DOTNET_PATH"  ""            "1"
setup_app "Hugo"        "$HUGO_HOME"        ""           "$HUGO_PATH"    "HUGO_ROOT"
setup_app "Java"        "$JAVA_HOME"        ""           "$JAVA_PATH"    "JAVA_ROOT"   "2"
setup_app "Maven"       "$MAVEN_HOME"       ""           "$MAVEN_PATH"   "MAVEN_ROOT"
setup_app "Node.js"     "$NVM_HOME"         ""           "$NODE_PATH"    "NODE_ROOT"   "2"       "$NPM_PATH" "NPM_GLOBAL" "$NVS_PATH" "NVS_HOME"
setup_app "PHP"         "$PHP_HOME"         ""           "$PHP_PATH"     "PHP_ROOT"    "2"
setup_app "Python"      "$PYTHON_HOME"      ""           "$PYTHON_PATH"  "PYTHON_ROOT" "2"
setup_app "Python root" "$PYTHON_HOME_ROOT" ""           "/opt/python"
setup_app "RVM"         "$RVM_HOME"         "RVM_PATH"
setup_app "Ruby"        "$RUBY_HOME"        "RUBY_HOME"  "$RUBY_PATH"    "RUBY_ROOT"   "2"

# .NET special setup
# Required due to https://github.com/devcontainers/features/pull/628/files#r1276659825
if [ -d "$DOTNET_HOME" ]; then
    chown -R "$USERNAME:$USERNAME" "$DOTNET_HOME"
    chmod g+r+w+s "$DOTNET_HOME"
    chmod -R g+r+w "$DOTNET_HOME"

    mkdir -p "$OPT_DIR/dotnet/lts"
    cp -R "$DOTNET_HOME/{dotnet,LICENSE.txt,ThirdPartyNotices.txt}" "$OPT_DIR/dotnet/lts" || true
fi

# Create a copy of PATH_ENTRIES for sudo
SUDO_PATH_ENTRIES=("${PATH_ENTRIES[@]}")

# Add standard system directories to sudo path
SUDO_PATH_ENTRIES+=(
    "/usr/local/sbin"
    "/usr/local/bin"
    "/usr/sbin"
    "/usr/bin"
    "/sbin"
    "/bin"
    "/usr/local/share"
)

# Add home bin to both
HOME_BIN="$HOME_DIR/.local/bin"
PATH_ENTRIES+=("$HOME_BIN")
SUDO_PATH_ENTRIES+=("$HOME_BIN")

# Add fallback to PATH for both
PATH_ENTRIES+=("\$PATH")
SUDO_PATH_ENTRIES+=("\$PATH")

# Join PATH entries with colons and write to env script
PATH_JOINED="$(IFS=:; echo "${PATH_ENTRIES[*]}")"
echo "export PATH=\"$PATH_JOINED\"" >> "$ENV_SCRIPT_FILEPATH"

# Join SUDO PATH entries and custmize secure_path for sudo
SUDO_PATH_JOINED="$(IFS=:; echo "${SUDO_PATH_ENTRIES[*]}")"
echo "Defaults secure_path=\"$SUDO_PATH_JOINED\"" >> "${SUDOERS_DIR}/${USERNAME}"

# Source env script in non-login interactive bash shells
touch "$BASHRC_FILEPATH"
if ! grep -qF "$ENV_SCRIPT_FILEPATH" "$BASHRC_FILEPATH"; then
    echo "[ -f $ENV_SCRIPT_FILEPATH ] && source $ENV_SCRIPT_FILEPATH" >> "$BASHRC_FILEPATH"
fi

# Source env script in non-login interactive zsh shells
mkdir -p "$(dirname "$ZSHRC_FILEPATH")"
touch "$ZSHRC_FILEPATH"
if ! grep -qF "$ENV_SCRIPT_FILEPATH" "$ZSHRC_FILEPATH" 2>/dev/null; then
    echo "[ -f $ENV_SCRIPT_FILEPATH ] && source $ENV_SCRIPT_FILEPATH" >> "$ZSHRC_FILEPATH"
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

echo "✅ Dev container user setup complete!"
