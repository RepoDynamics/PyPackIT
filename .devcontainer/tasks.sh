project() {
    conda run --cwd /pypackit --live-stream -vv --name proman proman "$@"
}

build-oj-paper() {
    current_dir=$(pwd)
    cd '/pypackit'
    docker exec -it openjournals-inara \
      inara -o pdf -p -v $1
    cd "$current_dir"
}

typecheck() {
    conda run --cwd /pypackit --name type_check --live-stream -vv mypy '--package pypackit' '--package pypackit_testsuite' '--python-executable /opt/conda/envs/app/bin/python' '--config-file .config/mypy.toml' --install-types --non-interactive
}

jupyterlab() {
    current_dir=$(pwd)
    cd '/pypackit'
    conda activate 'jupyter'
    jupyter-lab / --ContentsManager.allow_hidden=True --IdentityProvider.token=''
    conda deactivate
    cd "$current_dir"
}

build() {
    conda run --cwd /pypackit --name website --live-stream -vv bash .devcontainer/script/website_build.sh
}

live() {
    conda run --cwd /pypackit --name website --live-stream -vv bash .devcontainer/script/website_build.sh bash .devcontainer/script/website_livehtml.sh
}
