(dev-setup)=
# Setup

All integration and deployment tasks in |{{ ccc.name }}|
are automated on the cloud using [GitHub Actions]().
Therefore, in most cases you do not need to set up
a development environment on your local machine
to contribute to the project.
You can simply apply changes to the project's repository---even
directly in your web browser---and
push them to your fork or branch on GitHub.
|{{ ccc.name }}|'s automated workflows will then take care of the rest,
formatting, refactoring, testing,

However, sometimes you need a more interactive solution,
for example to quickly try out different
|{{ ccc.name }}| provides two options for
replicating the project's development environment
on your local machine:

- [Development containers](#dev-setup-devcontainer):
- [Environment files](#dev-setup-envfile):


| Feature | Environmentless | GitHub Codespaces           | Development Containers | Environment Files |
|---------|------------|-----------------------------|-------------------|-----------|
| Free    | ✅         | ⚠️ Up to 90 hours per month | ✅                | ✅       |


To further support developers during the implementation phase,
|{{ ccc.name }}| encapsulates the project's development environment into
[development containers](https://containers.dev).
Powered by [GitHub Codespaces](https://github.com/features/codespaces) and
[Visual Studio Code](https://code.visualstudio.com) (VS Code),
these containers can run both locally and on the cloud,
providing all contributors with a consistent,
ready-to-use workspace with all required tools preinstalled and configured.


## Environmentless


## Development Containers

[development containers](https://containers.dev/)

A development container (or dev container for short) allows you to use a container
as a full-featured development environment.
It can be used to run an application, to separate tools, libraries,
or runtimes needed for working with a codebase,
and to aid in continuous integration and testing.
Dev containers can be run locally or remotely,
in a private or public cloud, in a variety of
[supporting tools and editors](https://containers.dev/supporting).

[PyCharm](https://www.jetbrains.com/help/pycharm/dev-containers-starting-page.html)

- [GitHub Codespaces](https://github.com/features/codespaces)
- [Visual Studio Code](https://code.visualstudio.com/)


### GitHub Codespaces

[documentation](https://docs.github.com/en/codespaces/overview)


Note that GitHub Codespaces is only **free for 180 and 120 core-hours per month**
for GitHub Pro and GitHub Free users, respectively.
After that, you will be charged for additional usage.
By default, all accounts have a [spending limit](https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-github-codespaces/about-billing-for-github-codespaces#setting-a-spending-limit)
of $0 USD. This prevents new codespaces being created, or existing codespaces being opened,
if doing so would incur a billable cost to your account.
For more information about billing for GitHub Codespaces, see the
[GitHub Documentation](https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-github-codespaces/about-billing-for-github-codespaces).



### Visual Studio Code

1. [Download](https://code.visualstudio.com/Download) and install
   VSCode on [Linux](https://code.visualstudio.com/docs/setup/linux#_install-vs-code-on-linux),
   [macOS](https://code.visualstudio.com/docs/setup/mac#_install-vs-code-on-macos), or
   [Windows](https://code.visualstudio.com/docs/setup/windows#_install-vs-code-on-windows).
2. [Install Docker](https://docs.docker.com/get-started/get-docker/)
   for your operating system. A local installation of
   [Docker Desktop](https://www.docker.com/products/docker-desktop/)
   is recommended, but
   [alternative options](https://code.visualstudio.com/remote/advancedcontainers/docker-options)
   are available as well.
   If you are not using Docker Desktop, make sure you have
   [Docker Compose](https://docs.docker.com/compose/install/) installed as well.

You can [connect to other available containers](https://code.visualstudio.com/remote/advancedcontainers/connect-multiple-containers)
either from [separate VS Code windows](https://code.visualstudio.com/remote/advancedcontainers/connect-multiple-containers#_connect-to-multiple-containers-in-multiple-vs-code-windows)
or by [switching between containers](https://code.visualstudio.com/remote/advancedcontainers/connect-multiple-containers#_connect-to-multiple-containers-in-a-single-vs-code-window)
in the same window.

## Environment Files
