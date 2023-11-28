# Repository Structure

:::{toctree}
:hidden:

meta
github
source
tests
website
docs
local
root
:::

In addition to several [files in the root directory](root),
{{ pp_meta.name }} recognizes and works with six main directories and their contents in your repository:

- [Meta](meta): The main control center of the repository,
  containing all information, configurations and metadata for the entire project.
- [GitHub](github): The directory where GitHub looks for GitHub Actions workflow files
  and other configuration files.
  {{pp_meta.name}} also uses this directory to store some of its own data and settings,
  as well as configuration files for other external tools.
- [Source](source): Contains the top-level package directory and thus all source code of your package.
- [Tests](tests): Contains your package's entire test suite as a standalone Python package.
- [Website](website): All contents and configuration files required to build your website
  are stored in this directory.
- [Docs](docs): One of the directories where GitHub looks for
  the community health files of your repository,
  along with some other configuration files.
  By default, {{pp_meta.name}} also places the website directory inside this directory.
- [Local](local): When working on a local clone of the repository,
  this directory is used to store cached data, reports, and logs. 

These directories all have their default names and locations,
and are created automatically when you initialize a new repository
from the {{pp_meta.name}} repository template.
Therefore, your repository will have the following
main directory structure (files and subdirectories omitted) by default:

<pre>
📦 <a href="root" title="Root Files">&lt;root&gt;</a>
 ┃
 ┣ 🗂 <a href="github" title="GitHub Directory">.github</a>
 ┃
 ┣ 🗂 <a href="local" title="Local Directory">.local</a>
 ┃
 ┣ 🗂 <a href="meta" title="Meta Directory">.meta</a>
 ┃
 ┣ 🗂 <a href="docs" title="Docs Directory">docs</a>
 ┃ ┃
 ┃ ┗ 🗂 <a href="website" title="Website Directory">website</a>
 ┃
 ┣ 🗂 <a href="source" title="Source Directory">src</a>
 ┃
 ┗ 🗂 <a href="tests" title="Tests Directory">tests</a>
</pre>

Apart from the GitHub and Docs directories, whose names and locations are fixed due to GitHub's requirements,
you can [customize the paths](../../control/options/path.md) to all other directories,
including the [meta directory](../../control/location.md).
However, each directory must still conform to a specific substructure,
meaning that {{pp_meta.name}} will look for specific files and subdirectories
in specific locations inside each directory, as described in the corresponding sections.
