(install-common)=
# Common Steps

This section describes the installation steps that are common to both
[new](#install-new) and [existing](#install-existing) repositories.
Follow these steps when you are asked to do so in the respective installation guides:

1. [Add a GitHub Personal Access Token (PAT) to the repository](#install-pat).
2. [Activate trusted publishing (OIDC) for PyPI and TestPyPI](#install-pypi).
3. [Add an Anaconda token to the repository](#install-anaconda)
4. [Add a Zenodo token to the repository](#install-zenodo).
5. [Create a Codecov account and install the Codecov GitHub app](#install-codecov).

Note that other than the first step (GitHub PAT), all others are optional
and you can skip them if you do not wish to use the respective services.


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
4. Under ***Permissions*** select ***Repository permissions*** and
   set the ***Administration***, ***Contents***, and ***Pages*** access to ***Read and write***.
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
(cf. [PyPI docs](https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/)
and [GiHub docs](https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/configuring-openid-connect-in-pypi)).

To activate trusted publishing for PyPI and TestPyPI in
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
   4. ***Workflow name***: `cd-pypi.yaml`
   5. ***Environment name***: `PyPI`
4. Click on the {bdg-info}`Add` button to submit the form.
   Make sure the submission is accepted by checking the response message that appears at the top of the page.
   If the submission is rejected due to a name conflict,
   you have to try a different name for the project.
   In that case, don't forget to update your [package name](#ccc-pkg-name) in the project metadata
   (and/or rename your repository) afterwards.
5. Repeat the above steps in your [TestPyPI](https://test.pypi.org/manage/account/publishing/) account,
   only this time under the ***Environment name*** field enter `TestPyPI` instead of `PyPI`.


(install-anaconda)=
## Anaconda Token

{{ ccc.name }} can also build a conda package and publish it to your Anaconda channel.
To enable automatic publishing on Anaconda:

1. [Create an account on Anaconda](https://anaconda.org/account/register)
   or [log in to your existing account](https://anaconda.org/account/login).
2. In the [Settings](https://anaconda.org/aariam/settings/profile) page of your account,
   click on [Access](https://anaconda.org/aariam/settings/access) under the left panel.
3. In the ***Token Name*** field, enter a name (for your own reference) for the token.
4. From the ***Scopes*** section, select ***Allow all operations***.
5. Choose an expiration date under ***Expiration date***.
   Note that you have to repeat these steps to replace the token after it expires.
6. Click on the {bdg-success}`Create` button and copy the displayed token to your clipboard.
7. Go to [Settings > Security > Secrets and variables > Actions > Secrets > New repository secret](){.user-link-repo-settings-secrets-actions-new}
   in your repository.
8. In the ***Name*** field, enter `ANACONDA_TOKEN`,
   paste the token you copied in step 6 into the ***Secret*** field,
   and click on the {bdg-success}`Add secret` button.


(install-zenodo)=
## Zenodo Token

To enable the automatic publishing to Zenodo and/or Zenodo Sandbox:

1. [Create an account on Zenodo](https://zenodo.org/signup/)
   or [log in to your existing account](https://zenodo.org/login/).
2. In the [Applications](https://zenodo.org/account/settings/applications/) page of your account,
   click on [New token](https://zenodo.org/account/settings/applications/tokens/new/)
   under the ***Personal access tokens*** panel.
3. Add a ***Name*** (e.g., name of your GitHub repository), select `deposit:actions` under ***Scopes***,
   and click on the {bdg-info}`Create` button.
4. Copy the displayed token to your clipboard, and then click on the {bdg-info}`Save` button.
5. Go to [Settings > Security > Secrets and variables > Actions > Secrets > New repository secret](){.user-link-repo-settings-secrets-actions-new}
   in your repository.
6. In the ***Name*** field, enter `ZENODO_TOKEN`,
   paste the token you copied in step 4 into the ***Secret*** field,
   and click on the {bdg-success}`Add secret` button.
7. Repeat the above steps for [Zenodo Sandbox](https://sandbox.zenodo.org/),
   only this time in step 6, enter `ZENODO_SANDBOX_TOKEN` instead of `ZENODO_TOKEN`.


:::{admonition} For Existing Projects
:class: important dropdown

If your project is already published on either Zenodo or Zenodo Sandbox
and you wish to publish future versions under the same so-called concept record
(instead of creating a new concept), you can add your existing concept's DOI and ID
to the [variables files](){.user-link-repo-const-variables} in your repository.
Note that this **must be done in the first commit after adding your tokens**,
otherwise a new concept will be created for each platform (Zenodo or Zenodo Sandbox)
that does not define an ID.
:::

<!-- (https://docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content) -->


(install-codecov)=
## CodeCov Account

To automatically upload your test coverage results to CodeCov:

1. Create an account on [CodeCov](https://codecov.io/) using your GitHub account.
2. Install the Codecov GitHub app either by clicking on the ***Configure Codecov's GitHub app*** link
   on the Codecov website, or directly from the [app page](https://github.com/apps/codecov).
   You can choose to install it for all your repositories or only for the current repository.
