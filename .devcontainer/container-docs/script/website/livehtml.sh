sphinx-autobuild \
  docs/website/source \
  docs/website/.build \
  --verbose --show-traceback --keep-going --color --nitpicky --jobs auto \
  -a -b=dirhtml --open-browser --delay 0
