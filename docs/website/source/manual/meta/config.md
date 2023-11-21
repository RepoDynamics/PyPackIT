# Base Configurations

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


Base configurations are those that are needed during the initialization of the CI/CD pipelines.
Currently, the only configuration is the number of days to keep the caches for the fetched extensions,
and other data obtained through various web APIs,
such as GitHub repo/users data, software versions, publications etc.

:::{admonition} Local Configuration
:class: tip
When working with a local clone of the repository on your computer,
you can overwrite these configurations by creating another `config.yaml` file (with the same syntax)
in the root of the repository's `local` directory.
:::
