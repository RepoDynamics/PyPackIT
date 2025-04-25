#!/usr/bin/env bash
set -e
curl -L -o /usr/local/bin/pixi -fsSL --compressed "https://github.com/prefix-dev/pixi/releases/download/v${VERSION}/pixi-$(uname -m)-unknown-linux-musl"
chmod +x /usr/local/bin/pixi
pixi info
