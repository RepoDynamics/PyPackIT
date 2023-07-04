
References:
[Python Packaging User Guide](https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/)
on publishing package distribution releases using GitHub Actions workflows.

We use a better alternative; First, we use the PyPI [cibuildwheel](https://github.com/pypa/cibuildwheel) GitHub action,
to build multiple wheels on a matrix of OS and Python versions. This is only done when the package is not pure python (see this [issue](https://github.com/pypa/cibuildwheel/issues/1021)).

Then, we use the [pypi-publish](https://github.com/marketplace/actions/pypi-publish) GitHub action,
to publish the package on PyPI and TestPyPI, using trusted publishing.


## Setting Up PyPI and TestPyPI

Workflows use [trusted publishing](https://docs.pypi.org/trusted-publishers/) to automatically 
publish the package on TestPyPI and PyPI.

### PyPI

1. [Register](https://pypi.org/account/register/) an account on [PyPI](https://pypi.org/),
   or [log in](https://pypi.org/account/login/) to your existing account
2. Open the [Publishing](https://pypi.org/manage/account/publishing/) section.
3. Go to 'Add a new pending publisher' and add the package data 
   (see [PyPI docs](https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/) for more info).