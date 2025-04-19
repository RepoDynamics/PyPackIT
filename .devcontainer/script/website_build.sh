SPHINX_COMMON_OPTIONS="--verbose --show-traceback --keep-going --color --nitpicky --jobs auto"
sphinx-build -M dirhtml docs/website/source docs/website/.build $SPHINX_COMMON_OPTIONS

# Create a tarball of the built website according to GitHub Pages requirements.
# Ref: https://github.com/actions/upload-pages-artifact/blob/main/action.yml
tar \
  --dereference --hard-dereference \
  --directory "docs/website/.build/dirhtml" \
  -cvf "docs/website/.build/website.tar" \
  --exclude=.git \
  --exclude=.github \
  --exclude=".[^/]*" \
  .
