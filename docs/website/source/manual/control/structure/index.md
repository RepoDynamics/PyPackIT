(manual-cc-structure)=
# Structure

The control center unifies all project configurations,
metadata, and variables into structured [YAML](#yaml) data files,
eliminating redundancies and the need for
dealing with different tool-specific formats.

The entire control center settings is essentially a large mapping
(equivalent to a JSON object or a Python dictionary) with a [defined schema](#manual-cc-options)
where some keys have simple scalar values (strings, numbers, booleans)
while others have complex nested structures (sequences and mappings).
By default, this top-level mapping is broken down into multiple YAML files,
each containing a thematically related subset of the project configurations.


:::{admonition} Control Center's Default Directory Structure
:class: note dropdown toggle-shown

You can hover over the file names to see their descriptions,
and click on them to open the corresponding file
in your repository (needs [logging in](#help-website-login) to our website).
Note that many control center [options](#manual-cc-options)
have default values that are automatically applied at runtime,
when not explicitly set in the configuration files.
For a full reference of all available options,
see the [API reference](#api).

<pre>
🏠 <a class="user-link-repo-tree" title="Repository Root Directory">&lt;REPOSITORY ROOT&gt;</a>
 ┃
 ┣ 🗂 <a class="user-link-repo-cc" title="Control Center Directory">.control</a>
 ┃ ┃
 ┃ ┣ 🗂 <a class="user-link-repo-cc-hooks" title="Hooks Subdirectory">hooks</a>
 ┃ ┃ ┃
 ┃ ┃ ┣ 📄 <a class="user-link-repo-cc-hooks-cca" title="CCA Hooks">cca.py</a>
 ┃ ┃ ┃
 ┃ ┃ ┣ 📄 <a class="user-link-repo-cc-hooks-cca-inline" title="CCA Inline Code Templates">cca_inline.py</a>
 ┃ ┃ ┃
 ┃ ┃ ┗ 📄 <a class="user-link-repo-cc-hooks-requirements" title="Python Dependencies">requirements.txt</a>
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

For more information about the `hooks` subdirectory and its content,
see [Hooks](#manual-cc-hooks).
:::


(manual-cc-configpaths)=
## Configuration Paths

We use [JSONPath](#intro-jsonpath) path expressions
to refer to a specific configuration's location in the control center.
For example, you can set the name of your project at [`$.name`](#ccc-name),
i.e., as the value of the `name` key in the top-level control center mapping.
In which control center YAML file this key is defined (if at all) is completely up to you,
as [explained below](#manual-cc-structure-customization).


(manual-cc-structure-customization)=
## Customization

You are completely free to restructure your configurations in any way you like.
For example, you can combine all configurations into a single large YAML file,
or you can further break them down into other files and subdirectories.
You can even break down a single complex value (i.e., a mapping or a sequence)
into multiple files, each containing a subset of the value's data.
During [synchronization](#manual-cc-sync) events,
|{{ ccc.name }}| will automatically merge all configurations
into a single mapping according to the following logic:

1. The control center directory is recursively scanned
   (excluding the [`hooks`](#manual-cc-hooks) subdirectory),
   and all files with a `.yaml` or `.yml` extension (case-insensitive)
   are gathered as configuration files. Each file must represent a mapping.
2. All key-value pairs from the collected files are recursively merged
   into a single mapping, where values for the same path from different files
   are combined according to the following rules:

   - Mapping key-value pairs are combined. If two mappings share some keys,
     the values are recursively merged according to the same rules.
   - Sequences are concatenated.
     Note that configuration files are always read in a shallow-first alphabetical order,
     so the order of concatenated sequences in the final mapping
     is determined by filepaths.
   - Scalar values cannot be merged;
     if a scalar value is defined in multiple files,
     an error is raised and the conflicting paths are reported.
   - Mixed types (e.g., a sequence and a mapping) are not allowed at the same path;
     if such a conflict is detected, an error is raised and the conflicting paths are reported.
