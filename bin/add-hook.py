#!/usr/bin/env python

import tempfile
import subprocess
import sys
import os.path
import stat
import re

# from https://github.com/pre-commit/pre-commit/blob/faa6f8c70ccef865884adb0cb079c8162013bf19/pre_commit/commands/install_uninstall.py#L31
TEMPLATE_START = "# start templated\n"
TEMPLATE_END = "# end templated\n"

hook_name = sys.argv[1]
hook_path = os.path.join("hooks", hook_name)

if os.path.exists(hook_path):
    print(f"File {hook_path} already exists")
    sys.exit(1)

target = tempfile.TemporaryDirectory()
subprocess.run(["pre-commit", "init-templatedir", target.name, "-t", hook_name])

contents = open(os.path.join(target.name, "hooks", hook_name)).read()

before, rest = contents.split(TEMPLATE_START)
commands, after = rest.split(TEMPLATE_END)

here_arg = re.search(r"^HERE=.*", after, re.MULTILINE)
if not here_arg:
    print("Can't find here arg")
    sys.exit(1)

before += f"\n{here_arg.group(0)}\n"
after = after.replace(here_arg.group(0), "")
commands = commands.replace(
    "--config=.pre-commit-config.yaml",
    '--config="${HERE}/../generated-config/pre-commit-config.yaml"',
)

with open(hook_path, "w") as out:
    out.write(before)
    out.write(commands)
    out.write(after)

original_mode = os.stat(hook_path).st_mode
new_mode = original_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
os.chmod(hook_path, new_mode)
