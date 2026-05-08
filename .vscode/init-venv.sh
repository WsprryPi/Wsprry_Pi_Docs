#!/bin/bash
if [ -f ~/.bashrc ]; then
    # shellcheck disable=SC1090
    source ~/.bashrc
fi
# shellcheck disable=SC1091
source "$(git rev-parse --show-toplevel)/docs/.venv/bin/activate"
