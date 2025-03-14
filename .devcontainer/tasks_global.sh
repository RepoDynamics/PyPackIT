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
    conda run --name base --live-stream -vv python .devcontainer/script/base/build-conda.py "$@"
}

version() {
    conda activate 'versioning'
    versioningit \
        "pkg" \
        --verbose
    conda deactivate
}

lint() {
    conda run --name pre_commit --live-stream -vv pre-commit run --color always --config .devcontainer/config/pre-commit.yaml show-diff-on-failure --verbose
}
