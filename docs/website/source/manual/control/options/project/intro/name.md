# Name
By default, that is when the `core/intro.yaml` file is not present or doesn't contain a `name` key,
the name of the project is derived from the name of the repository,
by replacing each hyphen in the repository name with a space:
```python
def derive_project_name(repo_name: str) -> str:
    project_name = repo_name.replace("-", " ")
    return project_name
```
It is recommended that you keep this default behavior, in order to avoid any confusion
and make it easier for others to find your project. However, if you need to define another name
for your project, you can do so by adding a `name` key to the `core/intro.yaml` file:

:::{code-block} yaml
:caption: 🗂 `./.meta/core/intro.yaml`
# Name of the project
name: PyPackIT
:::

The project name on itself has no restrictions and can be any valid unicode string.
However, by default, {{pp_meta.name}} also derives the package name from the project name,
which has to conform to the
[Python Packaging Authority (PyPA)](https://packaging.python.org/en/latest/specifications/name-normalization/)
guidelines. Therefore, if you do not define the package name manually,
your project name can only contain ASCII alphanumeric characters,
spaces, periods `.`, underscores `_` and hyphens `-`.
Additionally, it must start and end with an alphanumeric character,
meaning that the name must match the following regex:
`^([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9._-]*[a-zA-Z0-9])$`.

:::{note}
The package name is derived from the name of the project, via normalization[^name-normalization]:
The project name is lowercased, with all runs of spaces, periods, underscores and hyphens
replaced with a single hyphen.
:::
[^name-normalization]: [Python Packaging User Guide > PyPA specifications > Package name normalization](https://packaging.python.org/en/latest/specifications/name-normalization/)
