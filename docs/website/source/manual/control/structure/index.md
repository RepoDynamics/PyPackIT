# Structure

The control center is a directory in your repository
containing declarative configurations in data files, along with optional
Python scripts to dynamically generate custom metadata and configurations during runtime.


## Location

By default, the control center is located at a directory named [`.control`](){.user-link-repo-cc}
in the root of your repository.
You can customize its location by setting the [`$.control.path`](#ccc-control-path) key
in your configuration files to the desired path relative to the root of your repository.

:::{admonition} Dynamic Directory
:class: important

Like other [dynamic directories](#repo-structure) in your repository,
you should not manually move or rename the control center directory.
After setting the new path in the configuration files,
simply push the changes to your Github repository, or run `controlman-sync` locally.
{{ ccc.name }} will automatically move the control center directory to the new location.
:::

For example, to change the control center location
to a directory at `dev/control-center`, you should have the following
configuration in one of your YAML files (more details below):

:::{code-block} yaml
:caption: Setting the control center path to `dev/control-center`

control:
  path: dev/control-center
:::


## Data Files

Declarative (i.e., almost all) project configurations are stored in YAML files
within the control center directory.

::::{admonition} YAML Data File Format
:class: note dropdown
:name: yaml-intro

YAML (YAML Ain't Markup Language) is a concise and human-readable data serialization language
commonly used for configuration files,
similar to JSON and TOML formats.
YAML provides 3 main data types: mappings, sequences, and scalars.
Scalars represent single values and include strings, numbers, booleans, and null values.
Sequences and mappings on the other hand are complex data types that can contain other data types.
Sequences (aka lists, arrays) are ordered lists of items, while mappings (aka dictionaries, hash tables)
represent key-value pairs. Each YAML file contains a single top-level data structure,
which can be any of the mentioned data types. For example, a YAML file can contain a single string,
and thus act as a plain text file:

:::{code-block} yaml
:caption: YAML file with a single-line string

'Greetings from within a YAML file!'
:::

:::{code-block} yaml
:caption: YAML file with a multi-line string

|
  Greetings from within a YAML file!
  YAML uses syntactically significant newlines and indentation like Python
  to represent complex data structures in a human-readable format.
  The pipe character (|) is used to denote the start of a multi-line string,
  which can span multiple lines without the need for explicit line breaks
  or quotation marks.
:::

It becomes more interesting when the top-level data type is a mapping or a sequence,
allowing for complex and nested data structures.
Sequences can be created either using dashes (`-`) or square brackets (`[]`).
For example, the following YAML file defines a sequence of mixed data types
using the dash notation (notice the use of `#` for comments):

:::{code-block} yaml
:caption: YAML file with a sequence of mixed data types

- This is the first item in the sequence. It is a string.  # and this is a comment!
- 42             # The second item in the sequence, which is an integer.
- 3.14159265359  # Look, it's π in the third place!
- true           # A boolean value as the fourth item.
- null           # This item is a null (aka None).
- [1, 2, 3]      # A nested sequence using square brackets.
- - One          # A nested sequence using dashes.
  - Two
  - Three
:::

Finally, mappings are created using colon (`:`) or curly braces (`{}`):

:::{code-block} yaml
:caption: YAML file with a mapping as the top-level data structure

key1: value1     # A simple key-value pair; both key and value are strings.
key2: true       # he key is a string and its value is a boolean.
true: 1          # The key is a boolean and the value is an integer.
my-dashed-list:  # A key with a nested sequence as its value.
  - One
  - Two
  - Three
my-inline-list: [1, 2, 3]
my-inline-map: {key1: value1, key2: value2}
my_nested_map:
  key1: value1
  key2: value2
  key3: value3
:::

YAML also provides several advanced features such as anchors and tags
to enhance its flexibility and reusability.
[Anchors](https://yaml.org/spec/1.2.2/#3222-anchors-and-aliases)
allow you to define a value once and reference it later using aliases,
which can significantly reduce duplication and improve maintainability of large configurations.
For example, the following YAML file defines a mapping
named `my-default-settings`, anchors it to the alias `default`,
and uses that alias to reuse the mapping in two different places:

:::{code-block} yaml
:caption: YAML file with anchors and aliases

my-default-settings: &default  # The '&' character is used
  key1: value1                 # to define an anchor named 'default'
  key2: value2                 # for the `my-default-settings` mapping.

my-cases:
  - name: case1
    settings: *default         # The '*' character is used to reference the anchor.
  - name: case2
    settings: *default         # Both cases reference the same settings.
:::

[Tags](https://yaml.org/spec/1.2.2/#tags) allow you to explicitly define the data type of a node
or apply custom semantics to the content.
For instance, a tag like `!str` can be used to specify that a value should be treated as a string.
{{ ccc.name }} uses this feature to allow for
[referencing values from external sources](#cc-inheritance).

To learn more about the YAML file format,
see [Learn YAML in Y Minutes](https://learnxinyminutes.com/docs/yaml/), or check out the
full specification at [yaml.org](https://yaml.org/spec/1.2.2/).
::::

The entire project configuration is essentially a large mapping (aka `dict`),
where some keys have simple scalar values,
while others have complex nested structures.
By default, this mapping is broken down to multiple YAML files,
each containing a thematically related subset of the project configurations:

:::{admonition} Control Center's Default Directory Structure
:class: note dropdown toggle-shown

You can hover over the file names to see their descriptions,
and click on them to open the corresponding file
in your repository (needs [logging in](#help-website-login) to our website).
Note that only the most essential configurations are provided in the default configuration files.
For a full reference of all available options you can set,
see the [Options](#cc-options) section.

<pre>
🏠 <a class="user-link-repo-tree" title="Repository Root Directory">&lt;REPOSITORY ROOT&gt;</a>
 ┃
 ┣ 🗂 <a class="user-link-repo-cc" title="Control Center Directory">.control</a>
 ┃ ┃
 ┃ ┣ 📄 <a class="user-link-repo-cc-proj" title="Main Project Configurations">proj.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a class="user-link-repo-cc-pkg" title="Package Configurations">pkg.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a class="user-link-repo-cc-doc" title="Documentation Configurations">doc.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a class="user-link-repo-cc-test" title="Test Suite Configurations">test.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a class="user-link-repo-cc-vcs" title="Version Control System Configurations">vcs.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a class="user-link-repo-cc-its" title="Issue Tracking System Configurations">its.yaml</a>
 ┃ ┃
 ┃ ┗ 📄 <a class="user-link-repo-cc-ci" title="Workflow Configurations">ci.yaml</a>
 ┗ ...
</pre>

:::

{.dummy #cc-file-structure}
You are completely free to restructure your configurations in any way you like.
For example, you can have a single large YAML file with all configurations,
or you can further break down the configurations into more files and subdirectories.
You can even break down a single complex value (i.e., a mapping or a sequence)
into multiple files, each containing a subset of the value's data.
When processing the control center, {{ ccc.name }} will automatically merge all configurations
into a single mapping using the following logic:

1. The control center directory is recursively scanned
   (excluding the [`hook`](#cc-dir-hook) subdirectory),
   and all files with a `.yaml` or `.yml` extension (case-insensitive)
   are gathered as configuration files. Each file must represent a mapping.
2. All key-value pairs from the collected files are recursively merged
   into a single mapping, where the values for the same path from different files
   are combined according to the following rules:

   - Mapping key-value pairs are combined. If two mappings share some keys,
     the values are recursively merged according to the same rules.
   - Sequences are concatenated.
     Note that files are always read in a shallow-first alphabetical order (i.e., using
     `sorted(pathlib.Path(CONTROL_CENTER_DIRPATH).rglob('*'), key=lambda p: (p.parts, p))`{l=python}),
     so the order of sequences in the final mapping is determined by the order of the files.
   - Scalar values cannot be merged;
     if a scalar value is defined in multiple files,
     an error is raised and the conflicting paths are reported.
   - Mixed types (e.g., a sequence and a mapping) are not allowed at the same path;
     if such a conflict is detected, an error is raised and the conflicting paths are reported.

(manual-control-configpaths)=
### Configuration Paths

We use [JSONPath](https://datatracker.ietf.org/doc/html/rfc9535) path expressions
to refer to a specific configuration value's location in the control center.

:::{admonition} JSONPath Syntax
:class: note dropdown

JSONPath is a query language that defines a string syntax for selecting a subset of a data structure.
It was originally designed for JSON data,
but can also used with other data serialization formats like YAML.
The root of the data structure (in our case, the control center's top-level mapping)
is represented by the `$` symbol,
mapping keys are accessed using the dot (`.`) notation,
and sequences are accessed using square brackets (`[]`) with an index.

For example, the path expression `$.l1-key.l2-key[0]`
means that the top-level data structure is a mapping,
it has a key named `l1-key` whose value is also a mapping,
with a key named `l2-key` whose value is a sequence,
and we are referring to the first element (index 0) of that sequence.

Wildcards can also be used in path expressions using the `*` symbol,
to match any key or index at a specific level.
For example, `$[*].l2-key` means that the root data structure is a sequence
of mappings, and we are referring to the value of the key `l2-key` in each mapping.
:::

For example, you can set the name of your project at [`$.name`](#ccc-name),
i.e., as the value of the `name` key in the top-level mapping of the control center.
In which control center YAML file this key is defined (if at all) is completely up to you,
as explained [above](#cc-file-structure).


(manual-control-structure-hooks)=
## Python Scripts

In addition to declarative configurations in YAML files,
you can also include Python scripts in the control center directory.
These can act as hooks to [dynamically generate custom metadata and configurations](#cc-hooks)
during control center synchronization events.
To do so, you must create a subdirectory named `hook` at the root of the control center directory,
containing a file named `main.py`.
Before running your script, {{ ccc.name }} will also look for a `requirements.txt` file
in the `hook` directory, and install the specified packages using `pip` if found.
Note that in contrast to the YAML files,
the `hook` directory and and its constituent `main.py` and `requirements.txt` files
must be exactly named and located as described above.
However, beside these two files,
you are free to add any other additional files or subdirectories in the `hook` directory.
For example, if you want to implement multiple complex hooks,
you can modularize your code by creating a Python package in the `hook` directory,
adding it to your `hook/requirements.txt` file, and importing it in your `hook/main.py` script.
