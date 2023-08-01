# GitHub

Learn about risks of script injection in GitHub workflows, when using user inputs in inline scripts:
https://docs.github.com/en/github-ae@latest/actions/security-guides/security-hardening-for-github-actions#understanding-the-risk-of-script-injections

## Issues


### Templates and Configuration
The contents of the repository's {{ '[Issues]({})'.format(pp_meta.url.github.issues.home) }} tab is controlled by [templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates)
and a [configuration file](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository#configuring-the-template-chooser)
under the {{ '[.github/ISSUE_TEMPLATE]({}/.github)'.format(pp_meta.url.github.tree) }} directory.

#### Configuration File
The configuration file at
{{ '[./github/ISSUE_TEMPLATE/config.yml]({}/.github/ISSUE_TEMPLATE/config.yml)'.format(pp_meta.url.github.tree) }}
controls some aspects of the template chooser (i.e. the landing page of the repository's 'Issues' section),
with following options:
- `blank_issues_enabled`: A boolean value defining whether free-form issues can be opened by users.
- `contact_links`: An array of dictionaries, defining additional external links for opening issues.
These links will be displayed after the available issue templates.
#### Templates
The issues templates use the GitHub's [issue forms](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository#creating-issue-forms).
Each `.yml` file (other than `config.yml`) provides a template for
a specific issue type. The issue forms use the YAML format, with a series of defined
[top-level keys](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms#top-level-syntax)
such as `name`, `description` and `labels`, and a
[body syntax](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-githubs-form-schema)
to define the form fields.
Any YAML file created in this directory using the specified syntax will be automatically added to the list of possible
issue forms that users can select from when opening a new issue in the repository.


## Pull Requests

Different [pull request templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository)
can only be accessed via [query parameters](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/using-query-parameters-to-create-a-pull-request)
. Otherwise, the main template directly under [./github] is used.


## Labels
Labels are managed automatically.
To add/modify/remove a label, modify the file ./github/config/labels.yaml.
Labels are then automatically synced by the workflow ./github/workflows/labels_sync.yaml,
using the [label-syncer](https://github.com/micnncim/action-label-syncer) action.

### Dev notes
An alternative action to consider: https://github.com/marketplace/actions/issue-label-manager-action
this has the same functionalities, but uses a JSON file for declaring labels, instead of a YAML file.

Another alternative: https://github.com/marketplace/actions/github-labeler


## Labeling PRs
We use [multi-labeler](https://github.com/fuxingloh/multi-labeler), which has support for
conventional commits, filepaths, branch names, titles, bodies and more.

GitHubs own [labeler](https://github.com/actions/labeler) action can only label PRs based on
the paths of files being changed.

[release-drafter](https://github.com/release-drafter/release-drafter) also has a PR labeling tool called
[autolabeler](https://github.com/release-drafter/release-drafter#autolabeler), which can label PRs based on
regex matches on title or body of the PR, as well as on branch name.

Other ones with support for multiple conditions, but not for conventional commits:
https://github.com/marketplace/actions/super-labeler
https://github.com/srvaroa/labeler
https://github.com/Resnovas/label-mastermind
https://github.com/Resnovas/smartcloud

Another one: https://github.com/marketplace/actions/auto-labeler
only matches regex on title or body of PRs.


## Configurations you have to set manually after creating a repository

### Automatically Deleting Branches after Merge
https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-the-automatic-deletion-of-branches

### Enabling Private Vulnerability Reporting
https://docs.github.com/en/code-security/security-advisories/repository-security-advisories/configuring-private-vulnerability-reporting-for-a-repository#enabling-or-disabling-private-vulnerability-reporting-for-a-repository




## Codecov
codecoverage : https://about.codecov.io/


## Funding
GitHub configuration file for displaying a sponsor button in the repository.
References:
  GitHub documentation for this file: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/displaying-a-sponsor-button-in-your-repository
  GitHub documentation on GitHub Sponsors: https://docs.github.com/en/sponsors/receiving-sponsorships-through-github-sponsors
