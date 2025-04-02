jupyterlab() {
    jupyter-lab / --ContentsManager.allow_hidden=True --IdentityProvider.token=''
}

build-oj-paper() {
    docker exec -it openjournals \
      inara -o pdf -p -v $1
}

build-python() {
    conda run --name pybuild --live-stream -vv python .devcontainer/script/build_python.py .local/temp/build-python "$@"
}

render-readme() {
    conda run --name pybuild --live-stream -vv python .devcontainer/script/render_readme.py .local/temp/readme-pypi "$@"
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

project() {
    conda run --name pypackit --live-stream -vv project "$@"
}
