# Customization

You can extend your control center's options and functionalities in two ways:
- Defining custom declarations in YAML files.
- Writing custom hooks to generate custom data and files dynamically at runtime.


## Custom Declarations

In general, most control center options only accept a set of
predefined data structures and values, as described in the
[Options](#manual-control-options) section.
This is to ensure that all configurations and data that are
correctly specified by the user, by [validating](#manual-control-validation) them against
a predefined schema.

To allow for user-defined custom specifications, {{ ccc.name }} provides a top-level
[`$.custom`](#ccc-custom) key in the control center configuration files, under which you can define
any custom data structures and values that are not covered by the predefined options.
These can then be referenced and used just like any other control center content.


(cc-hooks)=
## Hooks

To generate more complex data and files that cannot be declaratively defined in YAML files,
{{ ccc.name }} allows you to define custom Python scripts
that are automatically executed at certain stages during the control center processing.
To hook into each stage, you should define a callable object (a function or a class)
with a certain signature (as described below) in the `main.py` file in the
[`hooks` directory](#manual-control-structure-hooks) of the control center.

### Post-Load

The `post_load` hook is executed directly after the control center configuration files are loaded,
and before any other processing is done.
It is given the top-level control center mapping (a Python `dict` object) as a positional argument,
which it can modify in place (any returned value is ignored).
This hook is useful in particular scenarios where a control center configuration that is required
during the data generation and augmentation stages needs to be dynamically generated.

:::{admonition} Example
:class: tip dropdown

Assume you want to set the team members of your project dynamically,
by fetching the data from an external source, e.g., your organization's web API
at `https://api.example.com/team`, which accepts a `GET` request with a `project` query parameter,
and returns a JSON object with the same structure as the [`$.team`](#ccc-team) key in the control center.
To do so, you can define the following `post_load` hook in the `main.py` file in the `hooks` directory:

:::{code-block} python
:caption: `hook/main.py`

import requests

def post_load(ccc: dict) -> None:
    response = requests.get('https://api.example.com/team', params={'project': ccc['name']})
    ccc['team'] = response.json()
    return
:::

And since your hook requires the `requests` library,
you should add it to the `requirements.txt` file in the `hook` directory:

:::{code-block} txt
:caption: `hook/requirements.txt`

requests >= 2.32, < 3  # use a version range that suits your project
:::

### Post-Data

The `post_data` hook is executed after data generation and augmentation.
Like the `post_load` hook, it is given the top-level control center mapping as a positional argument,
which it can modify in place (any returned value is ignored).
This hook is useful when you need to generate additional data that are
not required during the data generation and augmentation stages,
but require the data generated during those stages.


### Post-File

The `post_file` hook is executed after all dynamic files are generated.
It is given two positional arguments:
the top-level control center mapping (like the previous hooks),
and a list of `NamedTuple` objects, each representing a dynamic file that was generated.
The hook can then modify the list of dynamic files, e.g., to add new files or modify existing ones.
Like the previous hooks, the list must be modified in place, and any returned value is ignored.
Note that modifying the control center mapping in this hook
will not affect the control center's contents.
Each `NamedTuple` object has the following attributes:

:type: `Enum`

    Type of the dynamic file.
:subtype: `tuple[str, str]`

    File subtype's ID and title.
:content: `str`

    File content.
:path: `str`

    Current path of the file relative to the repository's root directory.
:path_before: `str`

    Previous path of the file relative to the repository's root directory.
