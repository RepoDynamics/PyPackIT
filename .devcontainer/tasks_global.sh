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

typecheck() {
    conda run --name type_check --live-stream -vv mypy '--package pypackit' '--package pypackit_testsuite' '--python-executable /opt/conda/envs/{'"'"'type'"'"': '"'"'string'"'"', '"'"'description'"'"': '"'"'Name of the conda environment to use for installation.'"'"', '"'"'default'"'"': '"'"'app'"'"'}/bin/python' '--config-file .devcontainer/config/mypy.toml' --install-types --non-interactive
}

lint() {
    conda run --name pre_commit --live-stream -vv pre-commit run --color always --config .devcontainer/config/pre-commit.yaml --show-diff-on-failure --verbose
}
