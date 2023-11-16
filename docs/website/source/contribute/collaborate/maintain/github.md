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


## Labels
Labels are managed automatically.
To add/modify/remove a label, modify the file ./github/config/labels.yaml.
Labels are then automatically synced by the workflow ./github/workflows/labels_sync.yaml,
using the [label-syncer](https://github.com/micnncim/action-label-syncer) action.




## Configurations you have to set manually after creating a repository



## Codecov
codecoverage : https://about.codecov.io/

