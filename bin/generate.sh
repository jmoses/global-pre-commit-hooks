#!/bin/bash

set -e

yq pre-commit-config.json --output-format yaml > generated-config/pre-commit-config.yaml
