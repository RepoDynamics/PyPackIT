# Creating a New Repository


## Create a New Repository From {{pp_meta.name}} Template
1. Sign in to your [GitHub](https://github.com) account, and navigate to the
{{ '[{} GitHub repository]({})'.format(pp_meta.name, pp_meta.url.github.home) }}.
2. Click on the {bdg-success}`Use this template` button and select the
{{ '[Create a new repository](https://github.com/new?template_name={}&template_owner={})'.format(pp_meta.repo.name, pp_meta.repo.owner) }}
option from the dropdown menu.
3. Enter a name for your repository in the `Repository name` field.

:::{admonition} Naming convention
:class: important
A GitHub repository name can only contain alphanumeric characters,
hyphens, underscores, and periods. That is, the matching regular expression is:
```regex
^[a-zA-Z0-9._-]+$
```
By default, {{pp_meta.name}} also derives the name of your project, as well as the package name,
from the repository name. The project name on itself has no restrictions, and is simply constructed
by replacing each hyphen in the repository name with a space:
```python
def derive_project_name(repo_name: str) -> str:
    project_name = repo_name.replace("-", " ")
    return project_name
```
On the other hand, the [Python Packaging Authority (PyPA)](https://packaging.python.org/en/latest/specifications/name-normalization/)
requires that the package name consists only of ASCII alphanumeric characters,
hyphens, underscores, and periods.
Additionally, it must start and end with an alphanumeric character,
meaning that a valid non-normalized project name must match the following regex:
```regex
^([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9._-]*[a-zA-Z0-9])$
```
PyPA then normalizes the package name by lowercasing the non-normalized name,
and replacing all runs of consecutive hyphens, underscores, and periods with a single hyphen:
```python
import re

def normalize_package_name(non_normalized_package_name: str) -> str:
    normalized_package_name = re.sub(
       r'[._-]+', '-', non_normalized_package_name.lower()
    )
    return normalized_package_name
```
This means that, for example, all following package names are equivalent and can be used interchangeably:
- `my-project` (normalized)
- `my_project`
- `my.project`
- `My--Project`
- `mY-._.-ProjEcT`

By default, {{pp_meta.name}} derives the package name from the project name via a similar normalization,
with the only difference being that the non-normalized package name is not lowercased:
```python
import re

def derive_package_name(project_name: str) -> str:
    package_name = re.sub(
       r'[._-]+', '-', project_name
    )
    return package_name
```
Subsequently, the import name of the package is derived by lowercasing the package name and
replacing all hyphens with underscores:
```python
import re

def derive_import_name(package_name: str) -> str:
    import_name = re.sub(
       r'-', '_', package_name.lower()
    )
    return import_name
```
While you can manually set the project name, package name, and import name in the metadata,
it is strongly recommended to use the automatic derivation by choosing a repository name that obeys
the pattern for a valid non-normalized project name according to PyPA.
For example, choosing `My-Project` as the repository name, the project name will be `My Project`,
the package name will be `My-Project` (same as the repository name), and the import name will be `my_project`.
That is, the package will be shown on PyPI as `My-Project`,
while users can install it with `pip install my-project`{l=bash}
(or any other equivalent name, due to PyPA normalization),
and import it with `import my_project`{l=python}.
:::

4. Optionally, if you are a member of an organization, you can choose to create the repository under
one of your organizations (instead of your current account) by selecting it from the `Owner` dropdown menu.
5. Click on the `Create repository` button.

Following the above instructions will create a new repository in your selected account
using the {{pp_meta.name}} template, and will redirect you to the new repository.
Navigating to the `Actions` tab of your new repository, you will see that a workflow is running.
This will initialize your new repository by removing all unnecessary files and directories
and bringing your repository to a clean state.
While waiting for the workflow to complete, and before making any changes to your repository,
follow the next steps below.


## Add a Personal Access Token
{{pp_meta.name}} requires a personal access token to authenticate with GitHub and perform various tasks.

1. On your GitHub account, navigate to [Settings > Developer settings > Personal access tokens > Fine-grained tokens > Generate new token](https://github.com/settings/personal-access-tokens/new)
to create a new [fine-grained personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token).
2. Under `Token name`, enter a name for your token (e.g. `<YOUR-REPO-NAME>_REPODYNAMICS_ADMIN_TOKEN`),
and choose an expiration date under `Expiration`. Note that you have to repeat these steps after the token expires.
3. Under `Repository access` choose `Only select repositories`
and select your new repository from the dropdown menu.
4. Under `Permissions` select `Repository permissions` and set the `Administration` and `Pages`
access to `Read and write`.
5. Click on the {bdg-success}`Generate token` button at the bottom of the page.
6. Copy the displayed token to your clipboard.
7. Go back to your new repository, and click on the `Settings` tab.
8. Under the `Security` tab on the left menu, click on `Secrets and variables`, and select `Actions`.
9. On the `Secrets` tab, click on the `New repository secret` button.
10. In the `Name` field, enter `REPO_ADMIN_TOKEN`,
paste the token you copied in step 6 into the `Secret` field, and click on the `Add secret` button.


## Activate PyPI and TestPyPI Publishing
1. [Create an account on PyPI](https://pypi.org/account/register/)
or [log in to your existing account](https://pypi.org/account/login/).
2. Navigate to the [Publishing](https://pypi.org/manage/account/publishing/) section of your account.
3. Fill in the form under the `Add a new pending publisher` section:
   1. Under `PyPI Project Name`, enter the name you have selected for your package.
      If you haven't specifically defined a package name,
      this will be the automatically derived package name as described above.
      Make sure the name is available on PyPI by checking the [PyPI project index](https://pypi.org/project/).
   2. Under `Owner`, enter your GitHub username.
   3. Under `Reposiroty name`, enter the name of your new repository.
   4. Under `Workflow name`, enter `_pkg_publish.yaml`.
   5. Under `Environment name`, enter `PyPI`.
4. Do the same in your [TestPyPI](https://test.pypi.org/manage/account/publishing/) account,
   only this time under `Environment name`, enter `TestPyPI`.

## Configure Your New Repository
