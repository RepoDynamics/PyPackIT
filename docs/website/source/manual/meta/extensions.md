# Meta Extensions

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

{{pp_meta.name}} allows you to store some or all of your repository's `meta` content
in other repositories, and have them automatically fetched when needed.
This is particularly useful when you are managing multiple repositories,
and want to share some common configurations between them.
This way, you can make changes to the shared configurations in one place,
and have them automatically applied to all repositories that use them.

To avoid unnecessary network requests,
{{pp_meta.name}} will automatically cache the extensions every time they are fetched,
and will use them for a configurable amount of time, before marking them as expired and fetching them again.
This is done both on local clones, as well as on the GitHub servers when running the workflows.

To add an extension to your repository's `meta` content, create a file named `extensions.yaml`
in the root of your repository's `meta` directory.
The file must contain an array of objects, each declaring a single extension for a specific `meta` file.
Each object must contain the following keys:
- `type`: This is the relative path (from the root of the `meta` directory) to the `meta` file
being extended, without the `.yaml` extension.
For example, if you want to extend the `branches.yaml` file under the `dev` subdirectory
of the `meta` directory, you should set this key to `dev/branches`.
- `repo`: This is the fullname (i.e. `USERNAME/REPO-NAME`)
of the GitHub repository containing the extension file.
- `path`: This is the relative path (from the root of the repository) to the extension file in `repo`.

In addition, each object can also set the following optional keys:
- `ref`: This is the branch, tag, or commit hash of the extension file in `repo`.
if not provided, data will be fetched from the most recent commit of the `repo`'s default branch.
- `append_list`: This is a boolean flag (default: `true`) that indicates whether to append
the elements of the arrays (aka lists) present in the extended content to the corresponding existing lists
present in higher-priority content.
If set to `false`, any list that has a corresponding existing list in higher-priority content will
be treated as a duplicate (see `raise_duplicate` below).
- `append_dict`: This is a boolean flag (default: `true`) that indicates whether to append
the key-value pairs of the objects (aka dictionaries) present in the extended content
to the corresponding existing dictionaries present in higher-priority content.
If set to `false`, any dictionary that has a corresponding existing dictionary in higher-priority content
will be treated as a duplicate (see `raise_duplicate` below).
- `raise_duplicate`: This is a boolean flag (default: `false`) that indicates whether to raise an error
if any element (i.e., object, list, or primitive)
in the extended content is already set in a higher-priority content.
If set to `false`, the duplicates will be simply ignored.

The following is an example that extends the
`changelog.yaml` and `issue.yaml` files under the `dev` subdirectory.
Note that when defining multiple extensions for the same `meta` file (in this case, `dev/changelog`),
they must be ordered by priority (highest first).
This means that when two extensions share some common configurations/data,
the configurations/data from the extension with the highest priority will be used.

:::{code-block} yaml
:caption: 🗂 `./.meta/extension.yaml`

:::

Note that you cannot extend the `extensions.yaml` file itself, or any other `meta` file that is
directly under the root of the `meta` directory, namely `path.yaml` and `config.yaml`,
since these files are needed before any extensions can be fetched.
