# Extensions


{{ pp_meta.custom.meta[docname].tabs }}

{{pp_meta.name}} allows you to dynamically inherit
some or all of the contents of your repository's control center from other repositories.
This is particularly useful when you are managing multiple repositories,
and want to share some common configurations and metadata between them.
Using extensions, you can make changes to the shared data in one place,
and have them automatically applied to all repositories that use them.


## Setting

The {{ pp_meta.custom.meta[docname].path }} file accepts an array of objects,
each declaring a single extension for a specific file.
Each object defines the following keys:

:type: ***string***

    The YAML or TOML file in the control center to extend, defined by its relative path
    from the root of the control center, excluding the file extension.
    For example, to extend the `dev/branch.yaml` file, set this to `dev/branch`.
    As an exception, tool configuration files under `package_python/tools` are
    all defined by the same extension, `package_python/tools`.

:repo: ***string***

    The fullname of the target GitHub repository to retrieve the extension file from.
    The fullname has the form `OWNER-USERNAME/REPOSITORY-NAME`,
    e.g., `RepoDynamics/PyPackIT`.

:ref: ***string***, ***optional***

    A Git reference (e.g., branch, tag, or commit hash) in the target repository
    to retrieve the extension file from.
    If not specified, the latest commit on the default branch
    of the target repository is used as the reference.

:path: ***string***

    The path to the extension file in the target repository,
    relative to the root of the repository.

:append_list: ***boolean***, ***default***: `true`

    Whether to append the elements of the arrays (aka lists)
    present in the extended content to the corresponding existing arrays
    present in higher-priority content.
    If set to `false`, any array that has a corresponding existing array
    in higher-priority content will be treated as a duplicate
    (see `raise_duplicate` below).

:append_dict: ***boolean***, ***default***: `true`

    Whether to append the key-value pairs of the objects (aka dictionaries)
    present in the extended content to the corresponding existing objects
    present in higher-priority content.
    If set to `false`, any object that has a corresponding existing object
    in higher-priority content will be treated as a duplicate
    (see raise_duplicate below).

:raise_duplicate: ***boolean***, ***default***: `false`

    Whether to raise an error if any element (i.e., object, array, string, etc.)
    in the extended content is already set in a higher-priority content.
    If set to false, the duplicates will be simply ignored.


:::{important}
- When defining multiple extensions for the same file,
  they must be ordered by priority (highest first).
  This means that when `raise_duplicate` is set to `false` and
  two extensions share some common configurations/data,
  the configurations/data from the extension with the highest priority will be used.
- Only YAML and TOML files in the control center can be extended.
:::


## Usage

During the processing of your repository's control center,
for each YAML or TOML file, {{pp_meta.name}} checks if there are any extensions defined for it.
If so, it will first look for [unexpired](/manual/control/options/config/cache.md)
cached copies of the extension files, and if not found,
it will fetch them from the GitHub servers and cache them for future use.
This is done both on local devices, and on the GitHub servers when running the workflows:
On local devices, the extension files are cached in the RepoDynamics cache directory
under the local directory of the repository, whereas on the GitHub servers,
they are cached in the GitHub Actions cache directory (not part of the repository files)
that can be accessed from the Actions tab of the repository.
Subsequently, the contents of the extension files are merged into the contents of the target file,
according to the extension settings.
