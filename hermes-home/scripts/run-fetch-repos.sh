#!/bin/bash
source /hermes-home/.env 2>/dev/null
export GITHUB_TOKEN
cd /hermes-home/scripts
python3 fetch-repos-info.py "$@"