# Quickstart

## Getting Started






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
