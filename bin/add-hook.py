#!/usr/bin/env python

import tempfile
import subprocess
import sys
import os
import stat
import re
import shutil

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

shutil.copy(os.path.join(target.name, "hooks", hook_name), hook_path)
