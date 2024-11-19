# Upgrading

To upgrade an existing {{ ccc.name }} installation in your GitHub repository,
all you need to do is to replace the {{ ccc.name }} [workflow files](){.user-link-repo-workflow-files}
in your repository with ones from a newer version of {{ ccc.name }}.
These can be found in the
{{ '[`.github/workflows` directory]({}/.github/workflows)'.format(ccc.repo.url.blob) }}
of the {{ ccc.name }} template repository. Simply copy the files from the template repository
at a specific version tag or commit hash, and paste them into the same directory in your repository.

In the future, we will provide a more automated way to upgrade {{ ccc.name }} in your repository.
