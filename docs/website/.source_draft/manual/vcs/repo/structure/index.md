(repo-structure)=
# Structure

The directory structure of the repository defines the layout
  and the overall organization of the project; it is an important factor that can have a significant impact
  on the development process and maintainability of the project.
  A well-structured repository should have a clear directory structure,
  with a logical separation between different components of the project,
  and a consistent and standardized naming scheme for files and directories.
  This makes it easier for developers to navigate the repository,
  locate the relevant files, and understand the overall structure of the project.
  In addition, GitHub and many other tools and services that are commonly used in the project development
  process rely on the repository's structure to locate and identify various components of the project.
  This requires developers to follow a specific directory structure and naming scheme
  when setting up their repositories, so that these tools can locate the relevant files and directories
  needed for their operation.
  Moreover, the repository structure is one of the first things that users notice when visiting the repository,
  and thus plays a vital role in establishing the project's credibility and professionalism.

In addition to several files in the root directory,
|{{ ccc.name }}| recognizes and works with seven main directories
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
|{{ccc.name}}| also uses this directory to store some of its own data and settings,
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
By default, |{{ccc.name}}| also places the website directory inside this directory.
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

|{{ccc.name}}| also recognizes and works with several files in the root directory of your repository.
:::

::::


These directories all have their default names and locations,
and are created automatically when you initialize a new repository
from the |{{ccc.name}}| repository template.
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
meaning that |{{ccc.name}}| will look for specific files and subdirectories
in specific locations inside each directory, as described in the corresponding sections.
Also, **all directories must be orthogonal to each other**,
meaning that none of them can be a subdirectory of another.


## GitHub Directory

Every repository must contain a `./.github` directory,
i.e., a directory named `.github` located at the root (`./`) of the repository.
This is where GitHub looks for GitHub Actions workflow files
(`.yaml` files in the `./.github/workflows` directory) and other configuration files,
such as issue-, discussion-, and pull request templates.

When a repository is first initialized from the |{{ccc.name}}| template,
the `./.github` directory will only contain workflow files.
These are configurations that define the continuous integration and delivery (CI/CD)
pipelines of the repository, allowing the whole development and maintenance process of your project
to be automatically managed by |{{ccc.name}}|.
In general, you should never modify these files directly, since all configurations and data that
are specific to each project are read automatically from the repository's `meta` content (discussed below).
The only exception is when you want to add a new feature/functionality to your pipelines,
which is not covered by |{{ccc.name}}| and is completely orthogonal to its functionalities.

After the repository is configured, a number of other files and directories
will also be automatically added to the `./.github` directory,
including issue-, discussion-, and pull request templates, and other GitHub configuration files.
|{{ccc.name}}| also uses the `./.github` directory to store some of its own data and settings,
as well as configuration files for other external tools that are used by |{{ccc.name}}|.
You must never modify these files directly, as they are dynamic files that are automatically
generated and updated by |{{ccc.name}}| according to the repository's `meta` content.


## Control Center Directory

The meta directory is the main control center of your repository,
where all configurations, metadata, and settings
for your GitHub repository (and its corresponding git repository),
package, website, development pipeline, and other tools are stored in one place.
When you apply a change to the repository's `meta` content and push it to the remote repository,
|{{ccc.name}}| will automatically apply the corresponding changes to entire repository and its content,
so that the repository is always in a consistent state with its `meta` content.
This is the main mechanism that |{{ccc.name}}| uses to manage your repository and project,
so you must never modify any configuration directly, but always through the `meta` content.

This directory is named `.meta` by default, and is located at the root of the repository.
You can change the name and location of your repository's `meta` directory,
but it must have a specific substructure, meaning that |{{ccc.name}}| will look for
specific files and directories in specific locations inside the `meta` directory
to read the corresponding configurations and data from.

## Local Directory

This directory is used to store local files,
such as cache files, logs and reports from various tools.
It will be automatically added to the `.gitignore` file.

## Source Directory

The `source` directory is where all source code of your package is stored.
This directory is named `src` by default, and is located at the root of the repository.
However, you can change its name and location via the `meta` content.
|{{ccc.name}}| follows the
[Setuptools's src-layout](https://setuptools.pypa.io/en/latest/userguide/package_discovery.html#src-layout)
for package discovery.
This means that your `source` directory must contain a single top-level package directory,
which must at least contain a `__init__.py` file. The name of this top-level package directory
defines the import name of your package. You must never rename the top-level package directory directly;
instead, |{{ccc.name}}| will automatically rename it for you
when you change the package name in the `meta` content. |{{ccc.name}}| will also automatically
update all import statements in your source code to reflect the new package name.

When the repository is first initialized, |{{ccc.name}}| will automatically create the `source` directory
and the top-level package directory, along with the top-level `__init__.py` file.
Note that the docstring of the top-level `__init__.py` file is also dynamic. Therefore, while you can
change the content of the `__init__.py` file, you must never change the docstring directly, but always
through the `meta` content.


(manual-repo-cache-dir)=
## Cache Directory




:::{admonition} Important Considerations
:class: important

- You must also manually rename/move the control center directory to match the new path
  in the same commit where you create/modify/delete the path declaration file.
- The control center directory must be orthogonal to all other
  [main directories](/manual/fundamentals/structure/index.md) in your repository,
  meaning that it cannot be a subdirectory of any other main directory.
:::
