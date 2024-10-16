(install-common)=
# Common Steps

This section describes the installation steps that are common to both
[new](#install-new) and [existing](#install-existing) repositories.
Follow these steps when you are asked to do so in the respective installation guides:

1. [Add a Personal Access Token (PAT) to the repository](#install-pat).
2. [Activate trusted publishing (OIDC) for PyPI and TestPyPI](#install-pypi).
3. [Create a Codecov account and install the Codecov GitHub app](#install-codecov).
4. [Add a Zenodo token to the repository](#install-zenodo).


(install-pat)=
## GitHub PAT

The repository owner (or a member with admin permissions to the repository)
needs to create a [PAT](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
with the required permissions, and store it as a secret in the repository.

:::{admonition} Why a PAT is Required
:class: note dropdown

{{ccc.name}} works by interacting with your repository
and performing various tasks on your behalf. To be allowed to do so,
{{ccc.name}} needs a token to authenticate with GitHub.
By default, GitHub automatically creates a unique [`GITHUB_TOKEN`](https://docs.github.com/en/actions/security-guides/automatic-token-authentication#about-the-github_token-secret)
at the beginning of each workflow run, to be used by the workflow to authenticate with GitHub.
However, this token has limited [permissions](https://docs.github.com/en/actions/security-guides/automatic-token-authentication#permissions-for-the-github_token)
by design, and is not sufficient for {{ccc.name}} to perform all its tasks,
such as modifying the repository's settings.
Therefore, the PAT is used instead of the `GITHUB_TOKEN` to perform
tasks that require higher permissions.
:::

To add a [fine-grained personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)
to your repository:

1. [Click here](https://github.com/settings/personal-access-tokens/new) or alternatively
   in your GitHub user account, navigate to ***Settings*** > ***Developer settings*** >
   ***Personal access tokens*** > ***Fine-grained tokens*** > ***Generate new token***.
2. Under ***Token name***, enter a name for your token (e.g. `<YOUR-REPO-NAME>_REPODYNAMICS_ADMIN_TOKEN`),
   and choose an expiration date under ***Expiration***.
   Note that you have to repeat these steps to replace the token after it expires.
3. Under ***Repository access*** choose ***Only select repositories***
   and then select your new repository from the dropdown menu.
4. Under ***Permissions*** select ***Repository permissions*** and set the ***Administration*** and ***Pages***
   access to ***Read and write***.
5. Click on the {bdg-success}`Generate token` button at the bottom of the page.
6. Copy the displayed token to your clipboard.
7. Go to [Settings > Security > Secrets and variables > Actions > Secrets > New repository secret](){.user-link-repo-settings-secrets-actions-new}
   in your repository.
8. In the ***Name*** field, enter `REPO_ADMIN_TOKEN`,
   paste the token you copied in step 6 into the ***Secret*** field,
   and click on the {bdg-success}`Add secret` button.

:::{admonition} For Organization-Owned Repositories
:class: important dropdown

If your repository is owned by an organization (as opposed to a personal account),
your organization must allow GitHub Actions to create pull requests.
This can be set in the organization account under
[Settings > Actions > General > Workflow permissions](){.user-link-repo-org-settings-actions},
by enabling the option ***Allow GitHub Actions to create and approve pull requests***.
:::


(install-pypi)=
## PyPI Trusted Publishing

{{ ccc.name }} uses
[trusted publishing](https://docs.pypi.org/trusted-publishers/) ({term}`OIDC`)
to automatically authenticate with PyPI servers and publish your Python package on TestPyPI and PyPI,
without the need to manually set authentication credentials such as username and password
(cf. [PyPI docs](https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/)). 

To activate trusted publishing for both PyPI and TestPyPI in
your respective accounts:

1. [Create an account on PyPI](https://pypi.org/account/register/)
   or [log in to your existing account](https://pypi.org/account/login/).
2. If you have not published this project to PyPI before,
   go to the [Publishing](https://pypi.org/manage/account/publishing/) page of your account
   and navigate to the ***Add a new pending publisher*** section at the bottom of the page.
   Alternatively, if you have already published this project to PyPI,
   go to the [Your projects](https://pypi.org/manage/projects/) page of your account,
   find your project and click on the ***Manage*** button, then go to the ***Publishing*** tab
   and navigate to the ***Add a new publisher*** section at the bottom of the page.
3. Fill in the fields in the trusted publishing form for GitHub with following data:
   1. ***PyPI Project Name*** (only for new projects): Distribution name of your Python package
      as given in the [`$.pkg.name`](#ccc-pkg-name) field of your project's metadata.
      If you haven't specifically defined a package name,
      this will be the automatically derived package name
      as described in the [installation guide](#install-repo-naming).
   2. ***Owner***: GitHub username or organization name that owns the repository.
   3. ***Reposiroty name***: Name of your GitHub repository.
   4. ***Workflow name***: `_pkg_publish.yaml`
   5. ***Environment name***: `PyPI`
4. Click on the {bdg-info}`Add` button to submit the form.
   Make sure the submission is accepted by checking the response message that appears at the top of the page.
   If the submission is rejected due to a name conflict,
   you have to try a different name for the project.
   In that case, don't forget to update your [package name](#ccc-pkg-name) in the project metadata
   (and/or rename your repository) afterwards.
5. Repeat the above steps in your [TestPyPI](https://test.pypi.org/manage/account/publishing/) account,
   only this time under the ***Environment name*** field enter `TestPyPI` instead of `PyPI`.


(install-codecov)=
## CodeCov Account

1. Create an account on [CodeCov](https://codecov.io/) using your GitHub account.
2. Install the Codecov GitHub app either by clicking on the ***Configure Codecov's GitHub app*** link
   on the Codecov website, or directly from the [app page](https://github.com/apps/codecov).
   You can choose to install it for all your repositories or only for the current repository.


(install-zenodo)=
## Zenodo Token

<!-- (https://docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content) -->

:::{include} /_snippets/under_construction.md
:::
