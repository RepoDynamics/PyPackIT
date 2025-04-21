#!/usr/bin/env bash
set -euxo pipefail

# Install conda environments and setup conda configuration.


# Default arguments
ENVS=""
UPDATE_BASE=false
NO_CACHE_CLEAN=false
LOGFILE=""
DEBUG=false

OPTS=$(
    getopt \
        --longoptions env:,update-base,no-cache-clean,logfile:,debug,help \
        --name "$0" \
        --options '' \
        -- "$@"
)

if [[ $? -ne 0 ]]; then
    echo "Failed to parse options." >&2
    exit 1
fi

eval set -- "$OPTS"

while true; do
    case "$1" in
        --envs) ENVS="$2"; shift 2;;
        --update-base) UPDATE_BASE=true; shift;;
        --no-cache-clean) NO_CACHE_CLEAN=true; shift;;
        --logfile) LOGFILE="$2"; shift 2;;
        --debug) DEBUG=true; shift;;
        --help) show_help; exit 0;;
        --) shift; break;;
        *) echo "Unknown option: $1" >&2; show_help >&2; exit 1;;
    esac
done

if ! [[ "$DEBUG" == true ]]; then
    set +x
fi

if [[ -n "$LOGFILE" ]]; then
    echo "📝 Initializing logging to '$LOGFILE'."
    mkdir -p "$(dirname "$LOGFILE")"
    exec > >(tee -a "$LOGFILE") 2>&1
fi

if [[ "$UPDATE_BASE" == true ]]; then
    echo "⚠️ Updating base conda environment."
    conda update -n base --all -y
fi

if [ -d $ENVS ] && find $ENVS -name '*.yaml' | grep -q .; then
    umask 0002;
    for file in "$ENVS/*.yaml"; do
        conda env update --file "$file" 2>&1
    done
fi

if [[ "$NO_CACHE_CLEAN" == false ]]; then
    echo "Cleaning up conda cache..."
    conda clean --all -y
fi

