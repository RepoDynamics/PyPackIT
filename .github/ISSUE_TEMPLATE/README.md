# GitHub Issues Settings
This directory contains templates and configurations used when an issue is opened in the repository.

## Templates
The issues templates use the GitHub's [issue forms](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository#creating-issue-forms)
to create customizable web form fields. Each `.yml` file (other than `config.yml`) provides a template for
a specific issue type. The issue forms use the YAML format, with a series of defined [top-level keys](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms#top-level-syntax)
such as `name`, `description` and `labels`, and a [body syntax](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-githubs-form-schema)
to define the form fields.

Any YAML file created in this directory using the specified syntax will be automatically added to the list of possible
issue forms that users can select from when opening a new issue in the repository.


## Configurations
The [config.yml](../../.meta/config/issues_template_chooser.yaml) file contains the configurations for the
[template chooser](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository#configuring-the-template-chooser),
i.e. the landing page of the repository's 'Issues' section.

### Options
- `blank_issues_enabled`: A boolean value defining whether free-form issues can be opened by users.
- `contact_links`: An array of dictionaries, defining additional external links for opening issues.
These options will be displayed alongside the available templates in the 'Issues' section of the repository.

## References
- [GitHub Documentation](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates)
