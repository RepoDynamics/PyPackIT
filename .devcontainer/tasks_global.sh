project() {
    conda run --live-stream -vv --name proman proman "$@"
}

build-oj-paper() {
    docker exec -it openjournals \
      inara -o pdf -p -v $1
}

typecheck() {
    conda run --name type_check --live-stream -vv mypy '--package pypackit' '--package pypackit_testsuite' '--python-executable /opt/conda/envs/app/bin/python' '--config-file .config/mypy.toml' --install-types --non-interactive
}

jupyterlab() {
    conda activate 'jupyter'
    jupyter-lab / --ContentsManager.allow_hidden=True --IdentityProvider.token=''
    conda deactivate
}

build() {
    conda run --name website --live-stream -vv bash .devcontainer/script/website_build.sh
}

live() {
    conda run --name website --live-stream -vv bash .devcontainer/script/website_livehtml.sh
}
