# Metadata

## Project
The `project.yaml` file contains the general info on the project.

### Name
Name of the project;
this is only used in documents to refer to the project, so technically it can contain any unicode character,
but it is highly recommended to keep all names consistent, i.e. the package name, which has restrictions,
should be the normalized version of the project name. Therefore, we enforce the restrictions of a
valid non-normalized package name here, and then derive the package name from project name via normalization.

A valid name consists only of ASCII alphanumeric characters, period (.), underscore (_) and hyphen (-), 
and must start and end with a letter or number. The validating regex is thus (with `IGNORECASE` flag set):
```default
^([A-Z0-9]|[A-Z0-9][A-Z0-9._-]*[A-Z0-9])$
```
If ommited (or set to null), the repository name will be used.

#### References
* [Python Packaging User Guide > PyPA specifications > Package name normalization](https://packaging.python.org/en/latest/specifications/name-normalization/)

### Tagline
A single-sentence description of the project.

### Description
A long description of the project that can have multiple paragraphs, with Markdown or HTML formatting.

### Keywords
Keywords to describe the project. 

### License
Name of the license under which the project is distributed.
This must be one of the following values (case-insensitive):
- `Apache_v2`: [Apache License 2.0](https://choosealicense.com/licenses/apache-2.0/)
- `GNU_GPL_v3`: [GNU General Public License v3](https://choosealicense.com/licenses/gpl-3.0/)
- `MIT`: [MIT License](https://choosealicense.com/licenses/mit/)
- `BSD_2_Clause`: [BSD 2-Clause License](https://choosealicense.com/licenses/bsd-2-clause/)
- `BSD_3_Clause`: [BSD 3-Clause License](https://choosealicense.com/licenses/bsd-3-clause/)
- `BSL_v1`: [Boost Software License 1.0](https://choosealicense.com/licenses/bsl-1.0/)
- `GNU_AGPL_v3+`: [GNU Affero General Public License v3 or later](https://choosealicense.com/licenses/agpl-3.0/)
- `GNU_AGPL_v3`: [GNU Affero General Public License v3](https://choosealicense.com/licenses/agpl-3.0/)
- `GNU_GPL_v3+`: [GNU General Public License v3 or later](https://choosealicense.com/licenses/gpl-3.0/)

- `GNU-LGPLv3+`: GNU Lesser General Public License v3 or later
- `GNU-LGPLv3`: GNU Lesser General Public License v3
- `Unlicense`: The Unlicense

- `MPL-2.0`: Mozilla Public License 2.0
- `CC-BY-4.0`: Creative Commons Attribution 4.0 International License
- `CC-BY-SA-4.0`: Creative Commons Attribution-ShareAlike 4.0 International License
- `CC-BY-NC-4.0`: Creative Commons Attribution-NonCommercial 4.0 International License
- `CC-BY-NC-SA-4.0`: Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License
- `CC0-1.0`: Creative Commons Zero v1.0 Universal

### Start Year
The year in which the project was started. This is used to generate the copyright notice.

### GitHub
GitHub username and repository name of the project.

There seems to be no official GitHub documentation regarding repository naming rules.
[Experimentally determined rules](https://stackoverflow.com/a/59082561/14923024) are:
GitHub repository names can only contain alphanumeric characters,
plus hyphen (-), underscore (_), and dot (.), i.e. they must match the regex '^[A-Za-z0-9_.-]+$'.
All other characters are automatically replaced with hyphens, that is:
```python
repo_name = re.sub(r'[^A-Za-z0-9_.-]', '-', project_name),
```

Also, GitHub retains the capitalization only when displaying the repository name; 
otherwise, names are not case-sensitive. That is, "PyPackIT" will be displayed as is,
but any other capitalization of the word in any URL or address will also point to the same repository.

### Authors
GitHub usernames of project's main authors.


## Package

### Name (derived)
Name of the package, derived from the project name, via normalization:
The name is lowercased with all runs of the characters period (.), underscore (_) and hyphen (-) 
replaced with a single hyphen:
```python
package_name = re.sub(r'[._-]+', '-', project_name.lower())
```
#### References
* [Python Packaging User Guide > PyPA specifications > Package name normalization](https://packaging.python.org/en/latest/specifications/name-normalization/)

### Trove Classifiers
Trove classifiers for the package, used by PyPI.
Classifiers are categorized into the following groups:
- Development Status
- Environment
- Framework
- Intended Audience
- License
- Natural Language
- Operating System
- Programming Language
- Topic
- Typing

#### References
* [List of classifiers](https://pypi.org/classifiers/)
* [List of classifiers as a Python package](https://github.com/pypa/trove-classifiers/blob/main/src/trove_classifiers/__init__.py)

### Development Status
Development status of the package, according to the following scheme (see Trove classifiers for more details):
  1 : Planning
  2 : Pre-Alpha
  3 : Alpha
  4 : Beta
  5 : Production/Stable
  6 : Mature
  7 : Inactive




## Maintainers


### Issues
Maintainers that are automatically assigned to each opened issue.

Each key is the name of an issue template form (YAML file) under './github/ISSUE_TEMPLATE/', with the leading
integer and underscore stripped; e.g. for '1_bug_api.yaml', the key is 'bug_api'.
The 'default' key is used for all other issue forms that are not explicitly named here.
The values are lists of GitHub usernames.

### Pull Requests
Code owners that will be automatically requested to review pull requests before merging.

Each key is a glob pattern (with slightly modified rules; see reference) to match files and directories that
a list of GitHub usernames (the value) own.  

#### Notes
* Code owners must have write permissions for the repository.
* For code owners to be automatically requested for reviews, the option must be enabled:
https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches#require-pull-request-reviews-before-merging
* Order is important; the last matching pattern takes the most precedence.

#### References
* GitHub documentation about code owners:
https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
