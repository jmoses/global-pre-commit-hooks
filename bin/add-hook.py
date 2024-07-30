#!/usr/bin/env python

import tempfile
import subprocess
import sys
import os
import stat
import re
import shutil

TRAILER = """
# Capture the previous calls result
code=$?

if [ $code -ne 0 ] ; then
  # If it errors, just exit
  exit $code
elif [ -f .pre-commit-config.yaml ] ; then
  # If the repo has it's own config, run it
  echo "Running repo local pre-commit hooks"
  ARGS[1]=--config="$(pwd)/.pre-commit-config.yaml"

  if [ -x "$INSTALL_PYTHON" ]; then
      exec "$INSTALL_PYTHON" -mpre_commit "${ARGS[@]}"
  elif command -v pre-commit > /dev/null; then
      exec pre-commit "${ARGS[@]}"
  else
    echo 'Unable to run local pre-commit'
    exit 1
  fi
fi
"""

# Set the config path. If relative, it's relative to the repo clone root. Absolute paths also supported.
CONFIG_PATH = os.environ.get("PRECOMMIT_CONFIG_PATH", ".pre-commit-config.yaml")
if not os.path.isabs(CONFIG_PATH):
    CONFIG_PATH = os.path.join(os.getcwd(), CONFIG_PATH)

hook_name = sys.argv[1]
hook_path = os.path.join("hooks", hook_name)

if os.path.exists(hook_path):
    print(f"File {hook_path} already exists")
    sys.exit(1)

target = tempfile.TemporaryDirectory()
subprocess.run(
    ["pre-commit", "init-templatedir", target.name, "-t", hook_name, "-c", CONFIG_PATH]
).check_returncode()

with open(os.path.join(target.name, "hooks", hook_name)) as src:
    contents = src.read().replace("exec", "") + "\n" + TRAILER

    with open(hook_path, "w") as dest:
        dest.write(contents)

os.chmod(
    hook_path, os.stat(hook_path).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
)
