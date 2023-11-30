# Metadata File

{{ pp_meta.name }} gathers all the contents of your repository's control center into a single JSON file,
which is automatically updated whenever you apply changes to the control center.
This file, which is located at `{{ pp_meta.custom.path.file_metadata }}`, serves two main purposes:
- During workflow runs triggered by events that do not modify the contents of the control center,
  {{ pp_meta.name }} uses this file to read all the necessary data and configurations,
  instead of unnecessarily parsing and processing the control center's contents from scratch.
- It is made available to your documentation website, allowing you to use all available data and configurations
  in your website's content and templates, without any required intervention from {{ pp_meta.name }}.



## Structure


## Contents

An


## `repo`
- dictionary of strings

Target repository's metadata as a dictionary with the following keys:
- `name`: repository name
- `full_name`: repository full name in format OWNER-USERNAME/REPOSITORY-NAME
- `owner`: repository owner's username
- `id`: repository id
- `node_id`: repository node id
- `html_url`: repository url
- `default_branch`: repository default branch name
- `created at`: repository creation date

Depending on the value of `repo_target` set in the metadata, the target repository is either the
current repository (`repo_target` = 'self'), the repository's parent (`repo_target` = 'parent'),
or the repository's source (`repo_target` = 'source').


## Package

### `package.name`
- string

Name of the package.
It is derived from the name of the project (`name`), via normalization[^name-normalization]:
The project name is lowercased, with all runs of spaces, periods (.), underscores (_) and hyphens (-)
replaced with a single hyphen, i.e.:
```python
package_name = re.sub(r'[._- ]+', '-', project_name.lower())
```
[^name-normalization]: [Python Packaging User Guide > PyPA specifications > Package name normalization](https://packaging.python.org/en/latest/specifications/name-normalization/)
