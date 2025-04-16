FROM ubuntu:noble

ARG TLMIRRORURL=rsync://rsync.dante.ctan.org/CTAN/systems/texlive/tlnet/

ENV DOCKER_BUILDKIT=1 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    TEXLIVE_INSTALL_NO_CONTEXT_CACHE=1 \
    NOPERLDOC=1 \
    # other shells available at /usr/bin/fish and /usr/bin/zsh
    # SHELL=/bin/bash \
    TZ=UTC

# Remove ubuntu user if present
RUN if id "ubuntu" &>/dev/null; then \
        echo "Deleting user 'ubuntu'" && userdel -f -r ubuntu || echo "Failed to delete ubuntu user."; \
    else \
        echo "User 'ubuntu' does not exist."; \
    fi

# Install basic build tools
RUN apt-get update \
    && apt-get upgrade -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends software-properties-common \
    && add-apt-repository universe \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        clang \
        cmake \
        cppcheck \
        curl \
        default-jre \
        default-libmysqlclient-dev \
        equivs \
        fontconfig \
        fish \
        gdb \
        gettext \
        ghostscript \
        git \
        gnuplot-nox \
        gpg \
        gpg-agent \
        inotify-tools \
        jq \
        libatk-bridge2.0-0 \
        libatk1.0-0 \
        libc6 \
        libcups2 \
        libcurl4t64 \
        libdigest-perl-md5-perl \
        libfile-homedir-perl \
        libgbm1 \
        libgcc1 \
        libgdiplus \
        libgetopt-long-descriptive-perl \
        libglut3.12 \
        libgssapi-krb5-2 \
        libgtk-3-0 \
        liblttng-ust1 \
        libncurses6 \
        libnspr4 \
        libnss3 \
        libpango-1.0-0 \
        libpangocairo-1.0-0 \
        libpq-dev \
        libsecret-1-dev \
        libsm6 \
        libsqlite3-dev \
        libssl-dev \
        libstdc++6 \
        libtirpc3t64 \
        libunicode-linebreak-perl \
        libunwind8 \
        libuuid1 \
        libx11-6 \
        libx11-xcb1 \
        libxcomposite1 \
        libxdamage1 \
        libxfixes3 \
        libyaml-tiny-perl \
        lldb \
        llvm \
        make \
        moreutils \
        perl \
        python3 \
        python3-dev \
        python3-pip \
        python3-pip-whl \
        python3-pygments \
        python-is-python3 \
        rsync \
        sqlite3 \
        sudo \
        swig3.0 \
        tk-dev \
        unixodbc-dev \
        unzip \
        uuid-dev \
        valgrind \
        vim \
        vim-doc \
        xtail \
        zip \
        zlib1g \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /var/cache/apt/ \
    && export LIBDIR \
    && LIBDIR="$(find /usr/lib -maxdepth 1 -type d -name '*-linux-*' | grep -v '^.*/config-')" \
    && export BASELIBDIR \
    &&   BASELIBDIR="$(basename "${LIBDIR}")" \
    && ln -sf "/usr/lib/${BASELIBDIR}/libglut.so.3.12" "/usr/lib/${BASELIBDIR}/libglut.so.3"

WORKDIR /tmp
RUN curl https://tug.org/texlive/files/debian-equivs-2023-ex.txt --output texlive-local && \
    sed -i "s/2023/9999/" texlive-local && \
    equivs-build texlive-local && \
    dpkg -i texlive-local_9999.99999999-1_all.deb && \
    apt-get install -qyf --no-install-recommends && \
    apt-get clean && \
    rm -rf ./*texlive* && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /var/cache/apt/

# Install TeX Live from upstream mirror using full scheme, no docs or sources
RUN echo "Fetching installation from mirror $TLMIRRORURL" && \
    rsync -a --stats "$TLMIRRORURL" texlive && \
    cd texlive && \
    # create installation profile for full scheme installation
    echo "selected_scheme scheme-full" > install.profile && \
    echo "tlpdbopt_install_docfiles 0" >> install.profile && \
    echo "tlpdbopt_install_srcfiles 0" >> install.profile && \
    echo "tlpdbopt_autobackup 0" >> install.profile && \
    echo "tlpdbopt_sys_bin /usr/bin" >> install.profile && \
    ./install-tl -profile install.profile && \
    cd .. && \
    rm -rf texlive

# Finalize TeX Live setup: add to PATH, patch ConTeXt, generate caches
RUN echo "Adding TeX Live binaries to system PATH" && \
    $(find /usr/local/texlive -name tlmgr) path add && \
    # Patch for ConTeXt (issue #30)
    (sed -i '/package.loaded\["data-ini"\]/a if os.selfpath then environment.ownbin=lfs.symlinktarget(os.selfpath..io.fileseparator..os.selfname);environment.ownpath=environment.ownbin:match("^.*"..io.fileseparator) else environment.ownpath=kpse.new("luatex"):var_value("SELFAUTOLOC");environment.ownbin=environment.ownpath..io.fileseparator..(arg[-2] or arg[-1] or arg[0] or "luatex"):match("[^"..io.fileseparator.."]*$") end' /usr/bin/mtxrun.lua || true) && \
    echo "Generating font and ConTeXt caches..." && \
    (luaotfload-tool -u || true) && \
    mkdir -p /etc/fonts/conf.d && \
    (cp "$(find /usr/local/texlive -name texlive-fontconfig.conf)" /etc/fonts/conf.d/09-texlive-fonts.conf || true) && \
    fc-cache -fsv && \
    if [ -f "/usr/bin/context" ]; then \
      mtxrun --generate && \
      texlua /usr/bin/mtxrun.lua --luatex --generate && \
      context --make && \
      context --luatex --make; \
    fi

# test the installation; we only test the full installation because
# in that, all tools are present and have to work
RUN if [ "$SCHEME" = "full" ]; then \
        latex --version && printf '\n' && \
        biber --version && printf '\n' && \
        xindy --version && printf '\n' && \
        arara --version && printf '\n' && \
        context --version && printf '\n' && \
        context --luatex --version && printf '\n' && \
        asy --version && printf '\n' && \
        if [ "$DOCFILES" = "yes" ]; then texdoc -l geometry; fi && \
        if [ "$SRCFILES" = "yes" ]; then kpsewhich amsmath.dtx; fi; \
    fi && \
    python --version && printf '\n' && \
    pygmentize -V && printf '\n'


# Setup Fish
RUN FISH_PROMPT="function fish_prompt\n    set_color green\n    echo -n (whoami)\n    set_color normal\n    echo -n \":\"\n    set_color blue\n    echo -n (pwd)\n    set_color normal\n    echo -n \"> \"\nend\n" \
    && printf "$FISH_PROMPT" >> /etc/fish/functions/fish_prompt.fish \
    && printf "if type code-insiders > /dev/null 2>&1; and not type code > /dev/null 2>&1\n  alias code=code-insiders\nend" >> /etc/fish/conf.d/code_alias.fish

COPY .devcontainer/environment /usr/local/share/environments/
COPY install.py /usr/local/share/app_installation/install.py
COPY .github/.repodynamics/metadata.json /usr/local/share/app_installation/metadata.json
