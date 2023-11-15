# Generated Metadata

### `repo`
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
