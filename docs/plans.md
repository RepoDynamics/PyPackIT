# Plans

## Support cross-platform build and test

Enable building and testing on platforms/architectures
other than those directly provided by GitHub Actions runners.

References:
- [Supported GitHub-hosted runners and hardware resources](https://docs.github.com/en/actions/using-github-hosted-runners/using-github-hosted-runners/about-github-hosted-runners#supported-runners-and-hardware-resources)
- [QEMU GitHub Actions](https://github.com/docker/setup-qemu-action):
  QEMU is a generic and open source machine emulator and virtualizer,
  which can be used to run a variety of operating systems.
- [Multi-platform Dev Container Builds](https://github.com/devcontainers/ci/blob/main/docs/multi-platform-builds.md)
  by the [devcontainers/ci](https://github.com/devcontainers/ci) GHA action.



## Conda problems

Meta-issue tracking problems with environment.yaml files:
- https://github.com/conda/conda/issues/11341

Currently, selectors are not supported in environment files:
- https://github.com/conda/conda/issues/8089
- https://stackoverflow.com/questions/32869042/is-there-a-way-to-have-platform-specific-dependencies-in-environment-yml
- https://github.com/conda/conda/pull/7258

Creating environments from pyproject.toml is not supported either:
- https://github.com/conda/conda/issues/10633


## Add configuration files (dotfiles) to devcontainers

This can either be done directly by including the files
in the repository and copying to the container during build,
or by creating a dotfiles repository so that each person
can load their own dotfiles. We probably want to do a
combination of both, so that required configurations
are set by the repository, and then each user can
load their own optional configs like themes, secrets, etc.

### Jupyter config

See:
- https://github.com/anaconda/nb_conda_kernels?tab=readme-ov-file#use-with-nbconvert-voila-papermill
- https://github.com/jupyterlab/jupyterlab-github?tab=readme-ov-file#3-enabling-and-configuring-the-server-extension
- https://stackoverflow.com/questions/48950670/jupyterlab-user-settings-file

#### Default theme

Add the following JSON
```json
{
    "@jupyterlab/apputils-extension:themes": {
        "theme": "JupyterLab Dark"
    }
}
```
to the following path:
```bash
"$JUPYTERLAB_DIR/settings/overrides.json"
```
where `$JUPYTERLAB_DIR` (not available by default!) is by default set to `<sys-prefix>/share/jupyter/lab`, where where `<sys-prefix>` is the site-specific directory prefix of the current Python environment, e.g., `/opt/conda/envs/my-jupyter-env`.

see:
- https://jupyterlab.readthedocs.io/en/stable/user/directories.html#overrides-json
- https://stackoverflow.com/a/70485739/14923024

- 