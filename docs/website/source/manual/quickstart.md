# Quickstart

1. Click on the `Use this template` button on the [GitHub repository](), then click on the `Create a new repository` option.
2. Enter a name for your repository in the `Repository name` field, and click on the `Create repository` button.
   This will create a new repository in your GitHub account based on the template repository, 
   and will redirect you to the new repository.
3. Go to the `Actions` tab of the repository; here you will see the CI/CD workflow running.
   Wait for the workflow to complete successfully (with a green checkmark). 
   If the workflow fails (commonly due to an internal GitHub error), 
   re-run the workflow by clicking on the `Re-run all jobs` button, until it succeeds.
   
   This first workflow run will initialize your new repository, by deleting all dynamic files and directories,
   and bringing your repository to a clean state. The workflow will amend the initial commit with the changes.
4. Create a new branch and name it `dev/0`.
5. Go to the `.meta` directory, 


you must explicitly allow GitHub Actions to create pull requests.
This setting can be found in a repository's settings under Actions > General > Workflow permissions.
