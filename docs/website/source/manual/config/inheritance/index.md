(cc-inheritance)=
# Inheritance

While [templating](#manual-cc-templating)
greatly reduces data redundancy, facilitates maintenance, and ensures consistency
*within* a project, inheritance does the same *across* multiple projects,
allowing you to easily share and reuse configurations and metadata between projects
and manage them from a single source.
For example, if you have a GitHub organization with multiple repositories,
you can create a repository containing all the shared configurations and metadata,
and have all other repositories inherit them dynamically.
During [synchronization](#manual-cc-sync) events,
|{{ ccc.name }}| automatically downloads the data from the specified URLs
and merges them with your control center configurations.


:::{include} /_snippets/admo_caching.md
:::


## Syntax

Inheritance works similarly to templating, but instead of referencing
a path within your project's control center configurations,
you can reference a URL to any `JSON`, `YAML`, or `TOML` data file,
along with an optional template to extract specific data from it.
Inherited values are defined using a custom [YAML tag](#yaml) named `ext`,
with the syntax `!ext <URL> [<TEMPLATE>]`, where:
- `!ext` defines the tag.
- `<URL>` is the URL to the data file.
  It must end with `.json`, `.yaml`, `.yml`, or `.toml` (case-insensitive).
- `[<TEMPLATE>]` is an optional [template](#manual-cc-templating)
  to generate or extract data from the data file.
  If omitted, the top-level data structure (i.e., the entire file) is used.


::::{admonition} Example
:class: tip dropdown toggle-shown

Assume you have a GitHub organization named `MyOrg`,
where the same team members work on multiple repositories.
Instead of setting [`$.team`](#ccc-team) in each repository's control center to the same data,
you can create a shared file, e.g., `team.yaml`, in one of your repositories, e.g., `MyOrg/.Control`,
containing the shared `$.team` data. For example:

:::{code-block} yaml
:caption: Shared `team.yaml` file

member1:
  github:
    id: jane-doe
member2:
  github:
    id: john-doe
:::

Assuming the file is located at the root of the `main` branch,
its URL would be `https://raw.githubusercontent.com/MyOrg/.Control/refs/head/main/team.yaml`
(notice the use of the `raw.githubusercontent.com` domain that serves the raw file content
instead of an HTML page). Now, in your other repositories' control centers,
you can set the `$.team` value to the shared data as follows:

:::{code-block} yaml
:caption: Inheriting `$.team` from the shared file

team: !ext https://raw.githubusercontent.com/MyOrg/.Control/refs/head/main/team.yaml
:::

An alternative scenario is when you want to extract only a specific part of the shared data.
Assume the team data is structured in a `config.yaml` file as follows:

:::{code-block} yaml
:caption: Shared `config.yaml` file

some-key: some-value
members:
  member1:
    github:
      id: jane-doe
  member2:
    github:
      id: john-doe
:::

To extract only the `team` data, you can add a template to the tag:

:::{code-block} yaml
:caption: Inheriting `$.team` from a specific part of the shared file

team: !ext https://raw.githubusercontent.com/MyOrg/.Control/refs/head/main/config.yaml ${{ members }}$
:::

You can also use any other templating feature for more complex data extractions.
::::
