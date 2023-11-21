# Base Configurations

Base configurations are those that are needed during the initialization of the CI/CD pipelines.
Currently, the only configuration is the number of days to keep the caches for the fetched extensions,
and other data obtained through various web APIs,
such as GitHub repo/users data, software versions, publications etc.

To change the default values (one day for both extensions and API data, as shown below),
create a file named `config.yaml` in the root of the `meta` directory,
and set the corresponding values:

:::{code-block} yaml
:caption: 🗂 `./.meta/config.yaml`
# Number of days to keep the cache data for meta contents
cache_retention_days:
  # For extended `meta` content retrieved from other repositories
  extensions: 1
  # For data retrieved from web APIs 
  api: 1
:::

When working with a local clone of the repository on your computer,
you can overwrite these configurations by creating another `config.yaml` file (with the same syntax) 
in the root of the `local` directory.
