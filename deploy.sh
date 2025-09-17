#!/usr/bin/env bash

set -euxo pipefail
cd "$(dirname "$0")"

uv build

scp dist/*.whl irc.milkmedicine.net:/home/nil
ssh irc.milkmedicine.net "
    sudo su - nil bash -c '
        cd /home/nil && \
        . .venv/bin/activate && \
        uv pip install *.whl --reinstall
    ' && \
    systemctl restart sojuthing.service
"
