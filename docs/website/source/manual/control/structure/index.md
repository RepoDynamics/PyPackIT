(manual-cc-structure)=
# Structure

The control center unifies all project configurations,
metadata, and variables into structured [YAML](#yaml) data files,
eliminating redundancies and the need for
dealing with different tool-specific formats.

The entire control center settings is essentially a large mapping
(equivalent to a JSON object or a Python dictionary) with a [defined schema](#manual-cc-options)
where some keys have simple scalar values (strings, numbers, booleans),
while others have complex nested structures (sequences and mappings).
By default, this mapping is broken down into multiple YAML files,
each containing a thematically related subset of the project configurations:

:::{admonition} Control Center's Default Directory Structure
:class: note dropdown toggle-shown

You can hover over the file names to see their descriptions,
and click on them to open the corresponding file
in your repository (needs [logging in](#help-website-login) to our website).
Note that only the most essential configurations are provided in the default configuration files.
For a full reference of all available [options](#manual-cc-options) you can set,
see the [API reference](#api).

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

{#cc-file-structure}
You are completely free to restructure your configurations in any way you like.
For example, you can have a single large YAML file with all configurations,
or you can further break down the configurations into more files and subdirectories.
You can even break down a single complex value (i.e., a mapping or a sequence)
into multiple files, each containing a subset of the value's data.
When processing the control center, |{{ ccc.name }}| will automatically merge all configurations
into a single mapping using the following logic:

1. The control center directory is recursively scanned
   (excluding the [`hooks`](#manual-control-structure-hooks) subdirectory),
   and all files with a `.yaml` or `.yml` extension (case-insensitive)
   are gathered as configuration files. Each file must represent a mapping.
2. All key-value pairs from the collected files are recursively merged
   into a single mapping, where the values for the same path from different files
   are combined according to the following rules:

   - Mapping key-value pairs are combined. If two mappings share some keys,
     the values are recursively merged according to the same rules.
   - Sequences are concatenated.
     Note that files are always read in a shallow-first alphabetical order,
     so the order of concatenated sequences in the final mapping
     is determined by the order of the files.
   - Scalar values cannot be merged;
     if a scalar value is defined in multiple files,
     an error is raised and the conflicting paths are reported.
   - Mixed types (e.g., a sequence and a mapping) are not allowed at the same path;
     if such a conflict is detected, an error is raised and the conflicting paths are reported.


(manual-cc-configpaths)=
### Configuration Paths

We use [JSONPath](https://datatracker.ietf.org/doc/html/rfc9535) path expressions
to refer to a specific configuration value's location in the control center.

:::{admonition} JSONPath Syntax
:class: note dropdown

JSONPath is a query language that defines a string syntax
for selecting a subset of a data structure.
It was originally designed for JSON data,
but can also be used with other data serialization formats like YAML.
In JSONPath, the root of the data structure
(in our case, the control center's top-level mapping)
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

