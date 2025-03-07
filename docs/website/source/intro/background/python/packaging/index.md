(bg-packaging)=
# Packaging and Distribution

Packaging and distributing Python applications
ensures that software can be easily shared,
installed, and run across different environments.
This process involves preparing code
for public or private distribution
while handling dependencies and configurations
in a standardized way.
Effective packaging streamlines deployment,
fosters collaboration, and enables scalability
by providing consistent methods for delivering software.

The packaging and distribution process involves several key steps,
each playing a critical role in ensuring compatibility,
reliability, and ease of use for end users.
These include preparing import packages, configuring metadata,
building the package, and publishing it to indexing repositories
like [PyPI](#bg-pypi) and [Anaconda.org](#bg-anaconda-org).
Users can then download and install the package on their machines
using supported package management systems such as [pip](#bg-pip).
for PyPI and [conda](#bg-conda) or [mamba](#bg-mamba) for Anaconda.org.

The rest of this page provides a general overview
of key steps in the packaging and distribution of Python packages.
For information about Conda packages, see [Packaging and Distribution](#bg-conda-packaging)
in the Anaconda ecosystem.


:::{admonition} Learn More
:class: seealso

For more detailed information, see:
- [Python Packaging User Guide](https://packaging.python.org)---The official Python packaging guide by PyPA.
- [pyOpenSci Python Package Guide](https://www.pyopensci.org/python-package-guide/)---Packaging guides and tutorials for scientific packages by the [pyOpenSci](https://www.pyopensci.org/python-packaging-science.html) community.
:::


(bg-pkg-structure)=
## Package Structure

The first step in packaging involves
organizing the project’s code into one or several
[import packages](https://packaging.python.org/en/latest/glossary/#term-Import-Package).
This requires developers to follow a specific directory structure and naming scheme,
so that the package and its components can be correctly recognized
by [Python's import system](https://docs.python.org/3/reference/import.html).
Organizing code into reusable and logically structured packages
also makes it easier for developers to maintain and extend their projects.
Moreover, proper use of namespaces and directory structures
is essential for clarity and functionality.

Python packages are directories containing a special `__init__.py` file
(except for [namespace packages](https://packaging.python.org/en/latest/guides/packaging-namespace-packages/)),
which marks them as importable modules.
The name of this directory defines the import name of the package,
and must be a valid [Python identifier](https://docs.python.org/3/reference/lexical_analysis.html#identifiers)
and should follow the [naming conventions](https://www.python.org/dev/peps/pep-0008/#package-and-module-names)
defined in PEP 8.
All the source code of the package must be placed inside this directory,
organized into subpackages and modules, which can be further nested to any depth.


(bg-pyproject)=
## Configuration and Metadata

Import packages must define additional
build settings and package metadata,
allowing them to be built into binaries and installed on other machines.


:::{admonition} History
:class: note dropdown toggle-shown

Previously, building Python packages was done by
[distutils](https://packaging.python.org/en/latest/key_projects/#distutils)---the
original Python packaging system---which used a
[`setup.py` file](https://packaging.python.org/en/latest/discussions/setup-py-deprecated/)
for configurations.
As [Setuptools](https://packaging.python.org/en/latest/key_projects/#setuptools)
started [replacing distutils](https://peps.python.org/pep-0632/),
it added its own [`setup.cfg` file](https://setuptools.pypa.io/en/latest/userguide/declarative_config.html)
to enable declarative configurations in `.ini` format and reduce boilerplate code.
Additionally, [PEP 517](https://peps.python.org/pep-0517/) and
[PEP 518](https://www.python.org/dev/peps/pep-0518/) proposed
standardization of configurations in a build-system independent format,
using a `pyproject.toml` file. First introduced in 2016, this new standard
was established in 2021, after the acceptance and implementation of
[PEP 621](https://www.python.org/dev/peps/pep-0621/) and
[PEP 660](https://www.python.org/dev/peps/pep-0660/).
While `setup.py` and `setup.cfg` files are still valid configuration files for Setuptools,
it is [highly recommended](https://packaging.python.org/en/latest/guides/modernize-setup-py-project/)
to use `pyproject.toml` for defining static configurations and metadata in a declarative format.
:::


All package configurations can be declaratively defined
in the standardized [`pyproject.toml` file specification](https://packaging.python.org/en/latest/specifications/pyproject-toml).
Written in [TOML](#bg-toml) format, the `pyproject.toml` file defines
three main tables for build system dependencies, project metadata, and tool configuration.

### Build System Dependencies

The [`build-system`](https://packaging.python.org/en/latest/specifications/pyproject-toml/#declaring-build-system-dependencies-the-build-system-table)
table can be used to specify dependencies required to execute the build.
This includes the packaging system, e.g., [setuptools](https://setuptools.pypa.io),
[hatch](https://hatch.pypa.io),
[flit](https://flit.pypa.io),
[poetry](https://python-poetry.org),
or [pdm](https://pdm-project.org),
as well as other [build tools](https://packaging.python.org/en/latest/key_projects/)
and plugins, such as [setuptools-scm](https://setuptools-scm.readthedocs.io/en/latest/) for versioning.
The table can also contain specific configurations
for the selected build backend, such as the location of the source code,
files to include/exclude, and how to handle different aspects of the build process.
The exact format and syntax of these configurations depend on the selected build backend.


### Project Metadata

The [`project](https://packaging.python.org/en/latest/specifications/pyproject-toml/#declaring-project-metadata-the-project-table)
table specifies the project's [core metadata](https://packaging.python.org/en/latest/specifications/core-metadata/#core-metadata-specifications),
including:
- [**Name**]{.primary-color}: The name of the package on the online repository,
  used by the package manager to uniquely identify and locate the package.
  The package name must follow the [PyPA specifications](https://packaging.python.org/en/latest/specifications/name-normalization/)
  introduced in [PEP 503](https://peps.python.org/pep-0503/#normalized-names)
  and [PEP 508](https://peps.python.org/pep-0508/#names).
- [**Version**]{.primary-color}: The version identifier of the package, used by the package manager
  to identify and install the correct version of the package.
  It must be a valid public version identifier according to the
  [PyPA specifications](https://packaging.python.org/en/latest/specifications/version-specifiers/#version-specifiers)
  first introduced in [PEP 440](https://www.python.org/dev/peps/pep-0440/),
  and must be incremented for every new release of the package,
  following [specific rules](https://packaging.python.org/en/latest/specifications/version-specifiers/#version-ordering-across-different-metadata-versions).
- [**Python Version**]{.primary-color}: The minimum Python version required by the package,
  used by the package manager to ensure that the package is compatible with the user's Python interpreter.
  It must be a valid version specifier according to the
  [PyPA specifications](https://packaging.python.org/en/latest/specifications/version-specifiers/#id4),
  and must be incremented whenever the package drops support for older Python versions.
- [**Dependencies**]{.primary-color}: The required and optional dependencies of the package
  (i.e., other software that the package depends on to function correctly),
  which are automatically installed by the package manager along with the package.
  These must be specified in a standardized format defined in
  [PEP 508](https://www.python.org/dev/peps/pep-0508/),
  and must be kept up to date and synchronized with the dependencies used in the source code.
  Note that only packages available from PyPI are allowed.
- [**Entry Points**]{.primary-color}: The entry points of the package,
  such as console scripts, GUI scripts, and other callable objects,
  which are automatically registered by the package manager and made available to the user.
  These must follow the [PyPA specifications](https://packaging.python.org/en/latest/specifications/entry-points/),
  and must refer to actual objects (e.g., functions) defined in the source code.

In addition, several other metadata must be provided so that the online package index
can correctly categorize and display the package, facilitating its discovery by users,
and providing them with a clear overview of the project.
These include:
- [**Description**]{.primary-color}: A short description of the package,
  which is displayed on the package index and used by the package manager
  to provide a brief overview of the project.
- [**Keywords**]{.primary-color}: A list of keywords describing the package,
  which are used by the package index to categorize the package,
  and help users find it through various search and filtering options.
- [**License**]{.primary-color}: The license of the package,
  so that users can know under which terms they can use the project.
- [**Authors and Maintainers**]{.primary-color}: Names and emails of the
  authors and maintainers of the package,
  so that users can know who is responsible for the project and how to contact them.
- [**Project URLs**]{.primary-color}: A list of URLs related to the project,
  such as the project's homepage, documentation, source code, issue tracker, and changelog,
  which are displayed on the package index and used by the package manager
  to provide users with additional information and resources for the project.
- [**Classifiers**]{.primary-color}: A list of [Trove classifiers](https://pypi.org/classifiers/)
  as defined in [PEP 301](https://peps.python.org/pep-0301/#distutils-trove-classification),
  to describe each release of the package (e.g., development status, supported Python versions and operating systems,
  project topics, intended audience, natural language, license, etc.).
  These standardized classifiers are used by the package index to categorize the package,
  and help users find it through various search and filtering options.
- [**README**]{.primary-color}: A README file similar to the repository's README,
  containing a detailed and up-to-date description of the package,
  which is displayed on the package index to provide users with a clear overview of the project.
  As the first thing that users notice when viewing the project on the package index,
  it is crucial to have an informative, engaging, and visually appealing README
  that captures the attention of visitors and provides them with all the necessary information
  and resources for the project.
  Both PyPI and Anaconda.org support markup languages such as Markdown and reStructuredText
  for defining the contents of the README file.
  However, like GitHub, they impose several restrictions on the supported features,
  and perform additional post-processing and sanitization after rendering the contents to HTML.
  For example, PyPI uses the [Readme Renderer](https://github.com/pypa/readme_renderer) library
  to render the README file, which only supports a limited subset of HTML
  [tags](https://github.com/pypa/readme_renderer/blob/9c2eb81301bc230f2795cf7e6dc2c23f5815ea41/readme_renderer/clean.py#L20-L31)
  and [attributes](https://github.com/pypa/readme_renderer/blob/9c2eb81301bc230f2795cf7e6dc2c23f5815ea41/readme_renderer/clean.py#L33-L65).
  Since these do not completely overlap with the features supported by GitHub,
  a separate [PyPI-friendly README](https://packaging.python.org/en/latest/guides/making-a-pypi-friendly-readme/)
  must be provided for PyPI, to ensure that the contents are correctly rendered on the package index.


### Tool Configuration

The [`tool`](https://packaging.python.org/en/latest/specifications/pyproject-toml/#arbitrary-tool-configuration-the-tool-table)
table can contain arbitrary configurations for tools and services used in the entire project,
including but not limited to build tools, linters, formatters, and testing tools.
Each tool defines its own configuration structure, which can be added in a sub-table within `tool`.


## Build

Import package(s) must be transformed into
[distribution packages](https://packaging.python.org/en/latest/glossary/#term-Distribution-Package),
which are versioned archives containing the import packages and other required files and resources.
Distribution packages are the files that are actually uploaded to the online package index,
to be downloaded and installed by the end-users via package managers.
There are two major distribution formats for Python packages:

- [**Source Distributions**](https://packaging.python.org/en/latest/specifications/source-distribution-format)
  or [sdists](https://packaging.python.org/en/latest/glossary/#term-Source-Distribution-or-sdist)
  are `tar.gz` archive files providing the source code of the package,
  along with the required configuration files, metadata, and resources
  that are needed for generating various built distributions.
- [**Built Distributions**](https://packaging.python.org/en/latest/glossary/#term-Built-Distribution)
  are [binary archives](https://packaging.python.org/en/latest/specifications/binary-distribution-format/)
  containing files and metadata that only need to be moved to the correct location on the target system,
  to be installed.
  [Wheel](https://packaging.python.org/en/latest/glossary/#term-Wheel) is the standard
  binary distribution format for Python packages, designed to expedite the installation process
  by eliminating the need for building packages from source.
  A wheel archive contains all the necessary files
  for a Python package, including compiled binaries for specific platforms if needed.
  As a platform-independent standard defined in [PEP 427](https://www.python.org/dev/peps/pep-0427/),
  wheels are widely supported by tools like [pip](#bg-pip),
  replacing the older [Egg](https://packaging.python.org/en/latest/glossary/#term-Egg) format.
  Wheels can be either platform-independent or platform-specific,
  depending on whether the package is
  [pure-Python](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#pure-python-wheels)
  or contains compiled extensions.

PyPA [recommends](https://packaging.python.org/en/latest/tutorials/packaging-projects/#generating-distribution-archives)
always uploading a source distribution to PyPI,
along with one or more built distributions for each supported platform.
These can be generated using the [build](https://github.com/pypa/build)
(for source distributions and pure-Python wheels)
and [cibuildwheel](https://github.com/pypa/cibuildwheel) (for platform-specific wheels)
packages provided by PyPA.


(bg-packaging-publish)=
## Publication

The final step in the process involves publishing the package to a repository,
such as [PyPI](#bg-pypi), for distribution.
For PyPI, this requires developers to create an account on the platform,
generate an API token for authentication,
and use the [twine](https://github.com/pypa/twine/) library to upload the packages.
Alternatively, [trusted publishing](https://docs.pypi.org/trusted-publishers/)
([OpenID Connect](https://openid.net/developers/how-connect-works/) standard) can be used
in conjunction with the [PyPI publish GitHub Action](https://github.com/pypa/gh-action-pypi-publish)
to publish packages directly from GitHub Actions, without the need for an API token.

Sdists and wheels can also be published to any other supporting repository.
For example, they can be uploaded to [pypi.anaconda.org](https://docs.anaconda.com/anacondaorg/user-guide/packages/standard-python-packages/)
using the [Anaconda Client](https://docs.anaconda.com/anacondaorg/user-guide/getting-started-with-anaconda-client/).
