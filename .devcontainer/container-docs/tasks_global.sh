build() {
    conda run --name website --live-stream -vv bash .devcontainer/container-docs/script/website/build.sh
}

live() {
    conda run --name website --live-stream -vv bash .devcontainer/container-docs/script/website/livehtml.sh
}
