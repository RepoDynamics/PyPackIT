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


(manual-cc-configpaths)=
## Configuration Paths

We use [JSONPath](#intro-jsonpath) path expressions
to refer to a specific configuration's location in the control center.
For example, you can set the name of your project at [`$.name`](#ccc-name),
i.e., as the value of the `name` key in the top-level control center mapping.
In which control center YAML file this key is defined (if at all) is completely up to you,
as [explained earlier](#manual-cc-structure-customization).


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
