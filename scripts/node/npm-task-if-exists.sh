#!/bin/bash

[ -f package.json ] || exit 0

TASK=$1

if jq -e ".scripts | has(\"${TASK}\")" package.json > /dev/null ; then
    exec npm run "${TASK}"
fi
