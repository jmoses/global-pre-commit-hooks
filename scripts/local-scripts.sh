#!/bin/bash

DEFAULT_HOOK_DIR=.git/hooks

hook_type=$(ps -p $PPID -wwf | grep -Eo -- "--hook-type=.*? " | cut -d= -f2 | xargs)
if [[ "${hook_type}x" = "x" ]] ; then
  echo "Unable to determine hook type"
  exit 1
fi

legacy_hook="${DEFAULT_HOOK_DIR}/${hook_type}"
if [ -x "$legacy_hook" ] ; then
  exec "$legacy_hook" "$@"
fi
