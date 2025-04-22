# Refs:
# - https://www.tug.org/texlive/doc/install-tl.html#PROFILES
# - https://github.com/xu-cheng/latex-docker/blob/master/texlive.profile

# Installation scheme
selected_scheme scheme-full


# Path options
# ============
# System installation paths
TEXDIR         /usr/local/texlive
TEXMFLOCAL     /usr/local/texlive/texmf
TEXMFSYSCONFIG /usr/local/texlive/texmf-config
TEXMFSYSVAR    /usr/local/texlive/texmf-var
# User installation paths
TEXMFHOME      ~/texlive/texmf
TEXMFCONFIG    ~/texlive/texmf-config
TEXMFVAR       ~/texlive/texmf-var


# Installer options
# =================
instopt_adjustpath 0
instopt_adjustrepo 1
instopt_letter 0
instopt_portable 0
instopt_write18_restricted 1


# tlpdb options
# =============
# Number of backups to keep (default: 1)
tlpdbopt_autobackup 0
# Directory for backups (default: tlpkg/backups)
tlpdbopt_backupdir tlpkg/backups
# Generate formats at installation or update (default: 1)
tlpdbopt_create_formats 1
# (Windows) Create Start menu shortcuts (default: 1)
tlpdbopt_desktop_integration 1
# (Windows) Change file associations (default: 1)
tlpdbopt_file_assocs 1
# Run tlmgr generate updmap after maps have changed (default: 0)
tlpdbopt_generate_updmap 0
# Install documentation files (default: 1)
tlpdbopt_install_docfiles 0
# Install source files (default: 1)
tlpdbopt_install_srcfiles 0
# Run postinst code blobs (default: 1)
tlpdbopt_post_code 1
# Destination for symlinks for binaries (default: /usr/local/bin)
tlpdbopt_sys_bin  /usr/local/bin
# Destination for symlinks for info docs (default: /usr/local/share/info)
tlpdbopt_sys_info /usr/local/share/info
# Destination for symlinks for man pages (default: /usr/local/share/man)
tlpdbopt_sys_man  /usr/local/share/man
# (Windows) Install for all users (default: 1)
tlpdbopt_w32_multi_user 1
