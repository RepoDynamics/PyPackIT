FROM ubuntu:noble

ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONIOENCODING=UTF-8 \
    TZ=UTC
USER root

ARG SYSPKG_INSTALL_SCRIPT="/usr/local/share/pypackit/.devcontainer/feature/syspkg/install.sh"
COPY [".devcontainer/feature/syspkg/install.sh", "$SYSPKG_INSTALL_SCRIPT"]
RUN chmod +x "$SYSPKG_INSTALL_SCRIPT"

ARG SYSPKGS_ESSENTIAL="/usr/local/share/pypackit/.devcontainer/environment/syspkg/essential"
COPY [".devcontainer/environment/syspkg/essential/", "$SYSPKGS_ESSENTIAL/"]
RUN "$SYSPKG_INSTALL_SCRIPT" \
        --apt "$SYSPKGS_ESSENTIAL/apt_pkgs.txt" \
        --logfile "/var/log/pypackit-container/apt_install_essential.log" \
        --debug

ARG TEXLIVE_INSTALL_SCRIPT_DIR="/usr/local/share/pypackit/.devcontainer/feature/texlive"
ARG TEXLIVE_INSTALL_SCRIPT="${TEXLIVE_INSTALL_SCRIPT_DIR}/install.sh" \
    TEXLIVE_INSTALL_PROFILE="${TEXLIVE_INSTALL_SCRIPT_DIR}/install.profile"
COPY [".devcontainer/environment/texlive/", "${TEXLIVE_INSTALL_SCRIPT_DIR}/"]
RUN chmod +x "$TEXLIVE_INSTALL_SCRIPT"; \
    "$TEXLIVE_INSTALL_SCRIPT" \
        --install \
        --profile "$TEXLIVE_INSTALL_PROFILE" \
        --logfile "/var/log/pypackit-container/texlive_install.log" \
        --debug

ARG GIT_INSTALL_SCRIPT_DIR="/usr/local/share/pypackit/.devcontainer/feature/git"
ARG GIT_INSTALL_SCRIPT="$GIT_INSTALL_SCRIPT_DIR/install.sh"
COPY [".devcontainer/feature/git/", "$GIT_INSTALL_SCRIPT_DIR/"]
ENV PATH=/usr/local/git/bin:$PATH
RUN chmod +x "$GIT_INSTALL_SCRIPT"; \
    "$GIT_INSTALL_SCRIPT" \
        --version "2.49.0" \
        --prefix "/usr/local/git" \
        --logfile "/var/log/pypackit/git_install.log" \
        --debug

ENV CONDA_DIR=/opt/conda
ENV PATH=$CONDA_DIR/bin:$PATH
ARG MINIFORGE_INSTALL_SCRIPT="/usr/local/share/pypackit/.devcontainer/feature/miniforge/install.sh"
COPY [".devcontainer/feature/miniforge/install.sh", "$MINIFORGE_INSTALL_SCRIPT"]
RUN chmod +x "$MINIFORGE_INSTALL_SCRIPT"; \
    "$MINIFORGE_INSTALL_SCRIPT" \
        --download \
        --install \
        --miniforge-name "Miniforge3" \
        --miniforge-version "24.11.3-2" \
        --conda-dir "$CONDA_DIR" \
        --logfile "/tmp/log/pypackit/miniforge_install.log" \
        --debug

ARG SYSPKGS_RECOMMENDED="/usr/local/share/pypackit/.devcontainer/environment/syspkg/recommended"
COPY [".devcontainer/environment/syspkg/recommended/", "$SYSPKGS_RECOMMENDED/"]
RUN "$SYSPKG_INSTALL_SCRIPT" \
        --apt "$SYSPKGS_RECOMMENDED/apt_pkgs.txt" \
        --logfile "/var/log/pypackit-container/apt_install_recommended.log" \
        --debug

ARG OH_MY_ZSH_INSTALL_SCRIPT_DIR="/usr/local/share/pypackit/.devcontainer/feature/oh-my-zsh"
ARG OH_MY_ZSH_INSTALL_SCRIPT="$OH_MY_ZSH_INSTALL_SCRIPT_DIR/install.sh"
COPY [".devcontainer/feature/oh-my-zsh/", "$OH_MY_ZSH_INSTALL_SCRIPT_DIR/"]
ARG OH_MY_ZSH_INSTALL_DIR="/usr/local/oh-my-zsh"
RUN chmod +x "$OH_MY_ZSH_INSTALL_SCRIPT"; \
    "$OH_MY_ZSH_INSTALL_SCRIPT" \
        --install-dir "$OH_MY_ZSH_INSTALL_DIR" \
        --logfile "/var/log/pypackit/oh-my-zsh_install.log" \
        --debug

ARG USER_DELETE_SCRIPT="/usr/local/share/pypackit/.devcontainer/feature/user/delete.sh"
COPY [".devcontainer/feature/user/delete.sh", "$USER_DELETE_SCRIPT"]
RUN set -eux; \
    chmod +x "$USER_DELETE_SCRIPT"; \
    "$USER_DELETE_SCRIPT" --gid "1000" --uid "1000" --logfile "/var/log/pypackit/user_delete.log";

ARG USERNAME="pypackit-dev" \
    USER_HOME="/home/pypackit-dev" \
    USER_GID="1000" \
    USER_UID="1000" \
    USER_SHELL="/bin/bash" \
    SUDOERS_DIR="/etc/sudoers.d"
RUN set -eux; \
    groupadd --gid "$USER_GID" "$USERNAME"; \
    useradd \
        --create-home \
        --home-dir "$USER_HOME" \
        --gid "$USER_GID" \
        --shell "$USER_SHELL" \
        --uid "$USER_UID" \
        "$USERNAME"; \
    mkdir -p "$SUDOERS_DIR"; \
    echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" | tee "$SUDOERS_DIR/$USERNAME" > /dev/null; \
    chmod 0440 "$SUDOERS_DIR/$USERNAME";

# RUN chmod +x "$TEXLIVE_INSTALL_SCRIPT"; \
# "$TEXLIVE_INSTALL_SCRIPT" \
#     --generate-caches \
#     --verify-installation \
#     --profile "$TEXLIVE_INSTALL_PROFILE" \
#     --logfile "/var/log/pypackit-container/texlive_finalize.log" \
#     --debug

ARG CONDA_ENVS_DIR="/usr/local/share/pypackit/.devcontainer/environment/conda/"
COPY [".devcontainer/environment/conda/", "$CONDA_ENVS_DIR"]
RUN "$MINIFORGE_INSTALL_SCRIPT" \
        --envdir "$CONDA_ENVS_DIR" \
        --set-permission \
        --group "pypackit-dev" \
        --user "pypackit-dev" \
        --logfile "/var/log/pypackit-container/conda_envs_install.log" \
        --debug

# https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ARG PIXI_VERSION="0.46.0"
RUN set -eux; \
    curl -L -o "/usr/local/bin/pixi" -fsSL --compressed "https://github.com/prefix-dev/pixi/releases/download/v${PIXI_VERSION}/pixi-$(uname -m)-unknown-linux-musl"; \
    chmod +x /usr/local/bin/pixi; \
    pixi info

ARG PKG_INSTALL_SCRIPT_DIR="/usr/local/share/pypackit/.devcontainer/environment/pkg"
COPY ["install.py", ".github/.repodynamics/metadata.json", "$PKG_INSTALL_SCRIPT_DIR/"]
RUN set eux; \
    chmod +x "$PKG_INSTALL_SCRIPT_DIR/install.py"; \
    python3 "$PKG_INSTALL_SCRIPT_DIR/install.py" \
        --conda-env-name "website" \
        --packages '["ci"]' \
        --python-version "3.13" \
        --sources "conda" "pip" "apt" "bash" \
        --filepath "$PKG_INSTALL_SCRIPT_DIR/metadata.json" \
        --no-self; \
    conda clean --all -y

ARG VOLUME_DATA="/usr/local/share/pypackit/.devcontainer/volume/" \
    VOLUME_SETUP_SCRIPT="/usr/local/share/pypackit/.devcontainer/feature/volume/install.sh" \
    VOLUME_MANIFEST="/usr/local/share/pypackit/.devcontainer/environment/volume_manifest"
COPY [".devcontainer/feature/volume/install.sh", "$VOLUME_SETUP_SCRIPT"]
COPY [".devcontainer/environment/volume_manifest", "$VOLUME_MANIFEST"]
COPY ["./.devcontainer/volume/", "$VOLUME_DATA"]
RUN set -eux; \
    chmod +x "$VOLUME_SETUP_SCRIPT"; \
    "$VOLUME_SETUP_SCRIPT" "$VOLUME_DATA" --manifest "$VOLUME_MANIFEST" --action "write" --logfile "/var/log/pypackit/volume_setup.log";
