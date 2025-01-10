(manual-cc-options)=
# Options

The control center provides
[more than four thousand options](#https-controlman-repodynamics-com-schema-metadata-index)
structured into a number of
[top-level key-value pairs](#https-controlman-repodynamics-com-schema-metadata-properties)
covering every aspect of the project
from general descriptors and metadata
to various workflow setting and tool-specific configurations
({numref}`tab-cc-options-overview`).
All available options are documented in the
[API Reference](#https-controlman-repodynamics-com-schema-metadata),
which is automatically generated from [JSON Schemas](https://json-schema.org/understanding-json-schema)
that define the structure of control center configurations
and are used to validate user settings during [synchronization](#manual-cc-sync) events.


:::{table} An overview of main control center configuration categories. 
:widths: auto
:align: center
:name: tab-cc-options-overview

| Category        | Examples                                                                                                                                                                                   |
|-----------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Descriptors     | Project descriptors like [name](#ccc-name), [title](#ccc-title), [abstract](#ccc-abstract), [keywords](#ccc-keywords), [highlights](#ccc-highlights), and [theme colors](#ccc-color).      |
| Metadata        | Project metadata such as [license](#ccc-license), [copyright](#ccc-copyright), [citation](#ccc-citation), [language](#ccc-language), [funding](#ccc-funding), and [team](#ccc-team).       |
| Packages        | Python [package](#ccc-pkg) and [test suite](#ccc-test) configurations including [build settings](#ccc-pkg-build), [dependencies](#ccc-pkg-dependency), and [entry points](#ccc-pkg-entry). |
| Documentation   | Dynamic [document definitions](#ccc-documents), [discussions categories](#ccc-discussion), and [website configurations](#ccc-web).                                                         |
| Issue Tracking  | Configurations for [issues](#ccc-issue) and [pull requests](#ccc-pull), including [issue forms](#ccc-issus-forms), [protocols](#ccc-issue-protocol), and [labels](#ccc-label).             |
| Version Control | General configurations for the GitHub/Git [repository](#ccc-repo) and its [branches](#ccc-branch), [tags](#ccc-tag), [files](#ccc-file), and [commits](#ccc-commit).                       |
| Workflow        | Workflow configurations such as [role definitions](#ccc-role) and settings for various [Continuous pipelines](#ccc-workflow) and development [tools](#ccc-tool).                           |
:::


(manual-cc-preconfig)=
## Preconfiguration

Almost all available configurations are set to sensible defaults,
requiring most users to only specify a handful of project descriptors
like name, title, and keywords.
For all generic configurations such as tool settings,
default values are provided based on the latest standards and best practices.
For other project-specific configurations,
defaults are included as [dynamic templates](#manual-cc-templating)
that use simple project descriptors and metadata to
automatically generate more complex configurations.
Examples include license, citation, and various documentation files
like READMEs and community health files.

The default values are provided in two different places:
Some are included directly within the JSON Schemas,
and are thus documented in the [API Reference](#https-controlman-repodynamics-com-schema-metadata).
These defaults are [automatically applied](#help-jsonschema-defaults) when the input configurations
are being validated against the schema.
Additional default values are provided in the control center configuration files
included in the |{{ ccc.name }}| repository template at [`.control/`](){.user-link-repo-cc}.
These default values are not documented in the API Reference, but can be simply
reviewed by navigating your project's control center.
The reason for not including all default values in the schemas
is that many |{{ ccc.name }}| functionalities can be disabled
by omitting the corresponding configurations.
These are not included in the schemas, so users can disable features
they do not need simply by removing the corresponding configurations
from the provided configuration files.


## Augmentation

Another way |{{ ccc.name }}| minimizes manual configurations
is by generating and retrieving project-specific statistics
and data at [runtime](#manual-cc-sync). For example:

- **Github repository metadata** like name, ID, owner, creation date, URL,
  and other details are automatically retrieved from the
  [GitHub API](https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#get-a-repository)
  and added to [`$.repo`](#ccc-repo).
- **Team member data** including name, email, affiliation, bio, social accounts,
  and other available information are also retrieved from the
  [GitHub API](https://docs.github.com/en/rest/users/users?apiVersion=2022-11-28#get-a-user)
  and to each member under [`$.team`](#ccc-team).
- **License information** such as license full texts, copyright notices, and various other metadata
  are automatically retrieved from the SPDX database and added to [$.license](#ccc-license),
  requiring users to only define an SPDX license expression for their project.
- **Project statistics** such as released versions and their details,
  active branches and their configurations,
  and a list of dynamically maintained resources
  are automatically generated by analyzing your git repository
  and extracting data from each branch's configuration files.
  These are added to [`$.project`](#ccc-project), and are used for example
  in [issue form definitions](#ccc-issues-forms) to dynamically reference
  available release versions, supported Python versions,
  and other release-specific information
  for users to select from when submitting an issue.
- **Literature citations** can be automatically retrieved.
  |{{ ccc.name }}| can use the [ORCiD API](https://info.orcid.org/documentation/features/public-api/)
  to retrieve all publications of an author, and for each publication,
  it only needs a DOI to fetch full metadata and citation information from the
  [Crossref](https://www.crossref.org/documentation/retrieve-metadata/rest-api/)
  [DOI](https://www.doi.org/the-identifier/resources/factsheets/doi-resolution-documentation) APIs.


(manual-cc-options-custom)=
## Customization

Most control center options only accept a set of
predefined data structures and values, as described in the
[API Reference](#https-controlman-repodynamics-com-schema-metadata).
This is to ensure that all configurations and data are
correctly specified by the user, by validating them against
a predefined schema.

To enable custom user-defined configurations,
|{{ ccc.name }}| allows two special keys
that accept arbitrary values: `__custom__` and `__custom_template__`.
These keys can be added under any mapping in the control center configurations,
except those that already accept additional properties.
For example, you can define a top-level custom key at `$.__custom__`
and add all your custom configurations under it:


:::{code-block} yaml
:caption: Defining custom configurations at `$.__custom__`

__custom__:
  my_custom_sequence:
    - 1
    - 2
    - 3
  my_custom_mapping:
    a: true
    b: false
  my_custom_string: Hello World
:::


There two differences between `__custom__` and `__custom_template__` keys
(see [templating](#manual-cc-templating) for more details):

1. Relative paths in templates defined under `__custom_template__`
   are resolved against the path where that template is referenced, not where it is defined.
2. `__custom_template__` key-value pairs are not included in the [output metadata file](#manual-cc-outputs).

In other words, `__custom_template__` is only meant for intermediate configurations
that are used to generate other settings during synchronization events.
