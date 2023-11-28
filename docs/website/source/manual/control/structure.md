# Structure and Location

To change the path of the `meta` directory (default: `./.meta`),
create a file at `./.github/.repodynamics_meta_path.txt`
and put the new path (relative to the root of repository) in it.
Example:

:::{code-block}
:caption: 🗂 `./.github/.repodynamics_meta_path.txt`
some_directory/my_custom_meta_directory
:::


## Structure

Almost all of the configurations and metadata are stored in YAML files.

:::{admonition} Learn more about YAML and TOML formats
:class: seealso
To learn more about the YAML file format,
see [Learn YAML in Y Minutes](https://learnxinyminutes.com/docs/yaml/), or check out the
full specification at [yaml.org](https://yaml.org/spec/1.2.2/).
To learn more about the TOML file format,
see [Learn TOML in Y Minutes](https://learnxinyminutes.com/docs/toml/), or check out the
full specification at [toml.io](https://toml.io/en/v1.0.0).
:::



<pre>
📦 meta
 ┃
 ┣ 🗂 <a href="core" title="Core Metadata">core</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="core/credits" title="Project Credits">credits.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="core/intro" title="Project Introduction">intro.yaml</a>
 ┃ ┃
 ┃ ┗ 📄 <a href="core/license" title="License and Copyright">license.yaml</a>
 ┃
 ┣ 🗂 <a href="dev" title="Development Configurations">dev</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="dev/branch" title="Branches">branch.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="dev/changelog" title="Changelogs">changelog.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="dev/commit" title="Commits">commit.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="dev/discussion" title="Discussions">discussion.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="dev/issue" title="Issues">issue.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="dev/label" title="Labels">label.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="dev/maintainer" title="Maintainers">maintainer.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="dev/pull" title="Pull Requests">pull.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="dev/repo" title="Repository">repo.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="dev/tag" title="Tags">tag.yaml</a>
 ┃ ┃
 ┃ ┗ 📄 <a href="dev/workflow" title="Workflows">workflow.yaml</a>
 ┃
 ┣ 🗂 <a href="package" title="Package">package_python</a>
 ┃ ┃
 ┃ ┣ 🗂 <a href="" title="">tools</a>
 ┃ ┃ ┃
 ┃ ┃ ┣ 📄 <a href="" title="">bandit.toml</a>
 ┃ ┃ ┃
 ┃ ┃ ┣ 📄 <a href="" title="">black.toml</a>
 ┃ ┃ ┃
 ┃ ┃ ┣ 📄 <a href="" title="">isort.toml</a>
 ┃ ┃ ┃
 ┃ ┃ ┣ 📄 <a href="" title="">mypy.toml</a>
 ┃ ┃ ┃
 ┃ ┃ ┣ 📄 <a href="" title="">pylint.toml</a>
 ┃ ┃ ┃
 ┃ ┃ ┣ 📄 <a href="" title="">pytest.toml</a>
 ┃ ┃ ┃
 ┃ ┃ ┗ 📄 <a href="" title="">ruff.toml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="" title="">build.toml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="" title="">build_tests.toml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="" title="">conda.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="" title="">dev_config.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="" title="">docs.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="" title="">entry_points.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="" title="">metadata.yaml</a>
 ┃ ┃
 ┃ ┗ 📄 <a href="" title="">requirements.yaml</a>
 ┃
 ┣ 🗂 <a href="ui" title="User Interfaces">ui</a>
 ┃ ┃
 ┃ ┣ 🗂 <a href="ui/branding" title="Branding">branding</a>
 ┃ ┃ ┃
 ┃ ┃ ┣ 📄 <a href="ui/branding#favicon" title="">favicon.png</a>
 ┃ ┃ ┃
 ┃ ┃ ┣ 📄 <a href="ui/branding#icon" title="">icon.png</a>
 ┃ ┃ ┃
 ┃ ┃ ┣ 📄 <a href="" title="">logo_full_dark.svg</a>
 ┃ ┃ ┃
 ┃ ┃ ┣ 📄 <a href="" title="">logo_full_light.svg</a>
 ┃ ┃ ┃
 ┃ ┃ ┣ 📄 <a href="" title="">logo_full_light.png</a>
 ┃ ┃ ┃
 ┃ ┃ ┣ 📄 <a href="" title="">logo_simple_dark.svg</a>
 ┃ ┃ ┃
 ┃ ┃ ┣ 📄 <a href="" title="">logo_simple_light.svg</a>
 ┃ ┃ ┃
 ┃ ┃ ┗ 📄 <a href="" title="">social_preview.png</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="ui/health_file" title="Health Files">health_file.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="ui/readme" title="Readme Files">readme.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="ui/theme" title="Theme">theme.yaml</a>
 ┃ ┃
 ┃ ┗ 📄 <a href="ui/web" title="Website">web.yaml</a>
 ┃
 ┣ 📄 <a href="config" title="Base Configurations">config.yaml</a>
 ┃
 ┣ 📄 <a href="extensions" title="Meta Extensions">extensions.yaml</a>
 ┃
 ┗ 📄 <a href="path" title="Repository Paths">path.yaml</a>
</pre>
