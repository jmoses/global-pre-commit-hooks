#!/bin/bash

[ -f package.json ] || exit 0

if jq -e '.scripts | has("lint")' package.json > /dev/null ; then
    exec npm run lint
fi
