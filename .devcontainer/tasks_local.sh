jupyterlab() {
    current_dir=$(pwd)
    cd '/workspace'
    jupyter-lab / --ContentsManager.allow_hidden=True --IdentityProvider.token=''
    cd "$current_dir"
}

build-oj-paper() {
    current_dir=$(pwd)
    cd '/workspace'
    docker exec -it openjournals \
      inara -o pdf -p -v $1
    cd "$current_dir"
}

build-conda() {
    current_dir=$(pwd)
    cd '/workspace'
    _conda-build "$(version)" "$@"
    cd "$current_dir"
}

_conda-build() {
    conda run --cwd /workspace --name base --live-stream -vv bash .devcontainer/script/base/conda-build.sh "$@"
}

version() {
    current_dir=$(pwd)
    cd '/workspace'
    conda activate 'versioning'
    versioningit \
        "pkg" \
        --verbose
    conda deactivate
    cd "$current_dir"
}
