# Installation

{{pp_meta.name}} is distributed on both PyPI and conda-forge repositories,
and so can be conveniently installed using either `mamba`, `conda` or `pip`.
Simply select your package manager, and run the corresponding command in your terminal:

:::::{tab-set}
::::{tab-item} mamba
{{":::{code-block} shell
mamba install -c conda-forge PACKAGE_NAME".replace('PACKAGE_NAME', pp_meta.package.name)}}
:::
::::
::::{tab-item} conda
{{":::{code-block} shell
conda install -c conda-forge PACKAGE_NAME".replace('PACKAGE_NAME', pp_meta.package.name)}}
:::
::::
::::{tab-item} pip
{{":::{code-block} shell
pip install PACKAGE_NAME".replace('PACKAGE_NAME', pp_meta.package.name)}}
:::
::::
:::::

:::{admonition} Reminder: copy with ease
:class: tip
Copy the command by hovering your mouse over the block, and clicking on the button
that appears in its upper right corner.
:::

:::{admonition} Need more help?
:class: note
Please refer to the Introduction(../intro/background/python_pkgs.md)
section for an overview of Python packages and how to install them.
:::

:::{admonition} For developers
:class: seealso
To install the latest development version, or for editable installs,
see the [Developer Guide](../contribute/index.md).
:::
