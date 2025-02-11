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