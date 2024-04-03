#!/bin/bash

set -e
ROOT="$(pwd)"
mkdir -p generated-config
yq pre-commit-config.json --output-format yaml | sed "s+\$this+${ROOT}+g" > generated-config/pre-commit-config.yaml
