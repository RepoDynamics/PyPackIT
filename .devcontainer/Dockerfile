FROM ubuntu:noble

ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONIOENCODING=UTF-8 \
    TZ=UTC
USER root

ARG APT_INSTALL_SCRIPT="/usr/local/share/pypackit-container/.devcontainer/environment/apt/install.sh"
COPY [".devcontainer/environment/apt/install.sh", "$APT_INSTALL_SCRIPT"]
RUN chmod +x "$APT_INSTALL_SCRIPT"

ARG APT_REQUIRED_PACKAGES="/usr/local/share/pypackit-container/.devcontainer/environment/apt/required/packages.txt"
COPY [".devcontainer/environment/apt/required/packages.txt", "$APT_REQUIRED_PACKAGES"]
RUN "$APT_INSTALL_SCRIPT" "APT_REQUIRED_PACKAGES" --logfile /var/log/pypackit-container/apt_install_required.log
ARG APT_REQUIRED_POST_INSTALL="/usr/local/share/pypackit-container/.devcontainer/environment/apt/required/post_install.sh"
COPY [".devcontainer/environment/apt/required/post_install.sh", "$APT_REQUIRED_POST_INSTALL"]
RUN chmod +x $APT_REQUIRED_POST_INSTALL; \
    $APT_REQUIRED_POST_INSTALL

ARG APT_ESSENTIAL_PACKAGES="/usr/local/share/pypackit-container/.devcontainer/environment/apt/essential/packages.txt"
COPY [".devcontainer/environment/apt/essential/packages.txt", "$APT_ESSENTIAL_PACKAGES"]
RUN "$APT_INSTALL_SCRIPT" "APT_ESSENTIAL_PACKAGES" --logfile /var/log/pypackit-container/apt_install_essential.log
ARG APT_ESSENTIAL_POST_INSTALL="/usr/local/share/pypackit-container/.devcontainer/environment/apt/essential/post_install.sh"
COPY [".devcontainer/environment/apt/essential/post_install.sh", "$APT_ESSENTIAL_POST_INSTALL"]
RUN chmod +x $APT_ESSENTIAL_POST_INSTALL; \
    $APT_ESSENTIAL_POST_INSTALL

ARG GIT_INSTALL_SCRIPT="/usr/local/share/pypackit-container/.devcontainer/environment/git/install.sh"
COPY [".devcontainer/environment/git/install.sh", "$GIT_INSTALL_SCRIPT"]
ENV PATH=/usr/local/git/bin:$PATH
RUN chmod +x "$GIT_INSTALL_SCRIPT"; \
    "$GIT_INSTALL_SCRIPT" \
        --version "2.49.0" \
        --prefix "/usr/local/git" \
        --logfile "/var/log/pypackit-container/git_install.log" \
        --debug

ARG USERNAME=pypackit-dev \
    USER_HOME=/home/pypackit-dev \
    USER_GID=1000 \
    USER_UID=1000
RUN set -eux; \
    groupadd --gid $USER_GID $USERNAME; \
    useradd \
        --create-home \
        --home-dir "$USER_HOME" \
        --gid $USER_GID \
        --shell /bin/bash \
        --uid $USER_UID \
        $USERNAME; \
    echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" | tee /etc/sudoers.d/$USERNAME > /dev/null; \
    chmod 0440 /etc/sudoers.d/$USERNAME;

ARG TEXLIVE_INSTALL_SCRIPT="/usr/local/share/pypackit-container/.devcontainer/environment/texlive/install.sh" \
    TEXLIVE_INSTALL_PROFILE="/usr/local/share/pypackit-container/.devcontainer/environment/texlive/install.profile"
COPY [".devcontainer/environment/texlive/install.sh", "$TEXLIVE_INSTALL_SCRIPT"]
COPY [".devcontainer/environment/texlive/install.profile", "$TEXLIVE_INSTALL_PROFILE"]
RUN chmod +x "$TEXLIVE_INSTALL_SCRIPT"; \
    "$TEXLIVE_INSTALL_SCRIPT" \
        --profile "$TEXLIVE_INSTALL_PROFILE" \
        --logfile "/var/log/pypackit-container/texlive_install.log" \
        --debug

ENV CONDA_DIR=/opt/conda \
    PATH=$CONDA_DIR/bin:$PATH
ARG MINIFORGE_INSTALL_SCRIPT="/usr/local/share/pypackit-container/.devcontainer/environment/conda/install.sh"
COPY [".devcontainer/environment/conda/install.sh", "$MINIFORGE_INSTALL_SCRIPT"]
RUN chmod +x "$MINIFORGE_INSTALL_SCRIPT"; \
    "$MINIFORGE_INSTALL_SCRIPT" \
        --name "Miniforge3" \
        --version "24.11.3-2" \
        --conda-dir "$CONDA_DIR" \
        --group "pypackit-dev" \
        --user "pypackit-dev" \
        --logfile "/var/log/pypackit-container/miniforge_install.log" \
        --debug

ARG APT_RECOMMENDED_PACKAGES="/usr/local/share/pypackit-container/.devcontainer/environment/apt/recommended/packages.txt"
COPY [".devcontainer/environment/apt/recommended/packages.txt", "$APT_RECOMMENDED_PACKAGES"]
RUN "$APT_INSTALL_SCRIPT" "APT_RECOMMENDED_PACKAGES" --logfile /var/log/pypackit-container/apt_install_recommended.log
ARG APT_RECOMMENDED_POST_INSTALL="/usr/local/share/pypackit-container/.devcontainer/environment/apt/recommended/post_install.sh"
COPY [".devcontainer/environment/apt/recommended/post_install.sh", "$APT_RECOMMENDED_POST_INSTALL"]
RUN chmod +x $APT_RECOMMENDED_POST_INSTALL; \
    $APT_RECOMMENDED_POST_INSTALL

ARG CONDA_ENVS_INSTALL_SCRIPT="/usr/local/share/pypackit-container/.devcontainer/environment/conda/install-envs.sh" \
    CONDA_ENVS_DIR="/usr/local/share/pypackit-container/.devcontainer/environment/conda/envs"
COPY [".devcontainer/environment/conda/install-envs.sh", "$CONDA_ENVS_INSTALL_SCRIPT"]
COPY [".devcontainer/environment/conda/envs/", "$CONDA_ENVS_DIR"]
RUN chmod +x "$CONDA_ENVS_INSTALL_SCRIPT"; \
    "$CONDA_ENVS_INSTALL_SCRIPT" \
        --envs "$CONDA_ENVS_DIR" \
        --logfile "/var/log/pypackit-container/conda_envs_install.log" \
        --debug

RUN if id "ubuntu" &>/dev/null; then \
        echo "Deleting user 'ubuntu'" && userdel -f -r ubuntu || echo "Failed to delete ubuntu user."; \
    else \
        echo "User 'ubuntu' does not exist."; \
    fi

ARG OH_MY_ZSH_INSTALL_DIR=/home/pypackit-dev/.oh-my-zsh
RUN set -eux; \
    umask g-w,o-w; \
    mkdir -p "$OH_MY_ZSH_INSTALL_DIR"; \
    git clone --depth=1 \
        -c core.eol=lf \
        -c core.autocrlf=false \
        -c fsck.zeroPaddedFilemode=ignore \
        -c fetch.fsck.zeroPaddedFilemode=ignore \
        -c receive.fsck.zeroPaddedFilemode=ignore \
        "https://github.com/ohmyzsh/ohmyzsh" \
        "$OH_MY_ZSH_INSTALL_DIR" 2>&1; \
    cd "$OH_MY_ZSH_INSTALL_DIR"; \
    git repack -a -d -f --depth=1 --window=1;

ARG APT_OPTIONAL_PACKAGES="/usr/local/share/pypackit-container/.devcontainer/environment/apt/optional/packages.txt"
COPY [".devcontainer/environment/apt/optional/packages.txt", "$APT_OPTIONAL_PACKAGES"]
RUN "$APT_INSTALL_SCRIPT" "APT_OPTIONAL_PACKAGES" --logfile /var/log/pypackit-container/apt_install_optional.log
ARG APT_OPTIONAL_POST_INSTALL="/usr/local/share/pypackit-container/.devcontainer/environment/apt/optional/post_install.sh"
COPY [".devcontainer/environment/apt/optional/post_install.sh", "$APT_OPTIONAL_POST_INSTALL"]
RUN chmod +x $APT_OPTIONAL_POST_INSTALL; \
    $APT_OPTIONAL_POST_INSTALL

ARG USER_SHELL=/bin/zsh
RUN rm -f /etc/profile.d/00-restore-env.sh \
    echo "export PATH=${PATH//$(sh -lc 'echo $PATH')/\$PATH}" > /etc/profile.d/00-restore-env.sh \
    chmod +x /etc/profile.d/00-restore-env.sh \
    chown --recursive "$USERNAME:$USERNAME" "$HOME_DIR"; \
    chmod --recursive g+r+w "$HOME_DIR"; \
    find "${HOME_DIR}" -type d | xargs -n 1 chmod g+s; \
    if [ ! -f "/etc/pam.d/chsh" ] || ! grep -Eq '^auth(.*)pam_rootok\.so$' /etc/pam.d/chsh; then \
        echo "auth sufficient pam_rootok.so" >> /etc/pam.d/chsh; \
    elif [[ -n "$(awk '/^auth(.*)pam_rootok\.so$/ && !/^auth[[:blank:]]+sufficient[[:blank:]]+pam_rootok\.so$/' /etc/pam.d/chsh)" ]]; then \
        awk '/^auth(.*)pam_rootok\.so$/ { $2 = "sufficient" } { print }' /etc/pam.d/chsh > /tmp/chsh.tmp && mv /tmp/chsh.tmp /etc/pam.d/chsh; \
    fi; \
    chsh --shell "$USER_SHELL" "$USERNAME";
ENV BASH_ENV=/etc/bash/bashenv

CMD [ "sleep", "infinity" ]
