(manual-cc-location)=
# Location

The control center is a directory in your repository
where all project configurations, metadata, and variables
are consolidated in a [structured format](#manual-cc-structure).
This allows for easy tracking of settings throughout the project's lifespan
and eliminates the need for maintaining multiple configuration files in
different locations.
By default, the control center can be found at the root of the repository
in a directory named [`.control/`](){.user-link-repo-cc}.


## Customization

You can customize the location of the control center directory
by setting the [`$.control.path`](#ccc-control-path) key
in your configuration files.


:::{admonition} Moving Dynamic Directories
:class: important

Like other [dynamic directories](#repo-structure) in your repository,
you should not manually move or rename the control center directory.
Instead, after setting the new path in the configuration files,
|{{ ccc.name }}| will automatically move the directory to the new location
during the next [synchronization](#manual-cc-sync) event.
:::


For example, to change the control center location
to a repository directory at `dev/control-center`, you should have the following
configuration in your [YAML files](#manual-cc-structure-yaml-files):

:::{code-block} yaml
:caption: Setting the control center path to `dev/control-center`

control:
  path: dev/control-center
:::
