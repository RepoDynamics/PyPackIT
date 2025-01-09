(manual-cc-hooks)=
# Hooks

While most aspects of your project and its workflows
are already highly customizable via the provided control center configurations,
there may still remain some complex routines you wish to add
that are not covered by the available options.
Therefore, |{{ ccc.name }}| also allows you to add custom plugins for maximum flexibility.
These can hook into different stages of your workflows to perform arbitrary tasks.
Plugins are defined in Python modules added to a subdirectory named `hooks`
located at the root of the control center directory.
For each workflow, |{{ ccc.name }}| looks for a specific Python file in this directory.
Each file must contain a class named `Hooks` with a predefined signature,
which will be instantiated at the beginning of the corresponding workflow.
This class must define specific methods for hooking into certain stages of the workflow.
At each stage, if a corresponding method exists, it will be called with a set of relevant arguments.
Also, before running your hooks, |{{ ccc.name }}| will look for a `requirements.txt` file
in the `hooks` directory, and will install the specified packages using `pip`.


:::{admonition} Control Center's `hooks` Subdirectory Structure
:class: note dropdown toggle-shown

Note that in contrast to the [control center YAML files](#manual-cc-structure),
the `hooks` subdirectory and its constituent files
must be exactly named and located as described here.
You are however free to add any other additional files or subdirectories.
For example, if you want to implement multiple complex hooks,
you can modularize your code by creating a Python package in the `hooks` directory,
adding it to your `hooks/requirements.txt` file,
and importing it in your hook modules.

<pre>
🏠 <a class="user-link-repo-tree" title="Repository Root Directory">&lt;REPOSITORY ROOT&gt;</a>
 ┃
 ┣ 🗂 <a class="user-link-repo-cc" title="Control Center Directory">.control</a>
 ┃ ┃
 ┃ ┣ 🗂 <a class="user-link-repo-cc-hooks" title="Hooks Subdirectory">hooks</a>
 ┃ ┃ ┃
 ┃ ┃ ┣ 📄 <a class="user-link-repo-cc-hooks-cca" title="CCA Hooks">cca.py</a>
 ┃ ┃ ┃
 ┃ ┃ ┣ 📄 <a class="user-link-repo-cc-hooks-cca-inline" title="CCA Inline Code Templates">cca_inline.yaml</a>
 ┃ ┃ ┃
 ┃ ┃ ┗ 📄 <a class="user-link-repo-cc-hooks-requirements" title="Python Dependencies">requirements.txt</a>
 ┃ ┗ ...
 ┗ ...
</pre>

:::


Note that the `cca_inline.py` module serves a slightly different purpose,
which is documented in the [Templating](#manual-cc-templating) section.


## CCA

CCA plugins hook into the Continuous configuration automation pipeline
that processes your control center configuration files to synchronize your repository.
They can be added to the `Hooks` class in the `cca.py` module,
which is included in your repository by default.
This class can define 9 public methods, corresponding to the 9 stages of the CCA pipeline.
No return value is expected from any of the methods, but most are given mutable input arguments
that they may modify in-place.
