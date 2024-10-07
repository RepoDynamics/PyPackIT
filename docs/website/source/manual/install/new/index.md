(install-new)=
# New Repository

To install {{ccc.name}} in a new GitHub repository:
1. [Create a repository from {{ ccc.name }}'s template repository](#install-repo-creation).
2. [Add a Personal Access Token (PAT) and activate external services](#install-common).
3. [Customize project configurations and metadata](#install-new-project-config).
4. [Initialize project with a commit](#install-new-project-init).

:::{admonition} Don't Miss Step 2 
:class: important

Since step **2** is common for both new and existing repositories,
it is explained in a [separate section](#install-common),
while steps **1**, **3**, and **4** are detailed below.
Don't forget to follow all four steps in the given order.
:::


(install-repo-creation)=
## Repository Creation

The first step is to [create a new repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template)
using {{ ccc.name }}'s GitHub template repository:

1. [Sign in](https://github.com/login) to your GitHub account.
2. {{ '[Click here](https://github.com/new?template_name={}&template_owner={})'.format(ccc.repo.name, ccc.team.owner.github.id) }}
   or alternatively navigate to the {{ '[{} template repository]({})'.format(ccc.name, ccc.github.url.home) }},
   Click on the {bdg-success}`Use this template` button on the top-right corner
   and select ***Create a new repository*** from the dropdown menu.
3. Enter a name for your repository in the ***Repository name*** field.

{#install-repo-naming}
:::{admonition} Repository Naming
:class: dropdown tip

A GitHub repository name can only contain alphanumeric characters,
hyphens, underscores, and periods.
That is, the matching regular expression is: `^[a-zA-Z0-9._-]+$`.
By default, the repository name is also used to derive
the [project name](#ccc-name), and by extension, the [package name](#ccc-pkg-name),
which has additional restrictions.
While you can manually set these separately in the control center,
for consistency, it is recommended to choose a repository name 
that can be used to automatically derive the package name.
Considering the restrictions on the repository name,
this simply means that the repository name should not start with a digit,
and should end with an alphanumeric character.

For example, choosing `My-Project` as the repository name, the project name will be `My Project`,
the distribution package name will be `My-Project` (same as the repository name), 
and the import package name will be `my_project`.
That is, the package will be shown on PyPI as `My-Project`,
while users can install it with `pip install my-project`{l=bash}
(or any other equivalent name, due to PyPA's name normalization),
and import it with `import my_project`{l=python}.
:::

4. Optionally, if you are a member of an organization, you can choose to create the repository under
   one of your organizations (instead of your personal account)
   by selecting it from the ***Owner*** dropdown menu.
5. Click on the {bdg-success}`Create repository` button.

:::{include} /_snippets/admo_login.md
:::

You will be redirected to the newly created repository in your selected account.
Navigating to the repository's [Actions](){.user-link-repo-actions} tab, you will see that a workflow is running.
It will automatically initialize the new repository by generating all necessary files 
and removing extra files that belong to the {{ccc.name}} repository but are not part of the template.
While waiting for the workflow to complete and **before making any other changes**,
follow step 2 to [add a Personal Access Token (PAT) and activate external services](#install-common).


(install-new-project-config)=
## Project Configuration

Going back to your new GitHub repository after finishing the [common steps](#install-common),
verify that the first workflow run has completed successfully (with a green checkmark).
You will see that the default initial commit has been replaced by a new commit,
which contains all the generated files for your repository.

:::{admonition} Failing Workflows
:class: note dropdown

Rarely, workflows may fail due to internal GitHub errors.
When a workflow fails, you will see a red cross mark next to the workflow name.
In this case, you can re-run the workflow by clicking on the ***Re-run all jobs*** button.
{{ ccc.name }} always generates comprehensive job reports and logs for each workflow run,
which can also be investigated in case of a failure or unexpected behavior.
:::

Start customizing your new project:

1. Navigate to the [`.control/proj.yaml`](){.user-link-repo-cc-proj} file in the repository.
2. Replace the placeholder values for `$.title`, `$.abstract`, `$.keywords`, and `$.highlights` keys
   with your project's information.
3. Commit and push your changes. If you have followed the link above,
   you should be on the [github.dev](https://docs.github.com/en/codespaces/the-githubdev-web-based-editor)
   web-based editor, where you can commit and push your changes by clicking the
   <i class="fa-solid fa-code-branch"></i> icon in the left sidebar,
   typing a commit message, and clicking the {bdg-success}`Commit & Push` button.

After pushing your changes, the workflow will run again
and update all dynamic files with the new project information.
Looking at the changed files in the newly created [commits](){.user-link-repo-commits},
you can find all the files that have been updated with your new project's information,
such as the [repository README file](){.user-link-repo-readme}.
Furthermore, since now you have provided your PAT,
the workflow will also activate [GitHub Pages](https://pages.github.com/) for your repository,
build your website, and deploy it online.
A link to your website will be added to the
the [About](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics#about-topics)
section of your repository's [homepage](){.user-link-repo-home},
along with your project's title and keywords.

Your repository is now in the initialization phase.
During this phase, every time you push a commit to the repository, {{ccc.name}} will:

- Update all dynamic files and directories according to the control center configurations.
- Update repository configurations, including general settings, branch names,
  labels, issues forms, discussions, security settings, etc.
- Build and deploy your website to GitHub Pages.
- Build, lint, and test your package.
- Upload build artifacts, reports, and logs for each workflow run.

Continue customizing your project by modifying the [control center files](){.user-link-repo-cc}
and pushing your changes to the repository.
For example, open the [`.control/doc.yaml`](){.user-link-repo-cc-doc} file
and change your project theme's colors under [`$.theme.color`](#ccc-theme-color);
this will update the color of multiple components in your website, README files, and other documents.
You can also add your project's logo by replacing the default logo files
in [`docs/media/logo`](){.user-link-repo-logo} directory.

:::{admonition} Control Center Configurations
:class: seealso

For a full reference of all available options in your repository's control center,
see the [Options](../control/options/index.md) section.
:::


(install-new-project-init)=
## Project Initialization

After you feel satisfied with the results,
signal {{ccc.name}} to initialize your project,
by pushing a commit of [type](#feature-commits-structure) `init`
(i.e., a commit whose message starts with ***init:***).
After performing the same tasks as in the initialization phase,
{{ccc.name}} will:

- Replace all previous commits in the repository with a single `init` commit.
- Tag the commit with the version number `0.0.0`.
- Publish your package to PyPI and TestPyPI.
- Apply branch protection rules to all branches.

You can also customize the initialization process by providing additional configurations
in the commit message:

- To disable commit squashing and keep the previous commits in the repository,
  set the `squash` key to `false` in the [commit message footer](#feature-commits-structure).
- To use a different version number for the initial release,
  set the `version` key to the desired version number in the commit message footer
  (e.g., `version: 1.0.0`).
- Provide a custom description in the commit message summary to overwrite the default message
  (e.g., `init: Start my project.`).

:::{code-block}
:caption: Example `init` commit message

init: Initialize my project.

Here is an optional body for my commit message.

-----------------------------------------------
squash: false
version: 1.0.0
:::

Your repository is now fully configured,
your package is published, your website is live,
and all your workflows are set up and running. 
Continue to the [Quickstart](#quickstart) section
to learn how to further develop your project with {{ccc.name}}.
