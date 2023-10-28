# Metadata

## General Data















### `license_id`
- string, optional, default: `null`

Identifier of the license under which the project is distributed.



### `authors`
- list of dictionaries, optional, default: `null`

A list of authors of the project.
Authors must be listed in order of their contribution to the project.
Each author is represented by a dictionary with two keys:
- `username`: string, required\
GitHub username of the author.
- `roles`: list of strings, optional, default: `null`\
Roles of the author in the project.


### `email`
- dictionary of strings

A dictionary of email addresses for different purposes:
- `main`: string, required\
Main contact email address for the project. This is a required field, and
is used for other purposes if the other keys are not provided.
- `security`: string, optional, default: `main`\
Email address for reporting security vulnerabilities.
- `support`: string, optional, default: `main`\
Email address for support.
- `code_of_conduct`: string, optional, default: `main`\
Email address for reporting code of conduct violations.


## Repository Settings

### `funding`
- dictionary, optional, default: `null`

Configuration for the sponsor section of the repository[^github-funding].
The dictionary must have one or several of the following keys:
- `community_bridge`: string\
Project name for the [LFX Mentorship](https://lfx.linuxfoundation.org/tools/mentorship)
(formerly CommunityBridge) platform.
- `github`: string or list of strings\
Up to 4 GitHub usernames.
- `issuehunt`: string\
[IssueHunt](https://issuehunt.io/) username.
- `ko_fi`: string\
[Ko-fi](https://ko-fi.com/) username.
- `liberapay`: string\
[Liberapay](https://liberapay.com/) username.
- `open_collective`: string\
[Open Collective](https://opencollective.com/) username.
- `otechie`: string\
[Otechie](https://otechie.com/) username.
- `patreon`: string\
[Patreon](https://www.patreon.com/) username.
- `tidelift`: string\
A string in the format PLATFORM-NAME/PACKAGE-NAME for the [Tidelift](https://tidelift.com/) platform,
where PLATFORM-NAME is one of the following: npm, pypi, rubygems, maven, packagist, nuget.
- `custom`: string or list of strings\
Up to 4 custom URLs.

[^github-funding]: [GitHub Documentation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/displaying-a-sponsor-button-in-your-repository#about-funding-files)


### `health_file`
- dictionary of strings, optional, default: `null`

Target paths for GitHub Community Health Files.
These must be placed either in root (`.`), `docs`, or `.github` directory of the repository.
Providing each of the following keys will create the corresponding file in the repository.
- `code_of_conduct`: '.', 'docs', or '.github'
- `codeowners`: '.', 'docs', or '.github'
- `contributing`: '.', 'docs', or '.github'
- `governance`: '.', 'docs', or '.github'
- `security`: '.', 'docs', or '.github'
- `support`: '.', 'docs', or '.github'


### `labels`
- list of dictionaries

A list of labels for the issues, pull requests and discussions in the repository.
Each label is represented by a dictionary with the following keys:
- `name`: string, required\
Name of the label.
- `description`: string, required\
Description of the label.
- `color`: string, required\
Color of the label, in hexadecimal format (e.g. `ff0000` for red).
- `issues`: list of strings, optional, default: `null`\
Names of the issue templates that this label should be applied to.
- `pulls`: dictionary, optional, default: `null`\
Configuration for applying this label to pull requests.
For more information, see the [multi-labeler](https://github.com/fuxingloh/multi-labeler) action


### `issues`
- list of dictionaries, optional, default: `null`

Issue templates used in the repository, and their corresponding assignees,
provided as a list of dictionaries with the following keys:
- `name`: string, required\
Name of the issue template form.
- `assignees`: list of strings, optional\
GitHub usernames of the assignees for the issue template form.
If not provided, the repository owner will be the assignee.
If an empty list is provided, the issue template form will be used without any assignees.

The issue forms are displayed in the order they are provided here.


### `issues_contact_links`
- list of dictionaries, optional, default: `null`




## Maintenance





## General Repository Settings





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


## Package Data

### `package.development_status`
- integer

Development status of the package,
according to the following scheme (see Trove classifiers for more details):
  1 : Planning
  2 : Pre-Alpha
  3 : Alpha
  4 : Beta
  5 : Production/Stable
  6 : Mature
  7 : Inactive


### `package.python_version_min`
- string

Minimum Python version required to run the package. This must be a valid Python 3 version string in the
format '3.Y' or '3.Y.Z', where Y and Z are minor and patch versions, respectively.


### `package.operating_systems`
- dictionary

Operating systems supported by the package, as a dictionary with the following keys:
- `windows`
- `macos`
- `linux`
Each value may be an empty dictionary, or a dictionary with the following keys:
- `runner`: string, optional
- `cibw_build`: string, optional


### `package.trove_classifiers`
- list of strings

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

### `package.dependencies`
- list of dictionaries

Dependencies of the package, as a list of dictionaries with the following keys:
- `name`: string, required
- `pip_spec`: string, required,
- `conda_spec`: string, optional, default: `null`
- `conda_channel`: string, optional, default: `conda-forge`
- `usage`: string, optional, default: `null`
- `url_homepage`: string, optional, default: `null`
- `url_docs`: string, optional, default: `null`
- `url_source`: string, optional, default: `null`


### `package.optional_dependencies`


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


## Website Settings

### `navbar_icons`
- list of dictionaries, optional, default: `null`

### `quicklinks`
- list of lists of dictionaries, optional, default: `null`
