build() {
    conda run --cwd '/workspace' -n website --live-stream -vv bash .devcontainer/container-docs/script/website/build.sh
}

live() {
    conda run --cwd '/workspace' -n website --live-stream -vv bash .devcontainer/container-docs/script/website/livehtml.sh
}
