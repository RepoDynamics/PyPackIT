# Base Configurations


{{ pp_meta.custom.meta[docname].tabs }}


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
