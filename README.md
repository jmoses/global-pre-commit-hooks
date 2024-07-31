Create an easy-ish way to manage global git hooks, without actually having to do it on a per-repo basis, or "polluting" the repos with a config setup for whatever hook management solution.

This uses [pre-commit](https://github.com/pre-commit/pre-commit) with some slight changes to the hook script, and depends on the git `core.hooksPath` (either globally or locally, but locally is less useful) being set to the clone of this repo.

It will run all of the configured hooks at the appropriate time.  It will also check to see if there's an executable in the "normal" git hooks path (`.git/hooks/[hook]`), and if present, run it as well, using all the parameters that pre-commit usually sends the hook.

## To enable

Install `pre-commit` and clone this repo.  Then from in the clone

```
git config --global core.hooksPath $(pwd)/hooks
```

Then just add the hooks you're interested in as outlined below.  The default config has hooks for `pre-push` and `pre-commit`.

## To add new hooks

From the clone of this repo:

```shell
> python bin/add-hook.py {hook_name}
```

Where `hook_name` is anything that pre-commit supports on it's own.  This will write out the normal hook file, then read it in, modify it, and write it into the current directory, where it will start to be used immediately.

### Global pre-commit config location

By default the `add-hook.py` command will expect the pre-commit config to be `[repo clone location]/.pre-commit-config.yaml`.  If you want to have it read from somewhere else, the `add-hook.py` command will read from the `PRECOMMIT_CONFIG_PATH` environment variable, which can be a path relative to the repo, or an absolute path.

# [pre-commit](https://github.com/pre-commit/pre-commit) hooks

## `npm-task-if-exists`

Runs an NPM task if it exists. Takes the task name as an argument.

Requires: [jq](https://github.com/jqlang/jq)

## `local-repo-hook`

Runs an existing hook in the local repo, if it is present.
