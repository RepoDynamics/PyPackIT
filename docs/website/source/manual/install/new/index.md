(install-new)=
# New Repository

To create a new GitHub repository with |{{ccc.name}}| pre-installed:
1. [Create a repository from |{{ ccc.name }}|'s template repository](#install-repo-creation).
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
using |{{ ccc.name }}|'s GitHub template repository:

1. [Sign in](https://github.com/login) to your GitHub account.
2. |{{ '[Click here](https://github.com/new?template_name={}&template_owner={})'.format(ccc.repo.name, ccc.team.owner.github.id) }}|,
   or alternatively navigate to the |{{ '[{} template repository]({})'.format(ccc.name, ccc.repo.url.home) }}|,
   click on the {bdg-success}`Use this template` button on the top-right corner,
   and select ***Create a new repository*** from the dropdown menu.
3. Enter a name for your repository in the ***Repository name*** field.

:::{admonition} Repository Naming
:class: dropdown tip
:name: install-repo-naming

A GitHub repository name can only contain alphanumeric characters,
hyphens, underscores, and periods [^stackoverflow-github-repo-name].
That is, the matching regular expression is: `^[a-zA-Z0-9._-]+$`.
However, the repository name can also used to derive
the [project name](#ccc-name) and the [package name](#ccc-pkg-name),
the latter of which has additional restrictions.
While you can set these separately in the control center,
for consistency, it is recommended to choose a repository name
that can be used to automatically derive the package name.
Considering the restrictions on the repository name,
this simply means that the **repository name should not start with a digit,
and should end with an alphanumeric character**.

For example, choosing `My-Project` as the repository name
and leaving the project and package names undefined,
the project name will be automatically set to `My Project`,
the distribution package name to `My-Project` (same as the repository name),
and the import package name to `my_project`.
That is, the package will be shown on PyPI as `My-Project`,
while users can install it with `pip install my-project`{l=bash}
(or any other equivalent name, due to PyPA's name normalization),
and import it with `import my_project`{l=python}.

Note that GitHub retains the capitalization only when displaying the repository name,
but URLs and other repository addresses are case-insensitive.
[^stackoverflow-github-repo-name]: [Experimentally determined GitHub repository naming rules.](https://stackoverflow.com/a/59082561/14923024)
:::

4. Optionally, if you are a member of an organization, you can choose to create the repository under
   one of your organizations (instead of your personal account)
   by selecting it from the ***Owner*** dropdown menu.
5. Click on the {bdg-success}`Create repository` button.

:::{include} /_snippets/admo_login.md
:::

You will be redirected to the newly created repository in your selected account.
Navigating to the repository's [Actions](){.user-link-repo-actions} tab, you will see that a workflow is running.
It will automatically initialize your new repository by generating all necessary files
and removing extra files that belong to the |{{ccc.name}}| repository but are not part of the template.
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
|{{ ccc.name }}| always generates comprehensive job reports and logs for each workflow run,
which can also be investigated in case of a failure or unexpected behavior.
:::

Your repository is now in the initialization phase.
During this phase, every time you push a commit, |{{ccc.name}}| will run a workflow to:

- Update all dynamic files and directories according to the new control center configurations.
- Update repository configurations, including general settings and metadata, branch names,
  labels, issues forms, discussions, and security settings.
- Format, refactor, lint, build, and test the package, test suite, and documentation website.
- Publish a developmental version of the package to your Anaconda channel.
- Deploy the updated website to [GitHub Pages](https://pages.github.com/).
- Build a docker image of the repository and deploy it to GitHub Container Registry (ghcr.io)
  or another registry of your choice.
- Trigger a build on mybinder.org using the docker image.
- Update a draft release on GitHub.
- Update draft releases on Zenodo and/or Zenodo Sandbox.

All jobs can be fully customized (or disabled) from your repository's control center.
To start customizing your new project:

1. Navigate to the [`.control/proj.yaml`](){.user-link-repo-cc-proj} file in the repository.
2. Replace the placeholder values for [`$.name`](#ccc-name), [`$.title`](#ccc-title),
   [`$.abstract`](#ccc-abstract), [`$.keywords`](#ccc-keywords), and [`$.highlights`](#ccc-highlights) keys
   with your project's information. You can also remove the `$.name` key altogether,
   and |{{ ccc.name }}| will use your repository name instead.
3. Commit and push your changes. If you have followed the link in step 1 above,
   you should be on the [github.dev](https://docs.github.com/en/codespaces/the-githubdev-web-based-editor)
   web-based editor, where you can commit and push your changes by clicking the
   <i class="fa-solid fa-code-branch"></i> icon in the left sidebar,
   typing a commit message, and clicking the {bdg-success}`Commit & Push` button.

After pushing your changes, the workflow will run again.
You can see the results of each job in the respective workflow run page
under the repository's [Actions](){.user-link-repo-actions} tab,
where all created artifacts are uploaded along with comprehensive job reports and logs.
Navigating to different parts of your project, you can also verify the changes made. For example:

- Under the [About](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics#about-topics)
section of your repository's [homepage](){.user-link-repo-home}
you can see the updated title, keywords, license, citation, and other project metadata,
along with a link to your online documentation website.
- Looking at the changed files in the newly created [commits](){.user-link-repo-commits},
you can find all the files that have been updated,
such as the [repository README file](){.user-link-repo-readme}.
- Navigating to the [Releases](){.user-link-repo-releases} section of your repository,
you can find the draft release that is automatically updated after each push.
- In the [Packages](){.user-link-repo-releases} section of your repository,
you can find the uploaded docker image.
- Clicking on the Binder badge in your repository README, you can verify
that the docker image is now available on mybinder.org.
- If you have activated Anaconda, Zenodo, or Zenodo Sandbox, you can see the updated draft
on the respective websites.


You can continue customizing your project by modifying the [control center files](){.user-link-repo-cc}
and pushing your changes to the repository.
For example, open the [`.control/doc.yaml`](){.user-link-repo-cc-doc} file
and change your project theme's colors under [`$.color`](#ccc-color);
this will update the color of multiple components in your website, README files, and other documents.
You can also add your project's logo by replacing the sample logo files
in [`docs/website/source/_media/logo`](){.user-link-repo-logo}.
If you already have some initial source code, documentation, or other resources
that you want to add to your repository, you can do so now.


:::{admonition} Control Center Configurations
:class: seealso

|{{ ccc.name }}| is highly customizable with a wide range of options available in the control center,
most of which are provided with standard default values based on best practices.
To avoid overwhelming you with all the available options at once,
only the most essential configurations are provided in the configuration files.
For a full reference of all available options you can set in your repository's control center,
see the [Options](#manual-cc-options) section.
:::


(install-new-project-init)=
## Project Initialization

After you feel satisfied with the results,
you can signal |{{ ccc.name }}| to initialize your project
via a commit. Communicating with |{{ ccc.name }}| through commits
is done via [commit message footers](#feature-commits-structure).
This is the last part of the commit message,
separated from everything above it by a pre-defined separator (cf. [`$.commit.config`](#ccc-commit-config)).
The footer must be in standard YAML syntax, just like the control center configuration files.
Depending on the ongoing event, |{{ ccc.name }}| looks for specific keys defined in the commit footer
for instructions. During the initialization phase, |{{ ccc.name }}| looks for a `initialize-project`
key in the footer of the head commit of each push event. Setting this key to `true` will signal
the end of the initialization phase. If this key is present, |{{ ccc.name }}| will also look for
the following keys for further customized instructions for the initialization event:

:`version`: **string**, **default**: `0.0.0`

    The version to use for the initial release.
    This is useful if you already have an earlier version of your project
    published, and want to contrinue from there.
    Note that this must be a valid Python [public version identifier](https://packaging.python.org/en/latest/specifications/version-specifiers/#public-version-identifiers)
:`squash`: **boolean**, **default**: `true`

    Whether to squash all previous commits into the current commit.
    By default, |{{ ccc.name }}| rewrites the entrire Git history during initialization,
    merging all changes into the latest commit,
    so that the repository only contains the initialization commit afterwards.
    If you want to keep the Git history of the initialization phase, set this to false.
:`publish-zenodo`: **boolean**, **default**: `true`

    Whether to publish the draft release on Zenodo.
:`publish-pypi`: **boolean**, **default**: `true`

    Whether to publish the initial release on PyPI.
:`publish-github`: **boolean**, **default**: `true`

    Whether to publish the draft release on GitHub.
:`publish-zenodo-sandbox`: **boolean**, **default**: `true`

    Whether to publish the draft release on Zenodo Sandbox.
:`publish-testpypi`: **boolean**, **default**: `true`

    Whether to publish the initial release on TestPyPI.

For example, to initialize your project with version `1.0.0` while keeping all commits,
use a commit message like the following:

:::{code-block} git-commit-edit-msg
:caption: Example initialization commit message

init: Initialize my project.

Here is an optional body for my commit message.

---
initialize-project: true
version: 1.0.0
squash: false
:::

After performing the same tasks as in the initialization phase,
|{{ccc.name}}| will tag the latest commit with the given version number,
and publish your package to the specified repositories.
It will also apply all specified branch and tag protection rulesets.
Your repository is now fully configured,
your package is published, your website is live,
and all your workflows are set up and running.


:::{admonition} What's Next
:class: seealso

Continue to the [Quickstart](#quickstart) section
to learn how to start the development of your project with |{{ccc.name}}|.
:::
