#!/usr/bin/env bash
set -euo pipefail
__cleanup__() {
  echo "↪️ Function entry: __cleanup__" >&2
  if [[ "$NO_CLEAN" == false ]]; then
      [ -f "$INSTALLER" ] && { echo "🗑 Removing installer script at '$INSTALLER'" >&2; rm -f "$INSTALLER"; }
      [ -f "$CHECKSUM" ] && { echo "🗑 Removing checksum file at '$CHECKSUM'" >&2; rm -f "$CHECKSUM"; }
      [ -d "$INSTALLER_DIR" ] && [ -z "$(ls -A "$INSTALLER_DIR")" ] && {
          echo "🗑 Removing installation directory at '$INSTALLER_DIR'" >&2
          rmdir "$INSTALLER_DIR"
      }
  fi
  find "$CONDA_DIR" -follow -type f -name '*.a' -delete
  find "$CONDA_DIR" -follow -type f -name '*.pyc' -delete
  if [[ "$NO_CACHE_CLEAN" == false ]] && [[ -f "$CONDA_EXEC" ]]; then
      echo "🧹 Cleaning up conda cache."
      "$CONDA_EXEC" clean --all --force-pkgs-dirs --yes
  fi
  if [ -n "${LOGFILE-}" ]; then
    echo "ℹ️ Write logs to file '$LOGFILE'" >&2
    mkdir -p "$(dirname "$LOGFILE")"
    cat "$_LOGFILE_TMP" >> "$LOGFILE"
    rm -f "$_LOGFILE_TMP"
  fi
  echo "↩️ Function exit: __cleanup__" >&2
}
add_activation_to_rcfile() {
  echo "↪️ Function entry: add_activation_to_rcfile" >&2
  local conda_script="$CONDA_DIR/$CONDA_ACTIVATION_SCRIPT_PATH"
  local mamba_script="$CONDA_DIR/$MAMBA_ACTIVATION_SCRIPT_PATH"
  lines=(
      ". '$conda_script'"
      ". '$mamba_script'"
  )
  if [[ -n "$ACTIVE_ENV" ]]; then
      lines+=("conda activate $ACTIVE_ENV")
  fi
  for path in "${ACTIVATES[@]}"; do
      echo "▶️ Sourcing activation script to '$path'"
      [[ -f "$path" ]] || touch "$path"
      for line in "${lines[@]}"; do
          if grep -Fxq "$line" "$path"; then
              echo "⏭️ Line already exists in '$path': $line"
          else
              echo "$line" >> "$path"
              echo "ℹ️ Appended to '$path': $line"
          fi
      done
  done
  echo "↩️ Function exit: add_activation_to_rcfile" >&2
}
download_miniforge() {
  echo "↪️ Function entry: download_miniforge" >&2
  local installer_url
  local checksum_url
  if [[ "$MINIFORGE_VERSION" == "latest" ]]; then
      installer_url="https://github.com/conda-forge/miniforge/releases/latest/download/${INSTALLER_FILENAME}"
      checksum_url=""  # TODO: Find a way to get the checksum URL for the latest version.
  else
      installer_url="https://github.com/conda-forge/miniforge/releases/download/${MINIFORGE_VERSION}/${INSTALLER_FILENAME}"
      checksum_url="$installer_url.sha256"
  fi
  mkdir -p "$INSTALLER_DIR"
  if command -v wget >/dev/null 2>&1; then
      echo "📥 Downloading installer using wget from $installer_url" >&2
      wget --no-hsts --tries 3 --output-document "$INSTALLER" "$installer_url"
      if [[ -n "$checksum_url" ]]; then
          wget --no-hsts --tries 3 --output-document "$CHECKSUM" "$checksum_url"
      fi
  elif command -v curl >/dev/null 2>&1; then
      echo "📥 Downloading installer using curl from $installer_url" >&2
      curl --fail --location --retry 3 --output "$INSTALLER" "$installer_url"
      if [[ -n "$checksum_url" ]]; then
          curl --fail --location --retry 3 --output "$CHECKSUM" "$checksum_url"
      fi
  else
      echo "⛔ Neither wget nor curl is available." >&2
      exit 1
  fi
  if [[ -n "$checksum_url" ]]; then
      verify_miniforge
  fi
  echo "↩️ Function exit: download_miniforge" >&2
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
install_miniforge() {
  echo "↪️ Function entry: install_miniforge" >&2
  echo "📦 Installing Miniforge to $CONDA_DIR"
  if [[ "$INTERACTIVE" == true ]]; then
      /bin/bash "$INSTALLER" -p "$CONDA_DIR"
  else
      /bin/bash "$INSTALLER" -b -p "$CONDA_DIR"
  fi
  echo "Displaying conda info:"
  "$CONDA_EXEC" info
  echo "Displaying conda config:"
  "$CONDA_EXEC" config --show
  echo "Displaying conda env list:"
  "$CONDA_EXEC" env list
  echo "Displaying conda list:"
  "$CONDA_EXEC" list --name base
  __cleanup__
  echo "↩️ Function exit: install_miniforge" >&2
}
set_executable_paths() {
  echo "↪️ Function entry: set_executable_paths" >&2
  local verify=""
  while [[ $# -gt 0 ]]; do
    case $1 in
      --verify) shift; verify=true; echo "📩 Read argument 'verify': '"$verify"'" >&2;;
      --*) echo "⛔ Unknown option: "$1"" >&2; exit 1;;
      *) echo "⛔ Unexpected argument: "$1"" >&2; exit 1;;
    esac
  done
  CONDA_EXEC="${CONDA_DIR}/bin/conda"
  MAMBA_EXEC="${CONDA_DIR}/bin/mamba"
  if [ "${1:-}" != "verify" ]; then
      return
  fi
  if [[ ! -f "$CONDA_EXEC" ]]; then
      if command -v conda >/dev/null 2>&1; then
          CONDA_DIR="$(conda info --base)"
          CONDA_EXEC="${CONDA_DIR}/bin/conda"
      else
          echo "⛔ Conda executable not found at '$CONDA_EXEC'." >&2
          exit 1
      fi
  fi
  if [[ ! -f "$MAMBA_EXEC" ]]; then
      if command -v mamba >/dev/null 2>&1; then
          MAMBA_EXEC="$(mamba info --base | tail -n 2 | head -n 1)/bin/mamba"
      else
          echo "⛔ Mamba executable not found at '$MAMBA_EXEC'." >&2
          exit 1
      fi
  fi
  if [[ ! -f "$CONDA_EXEC" ]]; then
      echo "⛔ Conda executable not found." >&2
      exit 1
  fi
  if [[ ! -f "$MAMBA_EXEC" ]]; then
      echo "⛔ Mamba executable not found." >&2
      exit 1
  fi
  echo "🎛 Conda executable located at '$CONDA_EXEC'."
  echo "🎛 Mamba executable located at '$MAMBA_EXEC'."
  echo "↩️ Function exit: set_executable_paths" >&2
}
set_installer_filename() {
  echo "↪️ Function entry: set_installer_filename" >&2
  local installer_platform="$(uname)-$(uname -m)"
  if [[ "$MINIFORGE_VERSION" == "latest" ]]; then
      INSTALLER_FILENAME="${MINIFORGE_NAME}-${installer_platform}.sh"
  else
      INSTALLER_FILENAME="${MINIFORGE_NAME}-${MINIFORGE_VERSION}-${installer_platform}.sh"
  fi
  INSTALLER="${INSTALLER_DIR}/${INSTALLER_FILENAME}"
  CHECKSUM="${INSTALLER}.sha256"
  echo "↩️ Function exit: set_installer_filename" >&2
}
set_permission() {
  echo "↪️ Function entry: set_permission" >&2
  echo "🔐 Setting permissions for conda directory."
  getent group "$GROUP" >/dev/null || groupadd -r "$GROUP"
  id -nG "$USER" | grep -qw "$GROUP" || usermod -a -G "$GROUP" "$USER"
  chown -R "$USER:$GROUP" "$CONDA_DIR"
  chmod -R g+r+w "$CONDA_DIR"
  find "$CONDA_DIR" -type d -print0 | xargs -n 1 -0 chmod g+s
  echo "↩️ Function exit: set_permission" >&2
}
setup_environment() {
  echo "↪️ Function entry: setup_environment" >&2
  umask 0002
  for env_file in "${ENV_FILES[@]}"; do
      echo "📦 Installing conda environment from '$env_file'."
      "$MAMBA_EXEC" env update --file "$env_file"
  done
  for env_dir in "${ENV_DIRS[@]}"; do
      find "$env_dir" -type f \( -name "*.yml" -o -name "*.yaml" \) | while IFS= read -r env_file; do
          echo "📦 Installing conda environment from '$env_file'."
          "$MAMBA_EXEC" env update --file "$env_file"
      done
  done
  if [[ "$NO_CACHE_CLEAN" == false ]]; then
      echo "🧹 Cleaning up conda cache."
      "$MAMBA_EXEC" clean --all -y
  fi
  echo "↩️ Function exit: setup_environment" >&2
}
uninstall_miniforge() {
  echo "↪️ Function entry: uninstall_miniforge" >&2
  echo "🗑 Uninstalling conda (Miniforge)."
  "$CONDA_EXEC" init --reverse
  rm -rf "$("$CONDA_EXEC" info --base)"
  rm -f "$HOME/.condarc"
  rm -rf "$HOME/.conda"
  user_home=$(getent passwd "$USER" | cut -d: -f6)
  rm -rf "$user_home/.condarc"
  rm -rf "$user_home/.conda"
  echo "↩️ Function exit: uninstall_miniforge" >&2
}
verify_miniforge() {
  echo "↪️ Function entry: verify_miniforge" >&2
  echo "📦 Verifying installer checksum"
  if command -v sha256sum >/dev/null 2>&1; then
      if (cd "$INSTALLER_DIR" && sha256sum --check --status "$CHECKSUM"); then
          echo "✅ Checksum verification passed" >&2
      else
          echo "❌ Checksum verification failed" >&2
          exit 1
      fi
  elif command -v shasum >/dev/null 2>&1; then
      if (cd "$INSTALLER_DIR" && shasum --algorithm 256 --check --status "$CHECKSUM"); then
          echo "✅ Checksum verification passed" >&2
      else
          echo "❌ Checksum verification failed" >&2
          exit 1
      fi
  else
      echo "⛔ Neither sha256sum nor shasum is available." >&2
      exit 1
  fi
  echo "↩️ Function exit: verify_miniforge" >&2
}
_LOGFILE_TMP="$(mktemp)"
exec > >(tee -a "$_LOGFILE_TMP") 2>&1
echo "↪️ Script entry: Miniforge Installation Devcontainer Feature Installer" >&2
trap __cleanup__ EXIT
if [ "$#" -gt 0 ]; then
  echo "ℹ️ Script called with arguments: $@" >&2
  ACTIVATES=()
  ACTIVE_ENV=""
  CONDA_ACTIVATION_SCRIPT_PATH=""
  CONDA_DIR=""
  DEBUG=""
  DOWNLOAD=""
  ENV_DIRS=()
  ENV_FILES=()
  GROUP=""
  INSTALL=""
  INSTALLER_DIR=""
  INTERACTIVE=""
  LOGFILE=""
  MAMBA_ACTIVATION_SCRIPT_PATH=""
  MINIFORGE_NAME=""
  MINIFORGE_VERSION=""
  NO_CACHE_CLEAN=""
  NO_CLEAN=""
  REINSTALL=""
  SET_PERMISSION=""
  UPDATE_BASE=""
  USER=""
  while [[ $# -gt 0 ]]; do
    case $1 in
      --activates) shift; while [[ $# -gt 0 && ! "$1" =~ ^-- ]]; do ACTIVATES+=("$1"); echo "📩 Read argument 'activates': '"$1"'" >&2; shift; done;;
      --active_env) shift; ACTIVE_ENV="$1"; echo "📩 Read argument 'active_env': '"$ACTIVE_ENV"'" >&2; shift;;
      --conda_activation_script_path) shift; CONDA_ACTIVATION_SCRIPT_PATH="$1"; echo "📩 Read argument 'conda_activation_script_path': '"$CONDA_ACTIVATION_SCRIPT_PATH"'" >&2; shift;;
      --conda_dir) shift; CONDA_DIR="$1"; echo "📩 Read argument 'conda_dir': '"$CONDA_DIR"'" >&2; shift;;
      --debug) shift; DEBUG=true; echo "📩 Read argument 'debug': '"$DEBUG"'" >&2;;
      --download) shift; DOWNLOAD=true; echo "📩 Read argument 'download': '"$DOWNLOAD"'" >&2;;
      --env_dirs) shift; while [[ $# -gt 0 && ! "$1" =~ ^-- ]]; do ENV_DIRS+=("$1"); echo "📩 Read argument 'env_dirs': '"$1"'" >&2; shift; done;;
      --env_files) shift; while [[ $# -gt 0 && ! "$1" =~ ^-- ]]; do ENV_FILES+=("$1"); echo "📩 Read argument 'env_files': '"$1"'" >&2; shift; done;;
      --group) shift; GROUP="$1"; echo "📩 Read argument 'group': '"$GROUP"'" >&2; shift;;
      --install) shift; INSTALL=true; echo "📩 Read argument 'install': '"$INSTALL"'" >&2;;
      --installer_dir) shift; INSTALLER_DIR="$1"; echo "📩 Read argument 'installer_dir': '"$INSTALLER_DIR"'" >&2; shift;;
      --interactive) shift; INTERACTIVE=true; echo "📩 Read argument 'interactive': '"$INTERACTIVE"'" >&2;;
      --logfile) shift; LOGFILE="$1"; echo "📩 Read argument 'logfile': '"$LOGFILE"'" >&2; shift;;
      --mamba_activation_script_path) shift; MAMBA_ACTIVATION_SCRIPT_PATH="$1"; echo "📩 Read argument 'mamba_activation_script_path': '"$MAMBA_ACTIVATION_SCRIPT_PATH"'" >&2; shift;;
      --miniforge_name) shift; MINIFORGE_NAME="$1"; echo "📩 Read argument 'miniforge_name': '"$MINIFORGE_NAME"'" >&2; shift;;
      --miniforge_version) shift; MINIFORGE_VERSION="$1"; echo "📩 Read argument 'miniforge_version': '"$MINIFORGE_VERSION"'" >&2; shift;;
      --no_cache_clean) shift; NO_CACHE_CLEAN=true; echo "📩 Read argument 'no_cache_clean': '"$NO_CACHE_CLEAN"'" >&2;;
      --no_clean) shift; NO_CLEAN=true; echo "📩 Read argument 'no_clean': '"$NO_CLEAN"'" >&2;;
      --reinstall) shift; REINSTALL=true; echo "📩 Read argument 'reinstall': '"$REINSTALL"'" >&2;;
      --set_permission) shift; SET_PERMISSION=true; echo "📩 Read argument 'set_permission': '"$SET_PERMISSION"'" >&2;;
      --update_base) shift; UPDATE_BASE=true; echo "📩 Read argument 'update_base': '"$UPDATE_BASE"'" >&2;;
      --user) shift; USER="$1"; echo "📩 Read argument 'user': '"$USER"'" >&2; shift;;
      --*) echo "⛔ Unknown option: "$1"" >&2; exit 1;;
      *) echo "⛔ Unexpected argument: "$1"" >&2; exit 1;;
    esac
  done
else
  echo "ℹ️ Script called with no arguments. Read environment variables." >&2
  if [ "${ACTIVATES+defined}" ]; then
    echo "ℹ️ Parse 'activates' into array: '$ACTIVATES'" >&2
    IFS=" :: " read -r -a _tmp_array <<< "$ACTIVATES"
    ACTIVATES=("${_tmp_array[@]}")
    for _item in "${ACTIVATES[@]}"; do
      echo "📩 Read argument 'activates': '"$_item"'" >&2
    done
    unset _item
    unset _tmp_array
  fi
  [ "${ACTIVE_ENV+defined}" ] && echo "📩 Read argument 'active_env': '"$ACTIVE_ENV"'" >&2
  [ "${CONDA_ACTIVATION_SCRIPT_PATH+defined}" ] && echo "📩 Read argument 'conda_activation_script_path': '"$CONDA_ACTIVATION_SCRIPT_PATH"'" >&2
  [ "${CONDA_DIR+defined}" ] && echo "📩 Read argument 'conda_dir': '"$CONDA_DIR"'" >&2
  [ "${DEBUG+defined}" ] && echo "📩 Read argument 'debug': '"$DEBUG"'" >&2
  [ "${DOWNLOAD+defined}" ] && echo "📩 Read argument 'download': '"$DOWNLOAD"'" >&2
  if [ "${ENV_DIRS+defined}" ]; then
    echo "ℹ️ Parse 'env_dirs' into array: '$ENV_DIRS'" >&2
    IFS=" :: " read -r -a _tmp_array <<< "$ENV_DIRS"
    ENV_DIRS=("${_tmp_array[@]}")
    for _item in "${ENV_DIRS[@]}"; do
      echo "📩 Read argument 'env_dirs': '"$_item"'" >&2
    done
    unset _item
    unset _tmp_array
  fi
  if [ "${ENV_FILES+defined}" ]; then
    echo "ℹ️ Parse 'env_files' into array: '$ENV_FILES'" >&2
    IFS=" :: " read -r -a _tmp_array <<< "$ENV_FILES"
    ENV_FILES=("${_tmp_array[@]}")
    for _item in "${ENV_FILES[@]}"; do
      echo "📩 Read argument 'env_files': '"$_item"'" >&2
    done
    unset _item
    unset _tmp_array
  fi
  [ "${GROUP+defined}" ] && echo "📩 Read argument 'group': '"$GROUP"'" >&2
  [ "${INSTALL+defined}" ] && echo "📩 Read argument 'install': '"$INSTALL"'" >&2
  [ "${INSTALLER_DIR+defined}" ] && echo "📩 Read argument 'installer_dir': '"$INSTALLER_DIR"'" >&2
  [ "${INTERACTIVE+defined}" ] && echo "📩 Read argument 'interactive': '"$INTERACTIVE"'" >&2
  [ "${LOGFILE+defined}" ] && echo "📩 Read argument 'logfile': '"$LOGFILE"'" >&2
  [ "${MAMBA_ACTIVATION_SCRIPT_PATH+defined}" ] && echo "📩 Read argument 'mamba_activation_script_path': '"$MAMBA_ACTIVATION_SCRIPT_PATH"'" >&2
  [ "${MINIFORGE_NAME+defined}" ] && echo "📩 Read argument 'miniforge_name': '"$MINIFORGE_NAME"'" >&2
  [ "${MINIFORGE_VERSION+defined}" ] && echo "📩 Read argument 'miniforge_version': '"$MINIFORGE_VERSION"'" >&2
  [ "${NO_CACHE_CLEAN+defined}" ] && echo "📩 Read argument 'no_cache_clean': '"$NO_CACHE_CLEAN"'" >&2
  [ "${NO_CLEAN+defined}" ] && echo "📩 Read argument 'no_clean': '"$NO_CLEAN"'" >&2
  [ "${REINSTALL+defined}" ] && echo "📩 Read argument 'reinstall': '"$REINSTALL"'" >&2
  [ "${SET_PERMISSION+defined}" ] && echo "📩 Read argument 'set_permission': '"$SET_PERMISSION"'" >&2
  [ "${UPDATE_BASE+defined}" ] && echo "📩 Read argument 'update_base': '"$UPDATE_BASE"'" >&2
  [ "${USER+defined}" ] && echo "📩 Read argument 'user': '"$USER"'" >&2
fi
[[ "$DEBUG" == true ]] && set -x
{ [ "${ACTIVATES+isset}" != "isset" ] || [ ${#ACTIVATES[@]} -eq 0 ] } && { echo "ℹ️ Argument 'ACTIVATES' set to default value '()'." >&2; ACTIVATES=(); }
[ -z "${ACTIVE_ENV-}" ] && { echo "ℹ️ Argument 'ACTIVE_ENV' set to default value 'base'." >&2; ACTIVE_ENV="base"; }
[ -z "${CONDA_ACTIVATION_SCRIPT_PATH-}" ] && { echo "ℹ️ Argument 'CONDA_ACTIVATION_SCRIPT_PATH' set to default value 'etc/profile.d/conda.sh'." >&2; CONDA_ACTIVATION_SCRIPT_PATH="etc/profile.d/conda.sh"; }
[ -z "${CONDA_DIR-}" ] && { echo "ℹ️ Argument 'CONDA_DIR' set to default value '/opt/conda'." >&2; CONDA_DIR="/opt/conda"; }
{ [ "${ENV_DIRS+isset}" != "isset" ] || [ ${#ENV_DIRS[@]} -eq 0 ] } && { echo "ℹ️ Argument 'ENV_DIRS' set to default value '()'." >&2; ENV_DIRS=(); }
for elem in "${ENV_DIRS[@]}"; do
  [ -n ${ENV_DIRS-} ] && [ ! -d "$ENV_DIRS" ] && { echo "⛔ Directory argument to parameter 'ENV_DIRS' not found: '$ENV_DIRS'" >&2; exit 1; }
done
{ [ "${ENV_FILES+isset}" != "isset" ] || [ ${#ENV_FILES[@]} -eq 0 ] } && { echo "ℹ️ Argument 'ENV_FILES' set to default value '()'." >&2; ENV_FILES=(); }
for elem in "${ENV_FILES[@]}"; do
  [ -n ${ENV_FILES-} ] && [ ! -f "$ENV_FILES" ] && { echo "⛔ File argument to parameter 'ENV_FILES' not found: '$ENV_FILES'" >&2; exit 1; }
done
[ -z "${GROUP-}" ] && { echo "ℹ️ Argument 'GROUP' set to default value 'conda'." >&2; GROUP="conda"; }
[ -z "${INSTALLER_DIR-}" ] && { echo "ℹ️ Argument 'INSTALLER_DIR' set to default value '/tmp/miniforge-installer'." >&2; INSTALLER_DIR="/tmp/miniforge-installer"; }
[ -z "${LOGFILE-}" ] && { echo "ℹ️ Argument 'LOGFILE' set to default value ''." >&2; LOGFILE=""; }
[ -z "${MAMBA_ACTIVATION_SCRIPT_PATH-}" ] && { echo "ℹ️ Argument 'MAMBA_ACTIVATION_SCRIPT_PATH' set to default value 'etc/profile.d/mamba.sh'." >&2; MAMBA_ACTIVATION_SCRIPT_PATH="etc/profile.d/mamba.sh"; }
[ -z "${MINIFORGE_NAME-}" ] && { echo "ℹ️ Argument 'MINIFORGE_NAME' set to default value 'Miniforge3'." >&2; MINIFORGE_NAME="Miniforge3"; }
[ -z "${MINIFORGE_VERSION-}" ] && { echo "⛔ Missing required argument 'MINIFORGE_VERSION'." >&2; exit 1; }
[ -z "${USER-}" ] && { echo "ℹ️ Argument 'USER' set to default value ''." >&2; USER=""; }
exit_if_not_root
set_executable_paths
if [[ "$DOWNLOAD" == true || "$INSTALL" == true || "$REINSTALL" == true ]]; then
    set_installer_filename
fi
if [[ "$DOWNLOAD" == true ]]; then download_miniforge; fi
if [[ "$DOWNLOAD" == true || "$INSTALL" == true || "$REINSTALL" == true ]]; then
    if [[ -f "$CHECKSUM" ]]; then
        verify_miniforge
    else
        echo "⚠️ Checksum file not found. Skipping verification." >&2
    fi
fi
if [[ "$INSTALL" == true || "$REINSTALL" == true ]]; then
    if command -v conda >/dev/null 2>&1; then
        echo "⚠️ Conda installation found."
        if [[ "$REINSTALL" != true ]]; then
            echo "⏩ Conda is already available."
        else
            uninstall_miniforge
            install_miniforge
        fi
    else
        install_miniforge
    fi
fi
set_executable_paths --verify
if [[ ${#ACTIVATES[@]} -gt 0 ]]; then add_activation_to_rcfile; fi
if [[ "$UPDATE_BASE" == true ]]; then
    echo "⚠️ Updating base conda environment."
    "$MAMBA_EXEC" update -n base --all -y
fi
if [[ ${#ENV_FILES[@]} -gt 0 || ${#ENV_DIRS[@]} -gt 0 ]]; then setup_environments; fi
if [[ "$SET_PERMISSION" == true ]]; then set_permission; fi
echo "✅ Conda installation complete."
echo "↩️ Script exit: Miniforge Installation Devcontainer Feature Installer" >&2
