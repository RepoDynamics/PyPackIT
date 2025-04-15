FROM texlive/texlive:latest

ARG USERNAME=pypackit-dev
ARG USER_UID=1001
ARG USER_GID=1001

# Remove ubuntu user if present
RUN if id "ubuntu" &>/dev/null; then \
        echo "Deleting user 'ubuntu'" && userdel -f -r ubuntu || echo "Failed to delete ubuntu user."; \
    else \
        echo "User 'ubuntu' does not exist."; \
    fi

# Create user if it doesn't exist
RUN id -u $USERNAME || ( \
    groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* )

# Switch to new user
USER $USERNAME
WORKDIR /home/$USERNAME

# Copy environment setup files
COPY .devcontainer/container-docs/environment /usr/local/share/environments/
COPY install.py /usr/local/share/app_installation/install.py
COPY .github/.repodynamics/metadata.json /usr/local/share/app_installation/metadata.json
