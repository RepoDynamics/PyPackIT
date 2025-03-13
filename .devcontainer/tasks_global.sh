jupyterlab() {
    jupyter-lab / --ContentsManager.allow_hidden=True --IdentityProvider.token=''
}

build-oj-paper() {
    docker exec -it openjournals \
      inara -o pdf -p -v $1
}

build-conda() {
    _conda-build "$(version)" "$@"
}

_conda-build() {
    conda run --name base --live-stream -vv bash .devcontainer/script/base/conda-build.sh "$@"
}

version() {
    conda activate 'versioning'
    versioningit \
        "pkg" \
        --verbose
    conda deactivate
}
