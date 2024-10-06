(install-new)=
# New Repository

To install {{ccc.name}} in a new GitHub repository:
1. [Create a repository from {{ cc.name }}'s template repository](#install-repo-creation).
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





You will be redirected to the newly created repository in your selected account.
Navigating to the repository's `Actions` tab, you will see that a workflow is running.
It will automatically initialize the new repository by generating all necessary files 
and removing extra files that belong to the {{pp_meta.name}} repository but are not part of the template.
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
In this case, you can re-run the workflow by clicking on the `Re-run all jobs` button.
{{ ccc.name }} always generates comprehensive job reports and logs for each workflow run,
which can also be investigated in case of a failure or unexpected behavior.
:::

Start customizing your new project:

1. Navigate to the `.control/1_proj.yaml` file in the repository.
2. 



a second commit has been added to your repository's default branch,
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


(install-new-project-init)=
## Project Initialization

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

