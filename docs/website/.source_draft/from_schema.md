From the seven [main directories](/manual/fundamentals/structure/index.md) in your repository
that |{{ccc.name}}| manages and works with,
the [GitHub directory](/manual/fundamentals/structure/github.md)
and the [Docs directory](/manual/fundamentals/structure/docs.md)
have fixed paths according to GitHub requirements,
while the path to the other five directories can be customized.
As discussed before,
[Customizing the path to the control center directory](/manual/control/structure/index.md#location)
requires a configuration file outside the control center directory.
The path to the remaining four directories,
i.e., the [source](/manual/fundamentals/structure/source.md),
[tests](/manual/fundamentals/structure/tests.md),
[website](/manual/fundamentals/structure/website.md), and
[local](/manual/fundamentals/structure/local.md) directories,
along with the paths to subdirectories of the local directory,
can be customized using the `path.yaml` file
in your repository's control center, as described in this section.

All paths are relative to the root of the repository.

The `local` key accepts an object with
keys `root`, `cache`, and `report`. The `root` key must be set to a string defining
the path to the local directory itself. The `cache` and `report` keys
correspond to the cache and report subdirectories of the local directory;
they accept an object with a key `root` that must be set to a string defining
the path to the corresponding subdirectory, relative to the root of the local directory.
In addition, they each define paths to other subdirectories of the corresponding cache/report subdirectory,
each used for a specific tool. By default, the following keys are defined
for both the `cache` and `report` subdirectories: `repodynamics`, `coverage`, `mypy`, `pylint`,
`pytest`, and `ruff`. Each of these keys must be set to a string defining the path
to the cache/report subdirectory for that tool,
relative to the root of the corresponding cache/report subdirectory.

You can also add other custom keys under `dir.local.cache` and `dir.local.report`
for other tools that you use, and reference them in the corresponding configuration files.
Note that you do not have to specify all keys in the `path.yaml` file;
for all keys that are not specified, |{{ccc.name}}| will use the default values.
Also, you can entirely omit the `path.yaml` file if you do not want to customize any paths.


For example, if you only want to
- change the path of the source directory to `my_source_directory`,
- change the path of the cache subdirectory to `my_cache_directory`, and
- add a new subdirectory `my_tool_subdirectory` under the report subdirectory
for the tool `my_tool`,

:::{admonition} Important Considerations
:class: important

- You must also manually create/rename/move the corresponding directories to match the set path,
in the same commit where you create/modify/delete the `path.yaml` file.
- All four main directories must be orthogonal to all other
[main directories](/manual/fundamentals/structure/index.md) in your repository,
meaning that they cannot be a subdirectory of any other main directory.
:::

|{{ccc.name}}| automatically manages a variety of files in your repository's main directories,
and performs a number of tasks that require access to these files.
For example, to run your tests and build your website, |{{ccc.name}}| needs to know
the path to tests and website directories. In addition, these paths are used as
substitutions in a number of other configuration files for your project,
so that you do not have to manually update these files when you change a path.
The following are just a few examples of configuration files where these paths are used:

:::{code-block} toml
:caption: 🗂 `package_python/build.toml`
[tool.setuptools.packages.find]
where = [ "${‎{ dir.pkg.source }}$" ]

[tool.versioningit.onbuild]
source-file = "${‎{ dir.pkg.source }}$/${‎{ package.name }}$/__init__.py"
:::

:::{code-block} toml
:caption: 🗂 `package_python/tools/mypy.toml`
[tool.mypy]
cache_dir = "${‎{ dir.local.cache.mypy }}$"
any_exprs_report = "${‎{ dir.local.report.mypy }}$"
html_report = "${‎{ dir.local.report.mypy }}$"
linecount_report = "${‎{ dir.local.report.mypy }}$"
linecoverage_report = "${‎{ dir.local.report.mypy }}$"
lineprecision_report = "${‎{ dir.local.report.mypy }}$"
txt_report = "${‎{ dir.local.report.mypy }}$"
:::


:::{code-block} toml
:caption: 🗂 `package_python/tools/ruff.toml`
[tool.ruff]
cache-dir = "${‎{ dir.local.cache.ruff }}$"
:::

:::{code-block} yaml
:caption: 🗂 `ui/web.yaml`
readthedocs:
conda:
    environment: ${‎{ dir.web }}$/requirements.yaml
sphinx:
    configuration: ${‎{ dir.web }}$/source/conf.py
:::

:::{code-block} text
📦 <REPOSITORY-ROOT>
┃
┗ 🗂 .local
    ┃
    ┣ 🗂 cache
    ┃ ┃
    ┃ ┣ 🗂 coverage
    ┃ ┃
    ┃ ┣ 🗂 mypy
    ┃ ┃
    ┃ ┣ 🗂 pylint
    ┃ ┃
    ┃ ┣ 🗂 pytest
    ┃ ┃
    ┃ ┣ 🗂 repodynamics
    ┃ ┃
    ┃ ┗ 🗂 ruff
    ┃
    ┗ 🗂 report
    ┃
    ┣ 🗂 coverage
    ┃
    ┣ 🗂 mypy
    ┃
    ┣ 🗂 pylint
    ┃
    ┣ 🗂 pytest
    ┃
    ┣ 🗂 repodynamics
    ┃
    ┗ 🗂 ruff
:::