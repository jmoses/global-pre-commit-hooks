Create an easy-ish way to manage global git hooks, without actually having to do it on a per-repo basis, or "polluting" the repos with a config setup for whatever hook management solution.

This uses [pre-commit](https://github.com/pre-commit/pre-commit) with some slight changes to the hook script, and depends on the git `core.hooksPath` (either globally or locally, but locally is less useful) being set to the clone of this repo.

It will run all of the configured hooks at the appropriate time.  It will also check to see if there's an executable in the "normal" git hooks path (`.git/hooks/[hook]`), and if present, run it as well, using all the parameters that pre-commit usually sends the hook.

## To enable

Install `pre-commit`, `yq`, and clone this repo.  Then from in the clone

```
git config --global core.hooksPath $(pwd)
```

## To add new hooks

If you want to use other hooks than the ones that exist, you can get `pre-commit` to output what they would be, by using the `pre-commit init-templatdir` command.  It will output the "proper" hooks into a `hooks` directory and they can be copied over to this repos root.

You then have to move the `HERE` variable declaration above the "templated" section, and update the config path in the `ARGS` variable to be `--config="${HERE}/generated-config/pre-commit-config.yaml"` to pick up the global config.
