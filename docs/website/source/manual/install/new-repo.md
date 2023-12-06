# New Repository

To create a new GitHub repository with {{pp_meta.name}} installed, you need to perform the following steps:
1. [Create a repository from the {{pp_meta.name}} repository template](#create-a-repository-from-template).
2. [Add a personal access token as repository secret](#add-a-personal-access-token).
3. [Activate trusted publishing for PyPI and TestPyPI](#activate-trusted-publishing).
4. [Add project metadata](#add-project-metadata).
5. [Initialize project](#initialize-project).


## Create a Repository From Template

The first step is to create a new repository from the {{pp_meta.name}} template repository,
which will automatically add all necessary files and directories to your newly created repository.
To do so, follow the steps below
(cf. [GitHub documentation](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template)):

1. Sign in to your [GitHub](https://github.com) account, and navigate to the
{{ '[{} GitHub repository]({})'.format(pp_meta.name, pp_meta.url.github.home) }}.
2. Click on the {bdg-success}`Use this template` button and select the
{{ '[Create a new repository](https://github.com/new?template_name={}&template_owner={})'.format(pp_meta.repo.name, pp_meta.repo.owner) }}
option from the dropdown menu.
3. Enter a name for your repository in the `Repository name` field.

:::{admonition} Naming convention
:class: important

A GitHub repository name can only contain alphanumeric characters,
hyphens, underscores, and periods. That is, the matching regular expression is: `^[a-zA-Z0-9._-]+$`.
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
`^([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9._-]*[a-zA-Z0-9])$`.
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
This will initialize your new repository by removing all extra files and directories
(i.e., those that belong to the {{pp_meta.name}} repository, but are not part of the template)
and bringing your repository to a clean state.
While waiting for the workflow to complete, and before making any other changes to your repository,
follow the next steps below.


## Add a Personal Access Token

{{pp_meta.name}} works by interacting with your repository and its contents,
and performing various tasks on your behalf. To be allowed to do so,
{{pp_meta.name}} needs a token to authenticate with GitHub.
By default, GitHub automatically creates a unique [`GITHUB_TOKEN`](https://docs.github.com/en/actions/security-guides/automatic-token-authentication#about-the-github_token-secret)
at the beginning of each workflow run, to be used by the workflow to authenticate with GitHub.
However, this token has limited [permissions](https://docs.github.com/en/actions/security-guides/automatic-token-authentication#permissions-for-the-github_token)
by design, and is not sufficient for {{pp_meta.name}} to perform all its tasks,
such as modifying the repository's settings.
Therefore, you (i.e., the repository owner, or a user with admin permissions to the repository),
need to create a personal access token with the required permissions for the repository,
and store it as a secret in your repository,
so that {{pp_meta.name}} can use it instead of the `GITHUB_TOKEN` to perform the
tasks that require higher permissions. To do so, follow the steps below:

1. On your GitHub account, navigate to [Settings > Developer settings > Personal access tokens > Fine-grained tokens > Generate new token](https://github.com/settings/personal-access-tokens/new)
   to create a new [fine-grained personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token).
2. Under `Token name`, enter a name for your token (e.g. `<YOUR-REPO-NAME>_REPODYNAMICS_ADMIN_TOKEN`),
   and choose an expiration date under `Expiration`.
   Note that you have to repeat these steps to replace the token after it expires.
3. Under `Repository access` choose `Only select repositories`
   and select your new repository from the dropdown menu.
4. Under `Permissions` select `Repository permissions` and set the `Administration` and `Pages`
   access to `Read and write`.
5. Click on the {bdg-success}`Generate token` button at the bottom of the page.
6. Copy the displayed token to your clipboard.
7. Go back to your new repository, and click on the `Settings` tab.
8. Under the `Security` section on the left menu, click on `Secrets and variables`, and select `Actions`.
9. On the `Secrets` tab, click on the {bdg-success}`New repository secret` button.
10. In the `Name` field, enter `REPO_ADMIN_TOKEN`,
    paste the token you copied in step 6 into the `Secret` field,
    and click on the {bdg-success}`Add secret` button.

:::{admonition} For organization-owned repositories
:class: important
If your repository is owned by an organization (as opposed to a personal account),
your organization must allow GitHub Actions to create pull requests.
This can be set in the organization's `Settings` page, under
`Actions > General > Workflow permissions`,
at https://github.com/organizations/YOUR-ORGANIZATION-NAME/settings/actions.
:::


## Activate Trusted Publishing

{{ pp_meta.name }} uses [trusted publishing](https://docs.pypi.org/trusted-publishers/)
(i.e., the [OpenID Connect (OIDC)](https://openid.net/connect/) standard)
to automatically authenticate with PyPI servers and publish your Python package on TestPyPI and PyPI,
without the need for authentication credentials (e.g., username and password).
(cf. [PyPI docs](https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/)). You need to activate trusted publishing for both PyPI and TestPyPI in
your respective accounts, by following the steps below:

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
4. Repeat the above steps in your [TestPyPI](https://test.pypi.org/manage/account/publishing/) account,
   only this time under `Environment name`, enter `TestPyPI`.


## Add Project Metadata

Going back to your new repository, you should see that
the workflow has completed successfully (with a green checkmark).
If it is still running, wait for it to complete.
Otherwise, if the workflow has failed (commonly due to an internal GitHub error),
re-run it by clicking on the `Re-run all jobs` button.
{{ pp_meta.name }} will also generate job reports and extensive logs for each workflow run,
which can be investigated in case of a failure or unexpected behavior.

After the workflow completed successfully,
you will see that a second commit has been added to your repository's default branch,
and that it now contains only three directories: `.github`, `.meta`, and `docs`.
The repository is now in the initialization phase.
In this phase, the branch protection rules have not been applied yet,
so you can directly make changes to the default branch and push them to the remote repository.
You also don't have to worry about the commit messages in this phase,
as all commits will be squashed into a single commit at the [end of the initialization phase](#initialize-project).
The goal is to add your project's basic information and metadata,
and configure your repository until you are satisfied with the results.

The `.meta` directory is the default location of your repository's [control center](../control/index.md),
where all configurations, metadata, and settings for your GitHub repository (and its corresponding git repository),
package, website, development pipeline, and other tools are stored in one place.
When you apply a change to the control center's content and push it to the remote repository,
{{pp_meta.name}} will automatically apply the corresponding changes to entire repository and its content,
so that the repository is always in a consistent state with its control center.


All available options are already provided in the `.meta` directory,
where all general configurations and settings are set to sensible default values.
Therefore, as the first step, you only need to add some basic information about your project,
and provide some project-specific configurations:

- Open the project introduction metadata file at
  `./.meta/project/intro.yaml` and add a tagline, description, and some keywords and keynotes
  for your project.
- Open the project theme metadata file at `./.meta/ui/theme.yaml` and add the colors for your project.
- Open the logo directory at `./.meta/ui/logo` and add your project's logos.
- By default, the [GNU Affero General Public License v3 or later] is selected as the license for your project.
  If you want to use a different license, modify the license metadata file at `./.meta/project/license.yaml`
  to select a different pre-defined license or provide your own custom license.
- If you want to add multiple authors
  (by default, the repository owner is added automatically as the only author),
  or want to add funding options to your project,
  open the project credits metadata file at `./.meta/project/credits.yaml` and add the corresponding information.
- By default, the repository owner is set as the only maintainer for all issues, pull requests,
  and discussions, and their email address (read from their GitHub account) is set as
  the contact email address for the project.
  You can change these in the project maintainers metadata file at `./.meta/dev/maintainers.yaml`.

After you have committed and pushed your changes, the CI/CD workflow will automatically run again.
During the initialization phase, the workflow will perform the following tasks on each push:
- Update all dynamics directories and files, according to the control center settings.
- Update the repository's general info and settings, according to the `repo.config` specifications
  in the `./.meta/dev/repo.yaml` file.
  This includes the repository's description, website URL, and topics (keywords),
  which are displayed under the `About` section of the repository's homepage on GitHub, along with
  security settings such as secret scanning, vulnerability alerts, automated security fixes,
  and private security advisories, as well as enabling/disabling different GitHub features
  such as issues, discussions, projects, and wiki.
  Note that issues, squash merges, and the ability of GitHub Actions to create and approve pull requests
  are always automatically enabled by {{pp_meta.name}}, since they are required for its functionalities.
- Update the repository's labels, according to the specifications in the `./.meta/dev/labels.yaml` file.
- Activate the repository's GitHub Pages if necessary, update its custom URL
  if specified in the `web.base_url` specification of the `./.meta/ui/web.yaml` file,
  and deploy the website to GitHub Pages.
- Update the name of the repository's default branch, according to the `branch.default.name` specification
  in the `./.meta/dev/branches.yaml` file.


## Initialize Project

After you feel satisfied with the results, you can initialize your project by pushing a commit
with the message "init" to the default branch of your repository.
This will signal the end of the initialization phase, and will trigger the following tasks
(after running the tasks in the initialization phase for one last time):
- Squash all commits in the default branch into a single commit.
- Tag the commit with the version number `0.0.0`.
- Publish your package to PyPI and TestPyPI.
- Apply the branch protection rules to all branches.

After the workflow completes, your repository is now fully initialized and in its normal state.
From this point on, you must follow the development cycle of {{pp_meta.name}}
to make changes to your repository.
