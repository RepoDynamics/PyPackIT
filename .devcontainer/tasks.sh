build-oj-paper() {
    docker exec -it inara \
      inara -o pdf -p -v $1
}
