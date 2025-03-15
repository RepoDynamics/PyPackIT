#!/usr/bin/env bash
set -eux
RUN if [ -f /tmp/temp-env-files/bash.sh ]; then bash /tmp/temp-env-files/bash.sh; fi
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive && \
  if [ -f /tmp/temp-env-files/apt.txt ]; then \
    apt-get -y install --no-install-recommends $(xargs < /tmp/temp-env-files/apt.txt); \
  fi && rm -rf /var/lib/apt/lists/*
