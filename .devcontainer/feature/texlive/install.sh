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
add_texlive_bin_to_path() {
  echo "↪️ Function entry: add_texlive_bin_to_path" >&2
  local tlmgr="$(find "$TEXDIR" -name tlmgr)"
  if [[ -n "$tlmgr" ]]; then
      echo "📦 Located tlmgr at '$tlmgr'."
  else
      echo "⛔ tlmgr not found in TEXDIR '$TEXDIR'." >&2
      exit 1
  fi
  echo "🛤 Add TeX Live binaries to system PATH."
  "$tlmgr" path add
  echo "↩️ Function exit: add_texlive_bin_to_path" >&2
}
apply_patches() {
  echo "↪️ Function entry: apply_patches" >&2
  echo "Fixing ConTeXt path in mtxrun.lua"
  (sed -i \
      '/package.loaded\["data-ini"\]/a if os.selfpath then environment.ownbin=lfs.symlinktarget(os.selfpath..io.fileseparator..os.selfname);environment.ownpath=environment.ownbin:match("^.*"..io.fileseparator) else environment.ownpath=kpse.new("luatex"):var_value("SELFAUTOLOC");environment.ownbin=environment.ownpath..io.fileseparator..(arg[-2] or arg[-1] or arg[0] or "luatex"):match("[^"..io.fileseparator.."]*$") end' \
      "$SYS_BIN/mtxrun.lua" || true
  )
  echo "↩️ Function exit: apply_patches" >&2
}
download_texlive_installer() {
  echo "↪️ Function entry: download_texlive_installer" >&2
  echo "📥 Download TeX Live installer from '$MIRROR' to '$INSTALLER_DIR'."
  rsync -a --stats "$MIRROR" "$INSTALLER_DIR"
  echo "↩️ Function exit: download_texlive_installer" >&2
}
exit_if_not_root() {
  echo "↪️ Function entry: exit_if_not_root" >&2
  if [ "$(id -u)" -ne 0 ]; then
      echo '⛔ This script must be run as root. Use sudo, su, or add "USER root" to your Dockerfile before running this script.' >&2
      exit 1
  fi
  echo "↩️ Function exit: exit_if_not_root" >&2
}
generate_caches() {
  echo "↪️ Function entry: generate_caches" >&2
  echo "💾 Generate ConTeXt and font caches."
  (luaotfload-tool -u || true)
  mkdir -p /etc/fonts/conf.d
  (cp "$(find "$TEXDIR" -name texlive-fontconfig.conf)" /etc/fonts/conf.d/09-texlive-fonts.conf || true)
  fc-cache -fsv
  if [ -f "$SYS_BIN/context" ]; then
      mtxrun --generate
      texlua "$SYS_BIN/mtxrun.lua" --luatex --generate
      context --make
      context --luatex --make
  fi
  echo "↩️ Function exit: generate_caches" >&2
}
install_dummy_apt_package() {
  echo "↪️ Function entry: install_dummy_apt_package" >&2
  local equivs_file="${INSTALLER_DIR}/${DEBIAN_EQUIVS_FILENAME}"
  local dummy_version="9999.99999999-1"
  if ! command -v curl >/dev/null 2>&1; then
      echo "⛔ curl is not available." >&2
      exit 1
  fi
  echo "📥 Downloading equivs TeX Live APT package data."
  curl "$DEBIAN_EQUIVS_URL" --output "$equivs_file"
  read pkg_name pkg_version < <(
      awk -F': ' '/^Package:/{pkg=$2} /^Version:/{ver=$2} END{print pkg, ver}' "$equivs_file"
  )
  sed -i "s/${pkg_version}/${dummy_version}/" "$equivs_file"
  echo "📦 Installing equivs TeX Live APT package."
  equivs-build "$equivs_file"
  dpkg -i "${pkg_name}_${dummy_version}_all.deb"
  apt-get install -qyf --no-install-recommends
  if [[ "$NO_CACHE_CLEAN" == false ]]; then
      echo "🧹 Cleaning up APT cache."
      apt-get dist-clean
      rm -rf /var/cache/apt/
  fi
  echo "↩️ Function exit: install_dummy_apt_package" >&2
}
install_requirements() {
  echo "↪️ Function entry: install_requirements" >&2
  if ! command -v "$SYSPKG_INSTALL_SCRIPT" >/dev/null 2>&1; then
      echo "⛔ Package installer script '$SYSPKG_INSTALL_SCRIPT' is not available." >&2
      exit 1
  fi
  echo "📦 Install requirements."
  local script_dir="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"
  local requirements_dir="$script_dir/requirements"
  "$SYSPKG_INSTALL_SCRIPT" \
      --apt "$requirements_dir/apt_pkgs.txt" \
      --logfile "$LOGFILE" \
      --debug \
  echo "↩️ Function exit: install_requirements" >&2
}
install_texlive() {
  echo "↪️ Function entry: install_texlive" >&2
  export TEXLIVE_INSTALL_NO_CONTEXT_CACHE=1
  export NOPERLDOC=1
  if [[ -z "$PROFILE" ]]; then
      echo "📦 Installing TeXLive in interactive mode without a profile."
      "$INSTALLER_DIR/install-tl"
  elif [[ "$INTERACTIVE" == "true" ]]; then
      echo "📦 Installing TeXLive in interactive mode with initial profile '$PROFILE'."
      "$INSTALLER_DIR/install-tl" -init-from-profile "$PROFILE"
  else
      echo "📦 Installing TeXLive in non-interactive mode with profile '$PROFILE'."
      "$INSTALLER_DIR/install-tl" -profile "$PROFILE"
  fi
  echo "↩️ Function exit: install_texlive" >&2
}
set_sysbin() {
  echo "↪️ Function entry: set_sysbin" >&2
  SYS_BIN=$(awk '$1=="tlpdbopt_sys_bin"{sub(/^[^[:space:]]+[[:space:]]+/, ""); print}' "$PROFILE")
  if [[ -z "$SYS_BIN" ]]; then
      echo "🎛 Set tlpdbopt_sys_bin to '$SYS_BIN' from profile file '$PROFILE'."
  else
      SYS_BIN="$DEFAULT_SYS_BIN"
      echo "🎛 Set tlpdbopt_sys_bin to default value '$SYS_BIN'."
  fi
  echo "↩️ Function exit: set_sysbin" >&2
}
set_texdir() {
  echo "↪️ Function entry: set_texdir" >&2
  TEXDIR=$(awk '$1=="TEXDIR"{sub(/^[^[:space:]]+[[:space:]]+/, ""); print}' "$PROFILE")
  if [[ -n "$TEXDIR" ]]; then
      echo "🎛 TEXDIR set to '$TEXDIR' from profile file '$PROFILE'."
  else
      local version=$(find "$INSTALLER_DIR" -maxdepth 1 -type f -regex '.*/LATEX_[0-9]\{4\}' -exec basename {} \; | head -n1 | grep -oP '^LATEX_\K[0-9]{4}')
      if [[ -z "$version" ]]; then
          echo "⛔ No LATEX_YYYY file found in '$INSTALLER_DIR'." >&2
          exit 1
      fi
      TEXDIR="${DEFAULT_TEXDIR_PREFIX}/${version}"
      echo "🎛 TEXDIR set to default value '$TEXDIR'."
  fi
  echo "↩️ Function exit: set_texdir" >&2
}
uninstall_texlive() {
  echo "↪️ Function entry: uninstall_texlive" >&2
  echo "🗑 Uninstall TeX Live."
  tlmgr uninstall --all
  rm -rf "$(kpsewhich -var-value=TEXMFVAR)"
  echo "↩️ Function exit: uninstall_texlive" >&2
}
verify_installation() {
  echo "↪️ Function entry: verify_installation" >&2
  echo "☑️ Verify TeX Live installation."
  latex --version && printf '\n'
  biber --version && printf '\n'
  xindy --version && printf '\n'
  arara --version && printf '\n'
  context --version && printf '\n'
  context --luatex --version && printf '\n'
  asy --version && printf '\n'
  python --version && printf '\n'
  pygmentize -V && printf '\n'
  echo "↩️ Function exit: verify_installation" >&2
}
_LOGFILE_TMP="$(mktemp)"
exec > >(tee -a "$_LOGFILE_TMP") 2>&1
echo "↪️ Script entry: TeX Live Installation Devcontainer Feature Installer" >&2
trap __cleanup__ EXIT
if [ "$#" -gt 0 ]; then
  echo "ℹ️ Script called with arguments: $@" >&2
  DEBIAN_EQUIVS_FILENAME=""
  DEBIAN_EQUIVS_URL=""
  DEBUG=""
  DEFAULT_SYS_BIN=""
  DEFAULT_TEXDIR_PREFIX=""
  GENERATE_CACHES=""
  INSTALL=""
  INSTALLER_DIR=""
  INTERACTIVE=""
  LOGFILE=""
  MIRROR=""
  NO_CACHE_CLEAN=""
  NO_CLEAN=""
  PROFILE=""
  REINSTALL=""
  SYSPKG_INSTALL_SCRIPT=""
  VERIFY_INSTALLATION=""
  while [[ $# -gt 0 ]]; do
    case $1 in
      --debian_equivs_filename) shift; DEBIAN_EQUIVS_FILENAME="$1"; echo "📩 Read argument 'debian_equivs_filename': '"$DEBIAN_EQUIVS_FILENAME"'" >&2; shift;;
      --debian_equivs_url) shift; DEBIAN_EQUIVS_URL="$1"; echo "📩 Read argument 'debian_equivs_url': '"$DEBIAN_EQUIVS_URL"'" >&2; shift;;
      --debug) shift; DEBUG=true; echo "📩 Read argument 'debug': '"$DEBUG"'" >&2;;
      --default_sys_bin) shift; DEFAULT_SYS_BIN="$1"; echo "📩 Read argument 'default_sys_bin': '"$DEFAULT_SYS_BIN"'" >&2; shift;;
      --default_texdir_prefix) shift; DEFAULT_TEXDIR_PREFIX="$1"; echo "📩 Read argument 'default_texdir_prefix': '"$DEFAULT_TEXDIR_PREFIX"'" >&2; shift;;
      --generate_caches) shift; GENERATE_CACHES=true; echo "📩 Read argument 'generate_caches': '"$GENERATE_CACHES"'" >&2;;
      --install) shift; INSTALL=true; echo "📩 Read argument 'install': '"$INSTALL"'" >&2;;
      --installer_dir) shift; INSTALLER_DIR="$1"; echo "📩 Read argument 'installer_dir': '"$INSTALLER_DIR"'" >&2; shift;;
      --interactive) shift; INTERACTIVE=true; echo "📩 Read argument 'interactive': '"$INTERACTIVE"'" >&2;;
      --logfile) shift; LOGFILE="$1"; echo "📩 Read argument 'logfile': '"$LOGFILE"'" >&2; shift;;
      --mirror) shift; MIRROR="$1"; echo "📩 Read argument 'mirror': '"$MIRROR"'" >&2; shift;;
      --no_cache_clean) shift; NO_CACHE_CLEAN=true; echo "📩 Read argument 'no_cache_clean': '"$NO_CACHE_CLEAN"'" >&2;;
      --no_clean) shift; NO_CLEAN=true; echo "📩 Read argument 'no_clean': '"$NO_CLEAN"'" >&2;;
      --profile) shift; PROFILE="$1"; echo "📩 Read argument 'profile': '"$PROFILE"'" >&2; shift;;
      --reinstall) shift; REINSTALL=true; echo "📩 Read argument 'reinstall': '"$REINSTALL"'" >&2;;
      --syspkg_install_script) shift; SYSPKG_INSTALL_SCRIPT="$1"; echo "📩 Read argument 'syspkg_install_script': '"$SYSPKG_INSTALL_SCRIPT"'" >&2; shift;;
      --verify_installation) shift; VERIFY_INSTALLATION=true; echo "📩 Read argument 'verify_installation': '"$VERIFY_INSTALLATION"'" >&2;;
      --*) echo "⛔ Unknown option: "$1"" >&2; exit 1;;
      *) echo "⛔ Unexpected argument: "$1"" >&2; exit 1;;
    esac
  done
else
  echo "ℹ️ Script called with no arguments. Read environment variables." >&2
  [ "${DEBIAN_EQUIVS_FILENAME+defined}" ] && echo "📩 Read argument 'debian_equivs_filename': '"$DEBIAN_EQUIVS_FILENAME"'" >&2
  [ "${DEBIAN_EQUIVS_URL+defined}" ] && echo "📩 Read argument 'debian_equivs_url': '"$DEBIAN_EQUIVS_URL"'" >&2
  [ "${DEBUG+defined}" ] && echo "📩 Read argument 'debug': '"$DEBUG"'" >&2
  [ "${DEFAULT_SYS_BIN+defined}" ] && echo "📩 Read argument 'default_sys_bin': '"$DEFAULT_SYS_BIN"'" >&2
  [ "${DEFAULT_TEXDIR_PREFIX+defined}" ] && echo "📩 Read argument 'default_texdir_prefix': '"$DEFAULT_TEXDIR_PREFIX"'" >&2
  [ "${GENERATE_CACHES+defined}" ] && echo "📩 Read argument 'generate_caches': '"$GENERATE_CACHES"'" >&2
  [ "${INSTALL+defined}" ] && echo "📩 Read argument 'install': '"$INSTALL"'" >&2
  [ "${INSTALLER_DIR+defined}" ] && echo "📩 Read argument 'installer_dir': '"$INSTALLER_DIR"'" >&2
  [ "${INTERACTIVE+defined}" ] && echo "📩 Read argument 'interactive': '"$INTERACTIVE"'" >&2
  [ "${LOGFILE+defined}" ] && echo "📩 Read argument 'logfile': '"$LOGFILE"'" >&2
  [ "${MIRROR+defined}" ] && echo "📩 Read argument 'mirror': '"$MIRROR"'" >&2
  [ "${NO_CACHE_CLEAN+defined}" ] && echo "📩 Read argument 'no_cache_clean': '"$NO_CACHE_CLEAN"'" >&2
  [ "${NO_CLEAN+defined}" ] && echo "📩 Read argument 'no_clean': '"$NO_CLEAN"'" >&2
  [ "${PROFILE+defined}" ] && echo "📩 Read argument 'profile': '"$PROFILE"'" >&2
  [ "${REINSTALL+defined}" ] && echo "📩 Read argument 'reinstall': '"$REINSTALL"'" >&2
  [ "${SYSPKG_INSTALL_SCRIPT+defined}" ] && echo "📩 Read argument 'syspkg_install_script': '"$SYSPKG_INSTALL_SCRIPT"'" >&2
  [ "${VERIFY_INSTALLATION+defined}" ] && echo "📩 Read argument 'verify_installation': '"$VERIFY_INSTALLATION"'" >&2
fi
[[ "$DEBUG" == true ]] && set -x
[ -z "${DEBIAN_EQUIVS_FILENAME-}" ] && { echo "ℹ️ Argument 'DEBIAN_EQUIVS_FILENAME' set to default value 'debian-equivs-2023-ex.txt'." >&2; DEBIAN_EQUIVS_FILENAME="debian-equivs-2023-ex.txt"; }
[ -z "${DEBIAN_EQUIVS_URL-}" ] && { echo "ℹ️ Argument 'DEBIAN_EQUIVS_URL' set to default value 'https://tug.org/texlive/files/{'type': 'string', 'summary': 'Name of the Debian equivs filename to download.', 'default': 'debian-equivs-2023-ex.txt', 'array_delimiter': ' :: '}'." >&2; DEBIAN_EQUIVS_URL="https://tug.org/texlive/files/{'type': 'string', 'summary': 'Name of the Debian equivs filename to download.', 'default': 'debian-equivs-2023-ex.txt', 'array_delimiter': ' :: '}"; }
[ -z "${DEBUG-}" ] && { echo "ℹ️ Argument 'DEBUG' set to default value 'false'." >&2; DEBUG=false; }
[ -z "${DEFAULT_SYS_BIN-}" ] && { echo "ℹ️ Argument 'DEFAULT_SYS_BIN' set to default value '/usr/local/bin'." >&2; DEFAULT_SYS_BIN="/usr/local/bin"; }
[ -z "${DEFAULT_TEXDIR_PREFIX-}" ] && { echo "ℹ️ Argument 'DEFAULT_TEXDIR_PREFIX' set to default value '/usr/local/texlive'." >&2; DEFAULT_TEXDIR_PREFIX="/usr/local/texlive"; }
[ -z "${GENERATE_CACHES-}" ] && { echo "ℹ️ Argument 'GENERATE_CACHES' set to default value 'false'." >&2; GENERATE_CACHES=false; }
[ -z "${INSTALL-}" ] && { echo "ℹ️ Argument 'INSTALL' set to default value 'false'." >&2; INSTALL=false; }
[ -z "${INSTALLER_DIR-}" ] && { echo "ℹ️ Argument 'INSTALLER_DIR' set to default value '/tmp/texlive-installer'." >&2; INSTALLER_DIR="/tmp/texlive-installer"; }
[ -z "${INTERACTIVE-}" ] && { echo "ℹ️ Argument 'INTERACTIVE' set to default value 'false'." >&2; INTERACTIVE=false; }
[ -z "${LOGFILE-}" ] && { echo "ℹ️ Argument 'LOGFILE' set to default value ''." >&2; LOGFILE=""; }
[ -z "${MIRROR-}" ] && { echo "ℹ️ Argument 'MIRROR' set to default value 'rsync://rsync.dante.ctan.org/CTAN/systems/texlive/tlnet/'." >&2; MIRROR="rsync://rsync.dante.ctan.org/CTAN/systems/texlive/tlnet/"; }
[ -z "${NO_CACHE_CLEAN-}" ] && { echo "ℹ️ Argument 'NO_CACHE_CLEAN' set to default value 'false'." >&2; NO_CACHE_CLEAN=false; }
[ -z "${NO_CLEAN-}" ] && { echo "ℹ️ Argument 'NO_CLEAN' set to default value 'false'." >&2; NO_CLEAN=false; }
[ -z "${PROFILE-}" ] && { echo "ℹ️ Argument 'PROFILE' set to default value ''." >&2; PROFILE=""; }
[ -z "${REINSTALL-}" ] && { echo "ℹ️ Argument 'REINSTALL' set to default value 'false'." >&2; REINSTALL=false; }
[ -z "${SYSPKG_INSTALL_SCRIPT-}" ] && { echo "⛔ Missing required argument 'SYSPKG_INSTALL_SCRIPT'." >&2; exit 1; }
[ -z "${VERIFY_INSTALLATION-}" ] && { echo "ℹ️ Argument 'VERIFY_INSTALLATION' set to default value 'false'." >&2; VERIFY_INSTALLATION=false; }
exit_if_not_root
if [[ "$INSTALL" == true || $"REINSTALL" == true ]]; then
    mkdir -p "$INSTALLER_DIR"
    install_requirements
    if command -v tlmgr >/dev/null 2>&1; then
        echo "⚠️ LaTeX installation found."
        if [[ "$REINSTALL" == true ]]; then
            uninstall_texlive
        else
            echo "⛔ LaTeX is already installed."
            exit 1
        fi
    fi
    if command -v apt-get >/dev/null 2>&1; then
        install_dummy_apt_package
    fi
    download_texlive_installer
    install_texlive
    set_texdir
    if [[ "$NO_CLEAN" == false ]]; then
        echo "🗑 Removing installer artifacts."
        rm -rf "$INSTALLER_DIR"
    fi
    set_sysbin
    add_texlive_bin_to_path
    apply_patches
elif [[ "$GENERATE_CACHES" == true ]]; then
    set_texdir
    set_sysbin
fi
if [[ "$GENERATE_CACHES" == true ]]; then
    generate_caches
fi
if [[ "$VERIFY_INSTALLATION" == true ]]; then
    verify_installation
fi
echo "✅ TeX Live installation complete."
echo "↩️ Script exit: TeX Live Installation Devcontainer Feature Installer" >&2
