FROM ubuntu:noble

ARG USERNAME=pypackit-dev
ARG USER_UID=1000
ARG USER_GID=1000

# Remove ubuntu user if present
RUN if id "ubuntu" &>/dev/null; then \
        echo "Deleting user 'ubuntu'" && userdel -f -r ubuntu || echo "Failed to delete ubuntu user."; \
    else \
        echo "User 'ubuntu' does not exist."; \
    fi

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    # Restore man command
    && yes | unminimize 2>&1

ENV LANG="C.UTF-8"

# Install basic build tools
RUN apt-get update \
    && apt-get upgrade -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        make \
        unzip \
        # The tools in this package are used when installing packages for Python
        build-essential \
        swig3.0 \
        # Required for Microsoft SQL Server
        unixodbc-dev \
        # Required for PostgreSQL
        libpq-dev \
        # Required for mysqlclient
        default-libmysqlclient-dev \
        # Required for ts
        moreutils \
        rsync \
        zip \
        libgdiplus \
        jq \
        # By default pip is not available in the buildpacks image
        python3-pip-whl \
        python3-pip \
        #.NET Core related pre-requisites
        libc6 \
        libgcc1 \
        libgssapi-krb5-2 \
        libncurses6 \
        liblttng-ust1 \
        libssl-dev \
        libstdc++6 \
        zlib1g \
        libuuid1 \
        libunwind8 \
        sqlite3 \
        libsqlite3-dev \
        software-properties-common \
        tk-dev \
        uuid-dev \
        curl \
        gettext \
        inotify-tools \
    && rm -rf /var/lib/apt/lists/* \
    # This is the folder containing 'links' to benv and build script generator
    && apt-get update \
    && apt-get upgrade -y \
    && add-apt-repository universe \
    && rm -rf /var/lib/apt/lists/*

# Verify expected build and debug tools are present
RUN apt-get update \
    && apt-get -y install build-essential cmake cppcheck valgrind clang lldb llvm gdb python3-dev \
    # Install tools and shells not in common script
    && apt-get install -yq vim vim-doc xtail software-properties-common libsecret-1-dev \
    # Install additional tools (useful for 'puppeteer' project)
    && apt-get install -y --no-install-recommends libnss3 libnspr4 libatk-bridge2.0-0 libatk1.0-0 libx11-6 libpangocairo-1.0-0 \
                                                  libx11-xcb1 libcups2 libxcomposite1 libxdamage1 libxfixes3 libpango-1.0-0 libgbm1 libgtk-3-0 \
    # Clean up
    && apt-get autoremove -y && apt-get clean -y \

# Default to bash shell (other shells available at /usr/bin/fish and /usr/bin/zsh)
ENV SHELL=/bin/bash \
    DOCKER_BUILDKIT=1

# Install and setup fish
RUN apt-get install -yq fish \
    && FISH_PROMPT="function fish_prompt\n    set_color green\n    echo -n (whoami)\n    set_color normal\n    echo -n \":\"\n    set_color blue\n    echo -n (pwd)\n    set_color normal\n    echo -n \"> \"\nend\n" \
    && printf "$FISH_PROMPT" >> /etc/fish/functions/fish_prompt.fish \
    && printf "if type code-insiders > /dev/null 2>&1; and not type code > /dev/null 2>&1\n  alias code=code-insiders\nend" >> /etc/fish/conf.d/code_alias.fish

# Remove scripts now that we're done with them
RUN apt-get clean -y

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

CMD [ "sleep", "infinity" ]

COPY .devcontainer/environment /usr/local/share/environments/
COPY install.py /usr/local/share/app_installation/install.py
COPY .github/.repodynamics/metadata.json /usr/local/share/app_installation/metadata.json
