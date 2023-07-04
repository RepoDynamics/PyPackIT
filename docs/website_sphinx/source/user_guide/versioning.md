
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

Afterwards, until you create the next tag (0.0.1), any push to the main branch will create a development version
in the form of 0.0.1.devN, where N is the number of commits to the main branch since the last tag.
This is a [PEP440](https://peps.python.org/pep-0440/#public-version-identifiers)-compliant public version identifier, 
so that each push to the main branch can be published on TestPyPI. 


For developers:

an alternative is https://github.com/pypa/setuptools_scm/