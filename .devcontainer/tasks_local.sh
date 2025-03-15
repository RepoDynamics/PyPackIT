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
    conda run --cwd /workspace --name base --live-stream -vv python .devcontainer/script/base/build-conda.py "$@"
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

typecheck() {
    conda run --cwd /workspace --name type_check --live-stream -vv mypy '--package pypackit' '--package pypackit_testsuite' '--python-executable /opt/conda/envs/{'"'"'type'"'"': '"'"'string'"'"', '"'"'description'"'"': '"'"'Name of the conda environment to use for installation.'"'"', '"'"'default'"'"': '"'"'app'"'"'}/bin/python' '--config-file .devcontainer/config/mypy.toml' --install-types --non-interactive
}

lint() {
    conda run --cwd /workspace --name pre_commit --live-stream -vv pre-commit run --color always --config .devcontainer/config/pre-commit.yaml show-diff-on-failure --verbose
}
