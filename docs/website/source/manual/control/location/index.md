(manual-cc-location)=
# Location

The control center is a directory in your repository
where all project configurations, metadata, and variables
are consolidated in a [structured format](#manual-cc-structure).
This allows for easy tracking of settings throughout the project's lifespan,
and eliminates the need for maintaining multiple configuration files in
different locations.

By default, the control center directory can be found at
[`.control`](){.user-link-repo-cc}
located at the root of the repository.
You can customize its location
by setting the [`$.control.path`](#ccc-control-path) key
in the control center configuration files.


:::{admonition} Dynamic Directory
:class: important

Like other [dynamic directories](#repo-structure) in your repository,
you should not manually move or rename the control center directory.
Instead, after setting the new path in the configuration files,
simply push the changes to your GitHub repository, or run `pypackit sync` locally.
|{{ ccc.name }}| will automatically move the directory to the new location.
:::


For example, to change the control center location
to a directory at `dev/control-center`, you should have the following
configuration in your [YAML files](#manual-cc-structure-yaml-files):

:::{code-block} yaml
:caption: Setting the control center path to `dev/control-center`

control:
  path: dev/control-center
:::
