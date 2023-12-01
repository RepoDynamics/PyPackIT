# Paths


{{ pp_meta.custom.meta[docname] }}


You can change the name and location of your repository's main directories.
Notice that these changes are not applied automatically, meaning that you must manually
rename the directories and update the corresponding paths in the `meta` content in the same commit.
Also, all directories must be orthogonal to each other, meaning that none of them can be a subdirectory
of another.



All other paths can be configured in the `path.yaml` file located at the root of the `meta` directory.
The file must contain an object with a single key `dir`.
Within the `dir` object, you can define alternative paths for the `source` directory,
`tests` directory, `website` directory, and the `local` directory and its subdirectories.
You can also add other custom keys under `dir.local.cache` and `dir.local.report`
for other tools that you use, and reference them in the corresponding configuration files.
When no `path.yaml` file is present, {{pp_meta.name}} will use the following default values:

:::{code-block} yaml
:caption: 🗂 `./.meta/path.yaml`

:::

Note that you do not have to specify all keys in the `path.yaml` file.
For example, if you only want to change the name of the `source` directory and the `cache` directory,
this is how your `path.yaml` file should look like:

:::{code-block} yaml
:caption: 🗂 `./.meta/path.yaml`
dir:
  source: my_source_directory
  local:
    cache:
      root: my_cache_directory
:::
