# Quickstart

## Getting Started

### Step 1: Create a new repository from template
1. Click on the `Use this template` button on the [GitHub repository](), then click on the `Create a new repository` option.
2. Enter a name for your repository in the `Repository name` field, and click on the `Create repository` button.
   This will create a new repository in your GitHub account based on the template repository,
   and will redirect you to the new repository.
### Step 2: Create a personal access token
1. Go to your [GitHub account settings](https://github.com/settings/personal-access-tokens/new),
   to create a new fine-grained personal access token.
2. Enter a name for your token (e.g. `{YOUR-REPO-NAME}_REPODYNAMICS_ADMIN_TOKEN`)
   ans choose an expiration date. Note that you have to repeat these steps after the token expires.
3. Under `Repository access` choose `Only select repositories` and select your new repository.
4. Under `Permissions` choose `Repository permissions` and set the `Administration` and `Pages`
   access to `Read and write`.
5. Click on the `Generate token` button at the bottom of the page.
6. Copy the displayed token to your clipboard.
7. Go back to your new repository, and click on the `Settings` tab.
8. Under the `Security` tab on the left menu, click on `Secrets and variables`,
   and select `Actions`.
9. In the `Secrets` tab of the opened page, click on the `New repository secret` button.
10. In the `Name` field, enter `REPO_ADMIN_TOKEN`,
    paste the token you copied in step 6 into the `Secret` field, and click on the `Add secret` button.
### Step 3: Activate PyPI and TestPyPI publishing
1. Go to the [Publishing](https://pypi.org/manage/account/publishing/) section of your PyPI account settings.
2. Fill in the form under the `Add a new pending publisher` section:
   1. Under `PyPI Project Name`, enter the name you have selected for your project.
      Make sure the name is available on PyPI, by checking the [PyPI project index](https://pypi.org/project/).
   2. Under `Owner`, enter your GitHub username.
   3. Under `Reposiroty name`, enter the name of your new repository.
   4. Under `Workflow name`, enter `_pkg_publish.yaml`.
   5. Under `Environment name`, enter `PyPI`.
3. Do the same in your [TestPyPI](https://test.pypi.org/manage/account/publishing/) account,
   only this time under `Environment name`, enter `TestPyPI`.


11. then click on the `New repository secret` button.
4. Go to the `Actions` tab of the repository; here you will see the CI/CD workflow running.
   Wait for the workflow to complete successfully (with a green checkmark).
   If the workflow fails (commonly due to an internal GitHub error),
   re-run the workflow by clicking on the `Re-run all jobs` button, until it succeeds.

   This first workflow run will initialize your new repository, by deleting all dynamic files and directories,
   and bringing your repository to a clean state. The workflow will amend the initial commit with the changes.
5. Create a new branch and name it `dev/0`.
6. Go to the `.meta` directory,


you must explicitly allow GitHub Actions to create pull requests.
This setting can be found in a repository's settings under Actions > General > Workflow permissions.
