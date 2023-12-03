# Structure and Location
Your repository's control center is a directory in your repository,
where all contents are organized in a specific directory structure,
and categorized and stored in various files; these are mostly in YAML format, except
a few `pyproject.toml`-related options that are stored in TOML format,
and some media files in SVG and PNG formats.
Applying changes in the control center is thus as simple as editing the corresponding files
and pushing the changes to your repository.

:::{admonition} Learn YAML & TOML
:class: seealso
To learn more about the YAML file format,
see [Learn YAML in Y Minutes](https://learnxinyminutes.com/docs/yaml/), or check out the
full specification at [yaml.org](https://yaml.org/spec/1.2.2/).
Similarly, for the TOML file format,
see [Learn TOML in Y Minutes](https://learnxinyminutes.com/docs/toml/), or check out the
full specification at [toml.io](https://toml.io/en/v1.0.0).
:::


## Location
By default, the control center is located at `./.meta`, i.e., a directory named `.meta`
placed at the root of your repository.
You can customize the location of this directory
by creating a file at `{{ pp_meta.custom.path.file_path_meta }}`
containing the new path, relative to the root of your repository.

::::{dropdown} Example

To change the location of the control center directory to `./some_directory/my_custom_meta_directory`,
move the control center directory to this new location,
and create a file at `{{ pp_meta.custom.path.file_path_meta }}` containing only a single line
as shown below:

:::{code-block} text
:caption: 🗂 `{{ pp_meta.custom.path.file_path_meta }}`

some_directory/my_custom_meta_directory
:::

::::


If this file exists, {{ pp_meta.name }} will look for the control center directory
at the path specified in the file,
otherwise, it will look for it at the default location, i.e., at `./.meta`.


:::{admonition} Important Considerations
:class: important

- You must also manually rename/move the control center directory to match the new path
  in the same commit where you create/modify/delete the path declaration file.
- The control center directory must be orthogonal to all other
  [main directories](/manual/fundamentals/structure/index.md) in your repository,
  meaning that it cannot be a subdirectory of any other main directory.
:::


## Structure

The control center directory has a fixed pre-defined structure, shown below.
Note that your repository's control center does not need to contain all these files and directories;
almost all configuration files have default values that are automatically used by {{ pp_meta.name }}
when the corresponding file is not present.
On the other hand, except additional
TOML files that can be placed under the `package_python/tools` subdirectory,
you cannot add any additional files or directories to the control center;
{{ pp_meta.name }} will ignore any files or directories
that are not part of the control center structure below.


:::{card}
Directory structure of your repository's control center.
Click on any file or directory name to learn more about it
in the corresponding section under [Options](../options/index.md).
^^^

<pre>
📦 &lt;CONTROL-CENTER-DIRECTORY&gt;
 ┃
 ┣ 🗂 <a href="/manual/control/options/project" title="Project Information">project</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="/manual/control/options/project/credits" title="Project Credits">credits.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="/manual/control/options/project/intro" title="Project Introduction">intro.yaml</a>
 ┃ ┃
 ┃ ┗ 📄 <a href="/manual/control/options/project/license" title="License and Copyright">license.yaml</a>
 ┃
 ┣ 🗂 <a href="/manual/control/options/custom" title="Custom Metadata">custom</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="/manual/control/options/custom/#static-variables" title="Static Custom Variables">custom.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="/manual/control/options/custom/#dynamic-variables" title="Dynamic Custom Variables">generator.py</a>
 ┃ ┃
 ┃ ┗ 📄 <a href="/manual/control/options/custom/#requirements" title="Requirements">requirements.txt</a>
 ┃
 ┣ 🗂 <a href="/manual/control/options/dev" title="Development Configurations">dev</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="/manual/control/options/dev/branch" title="Branches">branch.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="/manual/control/options/dev/changelog" title="Changelogs">changelog.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="/manual/control/options/dev/commit" title="Commits">commit.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="/manual/control/options/dev/discussion" title="Discussions">discussion.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="/manual/control/options/dev/issue" title="Issues">issue.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="/manual/control/options/dev/label" title="Labels">label.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="/manual/control/options/dev/maintainer" title="Maintainers">maintainer.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="/manual/control/options/dev/pull" title="Pull Requests">pull.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="/manual/control/options/dev/repo" title="Repository">repo.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="/manual/control/options/dev/tag" title="Tags">tag.yaml</a>
 ┃ ┃
 ┃ ┗ 📄 <a href="/manual/control/options/dev/workflow" title="Workflows">workflow.yaml</a>
 ┃
 ┣ 🗂 <a href="/manual/control/options/package" title="Package">package_python</a>
 ┃ ┃
 ┃ ┣ 🗂 <a href="/manual/control/options/package/tools" title="">tools</a>
 ┃ ┃ ┃
 ┃ ┃ ┣ 📄 <a href="/manual/control/options/package/tools/#bandit" title="">bandit.toml</a>
 ┃ ┃ ┃
 ┃ ┃ ┣ 📄 <a href="/manual/control/options/package/tools/#black" title="">black.toml</a>
 ┃ ┃ ┃
 ┃ ┃ ┣ 📄 <a href="/manual/control/options/package/tools/#isort" title="">isort.toml</a>
 ┃ ┃ ┃
 ┃ ┃ ┣ 📄 <a href="/manual/control/options/package/tools/#mypy" title="">mypy.toml</a>
 ┃ ┃ ┃
 ┃ ┃ ┣ 📄 <a href="/manual/control/options/package/tools/#pylint" title="">pylint.toml</a>
 ┃ ┃ ┃
 ┃ ┃ ┣ 📄 <a href="/manual/control/options/package/tools/#pytest" title="">pytest.toml</a>
 ┃ ┃ ┃
 ┃ ┃ ┣ 📄 <a href="/manual/control/options/package/tools/#ruff" title="">ruff.toml</a>
 ┃ ┃ ┃
 ┃ ┃ ┗ 📄 <a href="/manual/control/options/package/tools/#additional-files" title="">*.toml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="/manual/control/options/package/build" title="">build.toml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="/manual/control/options/package/build_tests" title="">build_tests.toml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="/manual/control/options/package/conda" title="">conda.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="/manual/control/options/package/dev_config" title="">dev_config.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="/manual/control/options/package/docs" title="">docs.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="/manual/control/options/package/entry_points" title="">entry_points.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="/manual/control/options/package/metadata" title="">metadata.yaml</a>
 ┃ ┃
 ┃ ┗ 📄 <a href="/manual/control/options/package/requirements" title="">requirements.yaml</a>
 ┃
 ┣ 🗂 <a href="/manual/control/options/ui" title="User Interfaces">ui</a>
 ┃ ┃
 ┃ ┣ 🗂 <a href="/manual/control/options/ui/branding" title="Branding">branding</a>
 ┃ ┃ ┃
 ┃ ┃ ┣ 📄 <a href="/manual/control/options/ui/branding#favicon" title="">favicon.png</a>
 ┃ ┃ ┃
 ┃ ┃ ┣ 📄 <a href="/manual/control/options/ui/branding/#icon" title="">icon.png</a>
 ┃ ┃ ┃
 ┃ ┃ ┣ 📄 <a href="/manual/control/options/ui/branding/#" title="">logo_full_dark.svg</a>
 ┃ ┃ ┃
 ┃ ┃ ┣ 📄 <a href="/manual/control/options/ui/branding/#" title="">logo_full_light.svg</a>
 ┃ ┃ ┃
 ┃ ┃ ┣ 📄 <a href="/manual/control/options/ui/branding/#" title="">logo_full_light.png</a>
 ┃ ┃ ┃
 ┃ ┃ ┣ 📄 <a href="/manual/control/options/ui/branding/#" title="">logo_simple_dark.svg</a>
 ┃ ┃ ┃
 ┃ ┃ ┣ 📄 <a href="/manual/control/options/ui/branding/#" title="">logo_simple_light.svg</a>
 ┃ ┃ ┃
 ┃ ┃ ┗ 📄 <a href="/manual/control/options/ui/branding/#social-preview" title="">social_preview.png</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="/manual/control/options/ui/health_file" title="Health Files">health_file.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="/manual/control/options/ui/readme" title="Readme Files">readme.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="/manual/control/options/ui/theme" title="Theme">theme.yaml</a>
 ┃ ┃
 ┃ ┗ 📄 <a href="/manual/control/options/ui/web" title="Website">web.yaml</a>
 ┃
 ┣ 📄 <a href="/manual/control/options/config" title="Base Configurations">config.yaml</a>
 ┃
 ┣ 📄 <a href="/manual/control/options/extensions" title="Meta Extensions">extensions.yaml</a>
 ┃
 ┗ 📄 <a href="/manual/control/options/path" title="Repository Paths">path.yaml</a>
</pre>

:::
