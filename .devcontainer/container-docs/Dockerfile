FROM texlive/texlive:latest
RUN if id "ubuntu" &>/dev/null; then \
        echo "Deleting user 'ubuntu'" && userdel -f -r ubuntu || echo "Failed to delete ubuntu user."; \
    else \
        echo "User 'ubuntu' does not exist."; \
    fi

COPY .devcontainer/container-docs/environment /usr/local/share/environments/
COPY install.py /usr/local/share/app_installation/install.py
COPY .github/.repodynamics/metadata.json /usr/local/share/app_installation/metadata.json
