---
ccid: install
---

(install)=
# Installation

{{ccc.name}} can be used for both new and existing projects.
It is built on top of GitHub Actions,
and uses GitHub Actions workflows to interact with your repository and
automate the entire development and maintenance process of your project.
Therefore, installing {{ ccc.name }} in your GitHub repository is a matter of adding these workflows
and other necessary files to your repository, and setting up a few configurations.
For new repositories, this is a straightforward process, as you can
use the {{ ccc.name }} repository template to create a new repository
that contains all the necessary files.
For existing repositories, the process is a bit more involved,
as you need to manually add these files and bring your repository
to a state that is compatible with {{ ccc.name }}.


::::{grid} 1 2 2 2
:gutter: 3

:::{grid-item-card} New Repository
:class-title: sd-text-center
:link: new-repo
:link-type: doc

A step-by-step guide to creating a new GitHub repository and installing {{ ccc.name }}
using the {{ ccc.name }} repository template.
:::

:::{grid-item-card} Existing Repository
:class-title: sd-text-center
:link: existing-repo
:link-type: doc

A step-by-step guide to installing {{ ccc.name }} in an existing GitHub repository.
:::

:::{grid-item-card} Version Management
:class-title: sd-text-center
:link: versioning
:link-type: doc
:margin: 3 3 auto auto

Information on {{ ccc.name}}'s versioning scheme,
and instructions on version management,
such as updating and upgrading {{ ccc.name }} in your repository,
or pinning it to a specific version.
:::

::::
