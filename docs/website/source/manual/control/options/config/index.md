# Base Config

:::{toctree}
:hidden:

cache
:::


{{ pp_meta.custom.meta[docname].tabs }}

Base configurations are those that concern the control center itself,
and are thus needed before the processing of the control center can begin.


::::{grid} 1 2 2 2
:gutter: 3

:::{grid-item-card} Cache
:class-title: sd-text-center
:link: cache
:link-type: doc
:margin: 3 3 auto auto

Settings for various cached data,
such as extension files and other data obtained through various web APIs.
:::

::::

When working with a local clone of the repository on your computer,
you can overwrite these configurations by creating another `config.yaml` file (with the same syntax)
in the root of the repository's local directory.
Since the files under the local directory are automatically added to the `.gitignore` file,
this file will not be tracked by Git, and thus will not be pushed to the remote repository.
This allows you to easily maintain your own local configurations without affecting the remote repository,
which may be useful when working on development branches.
