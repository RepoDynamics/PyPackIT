#!/bin/bash
set -eux
# Ensure at least two arguments are provided
if [ "$#" -lt 2 ]; then
    echo "Error: Missing positional arguments." >&2
    echo "Usage: build-conda.sh <package-ID> <package-version> [extra-args...]" >&2
    exit 1
fi
# Assign recipe path
case "$2" in
    main)
        recipe_path="pkg/conda-recipe/local"
        ;;
    test)
        recipe_path="test/conda-recipe/local"
        ;;
    *)
        echo "Invalid package ID. Use 'main', or 'test'." >&2
        exit 1
        ;;
esac
# Check if the recipe path exists and is a file
if [ ! -f "$recipe_path/meta.yaml" ]; then
    echo "Error: Recipe file '$recipe_path' does not exist." >&2
    exit 1
fi
# Export package version
export PKG_FULL_VERSION="$1"
# Remove first two arguments, leaving only extra arguments
shift 2
# Ensure the output folder exists
output_folder=".local/build/conda"
mkdir -p "$output_folder"
# Build
conda build "$recipe_path" \
  --output-folder "$output_folder" \
  --stats-file "$output_folder/build-stats.json" \
  --package-format conda \
  --verify \
  --keep-going \
  --debug \
  --no-anaconda-upload \
  "$@"
