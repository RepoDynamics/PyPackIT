# Configurations and Metadata

Almost all of the configurations and metadata are stored in YAML files.
To learn more about the YAML file format,
see [Learn YAML in Y Minutes](https://learnxinyminutes.com/docs/yaml/), or check out the
full specification at [yaml.org](https://yaml.org/spec/1.2.2/).

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
 ┃ ┣ 📄 <a href="dev/branches" title="Branches">branches.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="dev/changelogs" title="Changelogs">changelogs.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="dev/commits" title="Commits">commits.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="dev/discussions" title="Discussions">discussions.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="dev/issues" title="Issues">issues.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="dev/labels" title="Labels">labels.yaml</a>
 ┃ ┃ 
 ┃ ┣ 📄 <a href="dev/maintainers" title="Maintainers">maintainers.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="dev/pulls" title="Pull Requests">pulls.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="dev/repo" title="Repository">repo.yaml</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="dev/tags" title="Tags">tags.yaml</a>
 ┃ ┃
 ┃ ┗ 📄 <a href="dev/workflows" title="Workflows">workflows.yaml</a>
 ┃
 ┣ 🗂 <a href="package" title="Package">package</a>
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
 ┃ ┣ 🗂 <a href="ui/logo" title="Logo">logo</a>
 ┃ ┃ ┃
 ┃ ┃ ┣ 📄 <a href="" title="">full_dark.svg</a>
 ┃ ┃ ┃
 ┃ ┃ ┣ 📄 <a href="" title="">full_light.png</a>
 ┃ ┃ ┃
 ┃ ┃ ┣ 📄 <a href="" title="">full_light.svg</a>
 ┃ ┃ ┃
 ┃ ┃ ┣ 📄 <a href="" title="">icon.png</a>
 ┃ ┃ ┃
 ┃ ┃ ┣ 📄 <a href="" title="">simple_dark.svg</a>
 ┃ ┃ ┃
 ┃ ┃ ┗ 📄 <a href="" title="">simple_light.svg</a>
 ┃ ┃
 ┃ ┣ 📄 <a href="ui/health_files" title="Health Files">health_files.yaml</a>
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
 ┗ 📄 <a href="paths" title="Repository Paths">paths.yaml</a>
</pre>


:::{toctree}
:hidden:

paths
extensions
config
core/index
dev/index
package/index
ui/index
:::
