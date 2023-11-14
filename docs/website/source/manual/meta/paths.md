# Repository Paths
You can change the name and location of your repository's main directories.
Notice that these changes are not applied automatically, meaning that you must manually
rename the directories and update the corresponding paths in the `meta` content in the same commit.
Also, all directories must be orthogonal to each other, meaning that none of them can be a subdirectory
of another.


## Meta Directory
To change the path of the `meta` directory (default: `./.meta`), 
create a file at `./.github/.repodynamics_meta_path.txt`
and put the new path (relative to the root of repository) in it.
Example:

:::{code-block}
:caption: 🗂 `./.github/.repodynamics_meta_path.txt`
some_directory/my_custom_meta_directory
:::


## Other Directories
All other paths can be configured in the `paths.yaml` file located at the root of the `meta` directory.
The file must contain an object with a single key `path`, which itself must contain an object with the
single key `dir`. Within the `dir` object, you can define alternative paths for the `source` directory,
`tests` directory, `website` directory, and the `local` directory and its subdirectories.
You can also add other custom keys under `path.dir.local.cache` and `path.dir.local.report`
for other tools that you use, and reference them in the corresponding configuration files.
When no `paths.yaml` file is present, {{pp_meta.name}} will use the following default values:

:::{code-block} yaml
:caption: 🗂 `./.meta/paths.yaml`
path:
  dir:
    # Name of the source directory
    source: src
    # Path to the tests directory
    tests: tests
    # Path to the website directory
    website: docs/website
    local:
      # Path to the local directory
      root: .local
      cache:
        # Name of the cache directory under the local directory
        root: cache
        # Name of subdirectories under the cache directory
        # You can add other keys here for other tools that you use
        repodynamics: repodynamics
        coverage: coverage
        mypy: mypy
        pylint: pylint
        pytest: pytest
        ruff: ruff
      report:
        # Name of the report directory under the local directory
        root: report
        # Name of subdirectories under the report directory
        # You can add other keys here for other tools that you use
        repodynamics: repodynamics
        coverage: coverage
        mypy: mypy
        pylint: pylint
        pytest: pytest
        ruff: ruff
:::

Note that you do not have to specify all keys in the `paths.yaml` file.
For example, if you only want to change the name of the `source` directory and the `cache` directory,
this is how your `paths.yaml` file should look like:

:::{code-block} yaml
:caption: 🗂 `./.meta/paths.yaml`
path:
  dir:
    source: my_source_directory
    local:
      cache:
        root: my_cache_directory
:::
