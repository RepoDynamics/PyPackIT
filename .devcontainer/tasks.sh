jupyterlab() {
    jupyter-lab / --ContentsManager.allow_hidden=True --IdentityProvider.token=''
}

build-oj-paper() {
    docker exec -it openjournals \
      inara -o pdf -p -v $1
}
