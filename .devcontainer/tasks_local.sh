build-oj-paper() {
    current_dir=$(pwd)
    cd '/workspace'
    docker exec -it openjournals \
      inara -o pdf -p -v $1
    cd "$current_dir"
}

typecheck() {
    conda run --cwd /workspace --name type_check --live-stream -vv mypy '--package pypackit' '--package pypackit_testsuite' '--python-executable /opt/conda/envs/{'"'"'type'"'"': '"'"'string'"'"', '"'"'description'"'"': '"'"'Name of the conda environment to use for installation.'"'"', '"'"'default'"'"': '"'"'app'"'"'}/bin/python' '--config-file .config/mypy.toml' --install-types --non-interactive
}

jupyterlab() {
    current_dir=$(pwd)
    cd '/workspace'
    conda activate 'jupyter'
    jupyter-lab / --ContentsManager.allow_hidden=True --IdentityProvider.token=''
    conda deactivate
    cd "$current_dir"
}

project() {
    conda run --cwd /workspace --name pypackit --live-stream -vv proman "$@"
}
