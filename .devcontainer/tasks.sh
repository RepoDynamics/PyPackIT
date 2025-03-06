build-oj-paper() {
    docker exec -it openjournals \
      inara -o pdf -p -v $1
}
