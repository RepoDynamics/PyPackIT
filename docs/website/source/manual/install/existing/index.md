(install-existing)=
# Existing Repository

To install {{ ccc.name }} in an existing GitHub repository:

1. [Merge the repository with {{ ccc.name }}'s template repository.](#install-repo-preparation)
2. [Add a Personal Access Token (PAT) and activate external services](#install-common).
3. [Customize project configurations and metadata](#install-existing-project-config).
4. [Push changes to GitHub.](#install-existing-)

:::{admonition} Don't Miss Step 2
:class: important

Since step **2** is common for both new and existing repositories,
it is explained in a [separate section](#install-common),
while steps **1**, **3**, and **4** are detailed below.
Don't forget to follow all four steps in the given order.
:::

## Repository Preparation

The first step is to add {{ ccc.name }}'s configuration files
to a local clone of your repository:

1. Clone your GitHub repository locally.
2. Install the {{ ccc.name }} Python package in a (preferably new) environment with `Python >= 3.10`
   using pip:
   ```bash
   pip install pypackit
   ```
3. On the main branch of your local repository, temporarily move everything
   other than the `.git` directory to another location outside of the repository directory.
4. In your terminal, run
   ```bash
   pypackit unpack 'PATH/TO/YOUR/REPOSITORY/DIRECTORY'
   ```
   or just `pypackit unpack` when you are already in the repository directory.

This will copy the {{ ccc.name }} repository template into your repository,
and sync it with your repository metadata.
Now you can start adding your project metadata and settings to
{{ ccc.name }}'s configuration files in the `.control` directory inside your repository.
To see the results of your configurations, run
```bash
pypackit sync 'PATH/TO/YOUR/REPOSITORY/DIRECTORY'
```
