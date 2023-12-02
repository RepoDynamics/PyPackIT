# Repository Structure

:::{toctree}
:hidden:

control
github
source
tests
website
docs
local
root
:::


In addition to several files in the root directory,
{{ pp_meta.name }} recognizes and works with seven main directories
and their contents in your repository:


::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} Control Center Directory
:link: control
:link-type: doc
:class-title: sd-text-center

The main control center of the repository,
containing all information, configurations and metadata for the entire project.
:::

:::{grid-item-card} GitHub Directory
:link: github
:link-type: doc
:class-title: sd-text-center

The directory where GitHub looks for GitHub Actions workflow files and other configuration files.
{{pp_meta.name}} also uses this directory to store some of its own data and settings,
as well as configuration files for other external tools.
:::

:::{grid-item-card} Source Directory
:link: source
:link-type: doc
:class-title: sd-text-center

Contains the top-level package directory and thus all source code of your package.
:::

:::{grid-item-card} Tests Directory
:link: tests
:link-type: doc
:class-title: sd-text-center

Contains your package's entire test suite as a standalone Python package.
:::

:::{grid-item-card} Website Directory
:link: website
:link-type: doc
:class-title: sd-text-center

All contents and configuration files required to build your website are stored in this directory.
:::

:::{grid-item-card} Docs Directory
:link: docs
:link-type: doc
:class-title: sd-text-center

One of the directories where GitHub looks for
the community health files of your repository,
along with some other configuration files.
By default, {{pp_meta.name}} also places the website directory inside this directory.
:::

:::{grid-item-card} Local Directory
:link: local
:link-type: doc
:class-title: sd-text-center

When working on a local clone of the repository,
this directory is used to store cached data, reports, and logs.
:::

:::{grid-item-card} Root Files
:link: root
:link-type: doc
:class-title: sd-text-center

{{pp_meta.name}} also recognizes and works with several files in the root directory of your repository.
:::

::::


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
 ┣ 🗂 <a href="control" title="Control Center Directory">.meta</a>
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
you can [customize the paths](../../control/options/path/index.md) to all other directories,
including the [control center directory](../../control/structure/index.md#location).
However, **each directory must conform to a specific substructure**,
meaning that {{pp_meta.name}} will look for specific files and subdirectories
in specific locations inside each directory, as described in the corresponding sections.
Also, **all directories must be orthogonal to each other**,
meaning that none of them can be a subdirectory of another.
