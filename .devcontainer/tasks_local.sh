project() {
    conda run --cwd /workspace --live-stream -vv --name proman proman "$@"
}

build-oj-paper() {
    current_dir=$(pwd)
    cd '/workspace'
    docker exec -it openjournals \
      inara -o pdf -p -v $1
    cd "$current_dir"
}

typecheck() {
    conda run --cwd /workspace --name type_check --live-stream -vv mypy '--package pypackit' '--package pypackit_testsuite' '--python-executable /opt/conda/envs/app/bin/python' '--config-file .config/mypy.toml' --install-types --non-interactive
}

jupyterlab() {
    current_dir=$(pwd)
    cd '/workspace'
    conda activate 'jupyter'
    jupyter-lab / --ContentsManager.allow_hidden=True --IdentityProvider.token=''
    conda deactivate
    cd "$current_dir"
}

build() {
    conda run --cwd /workspace --name website --live-stream -vv bash .devcontainer/container-docs/script/website/build.sh
}

live() {
    conda run --cwd /workspace --name website --live-stream -vv bash .devcontainer/container-docs/script/website/livehtml.sh
}
