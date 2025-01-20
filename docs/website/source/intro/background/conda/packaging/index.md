(bg-conda-packaging)=
# Packaging and Distribution

The (Ana)conda ecosystem provides a robust infrastructure 
for packaging and distributing software
spanning multiple languages, including Python, R, C, and C++.
Unlike Python’s native ecosystem, 
which primarily targets Python packages,
Conda offers a more expansive approach with cross-language compatibility, 
environment isolation, and efficient dependency management. 

This section delves into the details of 
the packaging and distribution process in the Conda ecosystem, 
highlighting relevant parallels and contrasts with [Python's native process](#bg-packaging).


:::{admonition} Learn More
:class: seealso

For more detailed information, see:
- [Conda-build Documentation](https://docs.conda.io/projects/conda-build/en/stable/)---The official documentation for building Conda packages.
- [Conda-forge Documentation](https://www.pyopensci.org/python-package-guide/)---The official documentation for contributing Conda packages to the conda-forge repository.
- [Anaconda.org Documentation](https://docs.anaconda.com/anacondaorg/user-guide/packages/)---The official documentation for building and uploading packages to Anaconda.org.
:::


## Package Structure

[Conda packages](https://docs.conda.io/projects/conda/en/stable/user-guide/concepts/packages.html)
are compressed archives that can contain different types of files
from package metadata, Python modules, and other source files,
to system-level libraries and executable programs.
Therefore, a conda package can be anything from a pure-Python package
(called a 
[Noarch](https://docs.conda.io/projects/conda/en/stable/user-guide/concepts/packages.html#noarch-python) 
package in conda)
to complex applications containing multiple platform-specific binaries.
Since Conda packages are language-agnostic, they also do not impose
a specific [import package](#bg-pkg-structure) structure.


(bg-conda-recipe)=
## Configuration and Metadata

Similar to the [`pyproject.toml` file](#bg-pyproject) for Python packages,
Conda packages must define build settings and package metadata
in a so-called [Conda-build recipe](https://docs.conda.io/projects/conda-build/en/stable/concepts/recipe.html),
consisting of a [`meta.yaml` file](https://docs.conda.io/projects/conda-build/en/stable/resources/define-metadata.html) written in [YAML](#bg-yaml)
plus other optional files such as 
[build scripts](https://docs.conda.io/projects/conda-build/en/stable/resources/build-scripts.html)
for Unix and Windows-based systems.
Conda-build recipes and `pyproject.toml` files share many configurations
like package name, version, and other descriptors,
but differ in defining the build process.

While `pyproject.toml` files are only meant for Python packages,
Conda-build recipes can be used to build any software and
thus offer a more generic solution.
In contrast to `pyproject.toml` files that can only build
Python packages located at the same filepath,
Conda-build recipes allow users to dynamically
collect the required [source](https://docs.conda.io/projects/conda-build/en/stable/resources/define-metadata.html#source-section)
files from any online or local location.
The recipe must then define a [build script](https://docs.conda.io/projects/conda-build/en/stable/resources/define-metadata.html#build-section), 
in which files are installed into an isolated build environment.
For example, to build a Python package,
this involves using [pip](#bg-pip) to install the package into the build environment.
Conda will then bundle all files added to the build environment into a Conda package,
along with package metadata defined in the recipe.


## Build

The [build process](https://docs.conda.io/projects/conda-build/en/stable/user-guide/tutorials/build-pkgs.html) 
in the Conda ecosystem involves converting source code 
and dependencies into a distributable binary package. 
This is achieved using the [conda-build](https://github.com/conda/conda-build) tool, 
which automates the creation of [`.conda` files](https://docs.conda.io/projects/conda/en/latest/user-guide/concepts/packages.html#conda-file-format)
(superseding the older `.tar.bz2` format) optimized for fast installation.
This generates platform-specific binaries that are ready for distribution. 
Unlike Python’s reliance on `wheel` for binary distributions, 
Conda packages inherently bundle all required dependencies, 
including compiled libraries, 
which ensures smooth installation regardless of the target environment.


## Publication

Once a package is built, it can be published 
to repositories like [Anaconda.org](#bg-anaconda-org) or [conda-forge](#bg-conda-forge). 
For Anaconda.org, developers must [create an account](https://docs.anaconda.com/free/anacondaorg/user-guide/work-with-accounts/)
on the platform and use the [anaconda-client](https://github.com/Anaconda-Platform/anaconda-client) library
to [upload the package](https://docs.anaconda.com/free/anacondaorg/user-guide/packages/conda-packages/#uploading-conda-packages)
to their Anaconda.org repository/channel, similar to how [twine](#bg-packaging-publish) is used for [PyPI](#bg-pypi).

Developers are also encouraged to publish to the [conda-forge](#bg-conda-forge)
community repository, which provides a curated collection of high-quality packages
that are automatically built and tested on a variety of platforms.
Conda-forge has its own process for [contributing packages](https://conda-forge.org/docs/maintainer/adding_pkgs.html),
which involves submitting a Conda-build recipe
to the [staged-recipes repository](https://github.com/conda-forge/staged-recipes) on GitHub,
where it is reviewed and tested by the community before being merged into the repository.
Once merged, the package is automatically built and uploaded to the conda-forge channel,
and made available to the users.
