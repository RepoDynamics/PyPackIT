# Project Credits

:::::{tab-set}
::::{tab-item} Info
- **Relative Path**: `{{ pp_meta.custom.meta[docname].path }}`
- **Pre-configured**: {{ pp_meta.custom.meta[docname].pre_config }}
::::
::::{tab-item} Schema
:::{code-block} yaml
{{ pp_meta.custom.meta[docname].schema_str }}
:::
::::
::::{tab-item} Default
:::{code-block} yaml
{{ pp_meta.custom.meta[docname].default_str }}
:::
::::
::::{tab-item} Example
:::{code-block} yaml
{{ pp_meta.custom.meta[docname].example_str }}
:::
::::
:::::

All metadata declaring the authors, funding options, and other credits for your project
are stored in the `core/credits.yaml` file in the repository's `meta` directory.


## Authors
You can declare the core authors of your project, and optionally their roles,
by adding an `author` key to the `core/credits.yaml` file.

### Authors Roles
To assign roles to authors, you must first declare these roles under the `role` key
of the `author` object. The value of the `role` key must be an object,
where the keys are the IDs of the roles (to be assigned to authors),
and the values are objects containing the following keys:
- `title`: The name of the role.
- `description`: A short description of the role.
- `abbreviation`: An abbreviation for the role.

Example:
:::{code-block} yaml
:caption: 🗂 `./.meta/core/credits.yaml`
author:
  role:
    concept:
      title: Conceptualization
      description: Development of the initial idea for the project.
      abbreviation: CNCPT
    dev:
      title: Software Development
      description: Implementation of the project.
      abbreviation: DEV
    maint:
      title: Maintenance
      description: Maintenance of the project.
      abbreviation: MAINT
:::


### Authors List
To declare the authors of your project, add a key `entries` to the `author` object,
where the value is an array of objects, each declaring a single author.
Each object must contain a key `username` with the GitHub username of the author,
and optionally a key `roles` with the IDs of the roles assigned to the author.

Example:
:::{code-block} yaml
:caption: 🗂 `./.meta/core/credits.yaml`
author:
  entries:
    - username: ${{ owner.username }}
      roles: [ concept, dev, maint ]
    - username: RepoDynamicsBot
      roles: [ maint ]
:::


## Funding Options
GitHub allows you to add a *Sponsor* button together with a *Sponsor this project* section
to the main page of your repository, to increase the visibility of funding options
for your open-source project. Clicking on the *Sponsor* button opens the *Sponsor this project* section,
where a list of links to your specified funding platforms is displayed to the user.
GitHub lets you specify up to four sponsored GitHub accounts (one of which can be a GitHub organization),
up to four custom URLs,
plus one name (either username, package name, or project name, depending on the platform)
per supported external funding platform (see below).
For more information, see the [About GitHub Sponsors](https://docs.github.com/en/sponsors/getting-started-with-github-sponsors/about-github-sponsors)
and [Displaying a sponsor button in your repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/displaying-a-sponsor-button-in-your-repository)
pages in the [GitHub Sponsors Docs](https://docs.github.com/en/sponsors/receiving-sponsorships-through-github-sponsors).

All configurations are set under the `funding` key in the `core/credits.yaml` file.
If the file/key is not present (default), this option will be disabled.
If set, the value of the `funding` key must be an object with any number of
the supported key-value pairs (one for each type of platform) described below.

 Example:
```yaml
funding:
   github: [ repodynamics, aariam ]
   tidelift: pypi/PyPackIT
   custom: https://some-custom-funding-platform.com/my-project
```

GitHub looks for a YAML file at `.github/FUNDING.yml` in the default branch of the repository;
If it exists and has the correct format, GitHub will display the
*Sponsor* button and *Sponsor this project* section on the repository's main page,
and will use the information in the file to populate the *Sponsor this project* section,
otherwise, the *Sponsor* button and *Sponsor this project* section will not be displayed.
{{ name }} automatically generates the `.github/FUNDING.yml` file when the `funding` key is set,
and will update/remove the file when the `funding` key is updated/removed.


### [GitHub Sponsors](https://github.com/sponsors)

To add sponsored GitHub accounts, add a key `github`, where the value is either a single
GitHub username, or an array of up to four GitHub usernames.
Example (single username):
```yaml
funding:
   github: aariam
```
Example (multiple usernames):
```yaml
funding:
   github: [ repodynamics, aariam ]
```


### [LFX Mentorship (CommunityBridge)](https://lfx.linuxfoundation.org/tools/mentorship)

To add an LFX Mentorship (CommunityBridge) account, add a key `community_bridge`,
where the value is the name of the project on LFX.
Example:
```yaml
funding:
   community_bridge: pypackit
```


### [IssueHunt](https://issuehunt.io/)

To add an IssueHunt account, add a key `issuehunt`,
where the value is your IssueHunt username.
Example:
```yaml
funding:
   issuehunt: aariam
```


### [Ko-fi](https://ko-fi.com/)

To add a Ko-fi account, add a key `ko_fi`,
where the value is your Ko-fi username.
Example:
```yaml
funding:
   ko_fi: aariam
```


### [Liberapay](https://liberapay.com/)

To add a Liberapay account, add a key `liberapay`,
where the value is your Liberapay username.
Example:
```yaml
funding:
   liberapay: aariam
```


### [Open Collective](https://opencollective.com/)

To add an Open Collective account, add a key `open_collective`,
where the value is your Open Collective username.
Example:
```yaml
funding:
   open_collective: aariam
```


### [Otechie](https://otechie.com/)

To add an Otechie account, add a key `otechie`,
where the value is your Otechie username.
Example:
```yaml
funding:
   otechie: aariam
```


### [Patreon](https://www.patreon.com/)

To add a Patreon account, add a key `patreon`,
where the value is your Patreon username.
Example:
```yaml
funding:
   patreon: aariam
```


### [Tidelift](https://tidelift.com/)
- Key: `tidelift`
- Type: `string`

To add a Tidelift account, add a key `tidelift`,
where the value is a string with the format `<PLATFORM-NAME>/<PACKAGE-NAME>`.
`<PACKAGE-NAME>` is the name of your package, and platform name is the name of the package manager
hosting your package; it must be one of the following:
`npm`, `pypi`, `maven`, `rubygems`, `nuget`, `packagist`.
Example:
```yaml
funding:
   tidelift: pypi/PyPackIT
```
