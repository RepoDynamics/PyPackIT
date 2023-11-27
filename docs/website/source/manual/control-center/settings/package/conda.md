# Conda

:::::{tab-set}
::::{tab-item} Info
- **Relative Path**: `{{ pp_meta.custom.meta[docname].path }}`
- **Pre-configured**: {{ pp_meta.custom.meta[docname].pre_config }}
::::
::::{tab-item} Schema
:::{code-block} yaml
{{ pp_meta.custom.meta[docname].schema_str }}
:::
::::
::::{tab-item} Default
:::{code-block} yaml
{{ pp_meta.custom.meta[docname].default_str }}
:::
::::
::::{tab-item} Example
:::{code-block} yaml
{{ pp_meta.custom.meta[docname].example_str }}
:::
::::
:::::

Conda packages are built with [conda-build](https://docs.conda.io/projects/conda-build/),
using instructions that are mostly defined in a single YAML file named
[meta.yaml](https://conda.io/projects/conda-build/en/stable/resources/define-metadata.html).
The YAML file can be created [from scratch](https://docs.conda.io/projects/conda-build/en/stable/user-guide/tutorials/build-pkgs.html)
, or with help of other utilities, such as [conda skeleton](https://docs.conda.io/projects/conda-build/en/stable/user-guide/tutorials/build-pkgs-skeleton.html)
. After build, the package distribution can be
[uploaded](https://docs.anaconda.com/free/anacondaorg/user-guide/tasks/work-with-packages/#uploading-packages)
on an Anaconda channel. While this may be done on a [personal channel](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/create-custom-channels.html)
, this complicates the installation process for users as they now have to specify the channel as well.
A more convenient alternative is to publish the package on the [conda-forge](https://conda-forge.org/) channel.
This requires following the [instructions](https://conda-forge.org/docs/maintainer/adding_pkgs.html).
