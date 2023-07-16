# Package


## Configuration
pyproject.toml file replaces setup.py.

It is written in [TOML](https://github.com/toml-lang/toml).

Python standard library has a module named [tomllib](https://docs.python.org/3/library/tomllib.html)
for reading (but not writing) TOML files.
To write TOML files, other non-standard libraries such as
[toml](https://github.com/uiri/toml) and [tomli-W](https://github.com/hukkin/tomli-w) can be used.
However, these don't preserve the original style of a TOML file when modifying.
[TOML Kit](https://github.com/sdispater/tomlkit) is another alternative that also preserves styling,
and is used in this package to read, modify and write the pyproject.toml file.


## Version


We use [semantic versions](https://semver.org/).

We use [versioningit](https://github.com/jwodder/versioningit) to automatically handle versions.
It will calculate the version of the package and dynamically inject it into pyproject.toml, so that using pip or build
to install/build the package will always have a version number. The version number is also injected into the main
\__init\__.py file of the package.

The [configurations](https://versioningit.readthedocs.io/en/stable/configuration.html)
are stored in pyproject.toml, under \[tool.versioningit] tables.

For this, after the initial commit to your repository, create a tag:

git tag -a 0.0.0 -m "Initial template by PyPackIT"

and push:

git push origin --tags

or

git push origin 0.0.0


This will build the package with version 0.0.0.

Afterward, until you create the next tag (0.0.1), any push to the main branch will create a development version
in the form of 0.0.1.devN, where N is the number of commits to the main branch since the last tag.
This is a [PEP440](https://peps.python.org/pep-0440/#public-version-identifiers)-compliant public version identifier,
so that each push to the main branch can be published on TestPyPI.


For developers:

an alternative is https://github.com/pypa/setuptools_scm/

[Versioneer](https://github.com/warner/python-versioneer) will automatically infer what version
is installed by looking at the `git` tags and how many commits ahead this version is. The format follows
[PEP 440](https://www.python.org/dev/peps/pep-0440/) and has the regular expression of:
```
\d+.\d+.\d+(?\+\d+-[a-z0-9]+)
```
If the version of this commit is the same as a `git` tag, the installed version is the same as the tag,
e.g. `{{cookiecutter.repo_name}}-0.1.2`, otherwise it will be appended with `+X` where `X` is the number of commits
ahead from the last tag, and then `-YYYYYY` where the `Y`'s are replaced with the `git` commit hash.


## Build

### Conda
Conda packages are built with [conda-build](https://docs.conda.io/projects/conda-build/),
using instructions that are mostly defined in a single YAML file named
[meta.yaml](https://conda.io/projects/conda-build/en/stable/resources/define-metadata.html).
The YAML file can be created [from scratch](https://docs.conda.io/projects/conda-build/en/stable/user-guide/tutorials/build-pkgs.html)
, or with help of other utilities, such as [conda skeleton](https://docs.conda.io/projects/conda-build/en/stable/user-guide/tutorials/build-pkgs-skeleton.html)
. After build, the package distribution can be
[uploaded](https://docs.anaconda.com/free/anacondaorg/user-guide/tasks/work-with-packages/#uploading-packages)
on an Anaconda channel. While this may be done on a [personal channel](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/create-custom-channels.html)
, this complicates the installation process for users as they now have to specify the channel as well.
A more convenient alternative is to publish the package on the [conda-forge](https://conda-forge.org/) channel.
This requires following the [instructions](https://conda-forge.org/docs/maintainer/adding_pkgs.html).




## Publishing
References:
[Python Packaging User Guide](https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/)
on publishing package distribution releases using GitHub Actions workflows.

We use a better alternative; First, we use the PyPI [cibuildwheel](https://github.com/pypa/cibuildwheel) GitHub action,
to build multiple wheels on a matrix of OS and Python versions. This is only done when the package is not pure python (see this [issue](https://github.com/pypa/cibuildwheel/issues/1021)).

Then, we use the [pypi-publish](https://github.com/marketplace/actions/pypi-publish) GitHub action,
to publish the package on PyPI and TestPyPI, using trusted publishing.


### Setting Up PyPI and TestPyPI

Workflows use [trusted publishing](https://docs.pypi.org/trusted-publishers/) to automatically
publish the package on TestPyPI and PyPI.

### PyPI

1. [Register](https://pypi.org/account/register/) an account on [PyPI](https://pypi.org/),
   or [log in](https://pypi.org/account/login/) to your existing account
2. Open the [Publishing](https://pypi.org/manage/account/publishing/) section.
3. Go to 'Add a new pending publisher' and add the package data
   (see [PyPI docs](https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/) for more info).
