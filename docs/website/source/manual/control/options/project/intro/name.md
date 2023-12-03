# Name

By default, that is when the `project/intro.yaml` file is not present or doesn't contain a `name` key,
the name of your project is derived from the name of the repository,
by replacing each hyphen in the repository name with a space, i.e. via the following Python function:
```python
def derive_project_name(repo_name: str) -> str:
    project_name = repo_name.replace("-", " ")
    return project_name
```
It is recommended that you keep this default behavior, in order to avoid any confusion
and make it easier for others to find your project.


## Setting
If you need to define a custom name
for your project, you can do so by adding a `name` key to the `project/intro.yaml` file:

:::{code-block} yaml
:caption: 🗂 `project/intro.yaml`
# Name of the project
name: My Custom Project Name
:::

The project name on itself has no restrictions and can be any valid unicode string.
However, by default, {{ pp_meta.name} } also derives the package name from the project name,
which has to conform to the
[Python Packaging Authority (PyPA)](https://packaging.python.org/en/latest/specifications/name-normalization/)
guidelines. Therefore, if you do not define the package name manually,
your project name can only contain ASCII alphanumeric characters,
spaces, periods `.`, underscores `_` and hyphens `-`.
Additionally, it must start and end with an alphanumeric character,
meaning that the name must match the following regex:
```text
^([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9._-]*[a-zA-Z0-9])$
```


## Usage
The project name itself is only used to dynamically reference the name of your project
in various documents, such as documentation website, README files, community health files, etc.
However, as mentioned above, it is also used to derive the package name when the latter is not
specified separately.
