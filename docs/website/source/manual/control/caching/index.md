# Caching

To speed up the processing of your repository's control center,
all data retrieved from the web,
including inherited extensions, GitHub repo/users data, software versions, and publications
can be cached on both local devices and on GitHub servers.
Each time such data is needed, {{ccc.name}} first checks if there is an unexpired entry for it in the cache,
and if not, it will fetch it from the corresponding web API and cache it for future use.


## Location

The cache is a YAML file stored at `RepoDynamics/.metadata_cache.yaml` 
relative to your repository's [cache directory](#manual-repo-cache-dir),
where each piece of cached data is stored as a separate entry with a timestamp.
If you run {{ ccc.name }} on a local device,
you can find the cache file in the repository's cache directory.
However, since the cache directory is added to the [`.gitignore`](#ccc-repo-gitignore) file,
it will not be pushed to the remote repository.
Instead, when project workflows are run on GHA,
the cache directory is stored and retrieved using GHA cache actions,
and can be accessed from the Actions tab of the repository.


## Retention Time

The retention time of each type of cached data can be set in the control center
at [`$.control.cache.retention_hours`](#ccc-control-cache-retention-hours).
This sets the expiration time of each cached entry in hours,
for both local and GHA caches.
However, you might want to set different retention times when
running local control center synchronizations.
One way is to change `$.control.cache.retention_hours`
and then reset it to the original value before commiting the changes.
{{ ccc.name }} provides a more convenient way to do this:
Create a file named `.local_config.yaml` in the repository's cache directory,
and set the desired retention times in it, at the same path as in the control center.

::::{admonition} Example
:class: tip dropdown

:::{code-block} yaml
:caption: `.local_config.yaml`

control:
  cache:
    retention_hours:
      extension: 24
      repo: 24
      user: 24
      orcid: 1000
      doi: 1000
      python: 1000
:::
::::

If this file exists, the control center will use the values in it
instead of the values in the project's control center configuration files.
