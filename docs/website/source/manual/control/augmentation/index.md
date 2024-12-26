# Augmentation

|{{ ccc.name }}| automatically augments your project's metadata
with various additional data,
so that you don't have to manually define and update them.
These are dynamically generated at runtime each time the control center is being processed
(e.g., during synchronization events),
and are then added to the control center at specific locations,
and can be used just like any other control center content.
The added data are generated in three ways:
pre-configured default values, local calculations, and external data retrieval.


## Default Values

Many control center configurations whose values can be automatically determined
from other configurations are given default values using [templating](#manual-control-templating) features.
For example, there are several URLs defined under [`$.repo.url`](#ccc-repo-url),
each pointing to a specific part of your GitHub repository.
All of these are automatically set based on other repository data.
For example, [`$.repo.url.blob`](#ccc-repo-url-blob),
which points to *blob* view of the repository's main branch,
is set to `${‎{ repo.url.home }}/blob/${‎{ branch.main.name }}`,
where `${‎{ repo.url.home }}` is the URL of the repository's home page,
automatically retrieved from the GitHub API, and `${‎{ branch.main.name }}`
is the name of the main branch, which is configurable in the control center.


## Calculation

|{{ ccc.name }}| processes your entire Git repository each time the control center is being processed,
and generates various data that are then added to the control center
and used in other parts of the project.
For example, it analyzes each (pre)release branch of the repository and its control center configurations,
and generates a summary of all releases and their corresponding information,
which is then added to the [`$.project`](#ccc-project) key of the control center.
These can then be dynamically referenced in other parts of your project.
For example, they are used in [issue form definitions](#ccc-issues-forms)
which reference available release versions, supported Python versions,
and other release-specific information
for users to select from when submitting an issue.


## Retrieval

Various web APIs are used to retrieve additional data about your project.

:::{include} /_snippets/admo_caching.md
:::


### Account Information

The [GitHub API](https://docs.github.com/en/rest?apiVersion=2022-11-28)
is used to retrieve information on your GitHub repository and team members:

- Repository details such as [`$.repo.name`](#ccc-repo-name),
  [`$.repo.full_name`](#ccc-repo-full-name),
  [`$.repo.url.home`](#ccc-repo-url-home),
  [`$.repo.id`](#ccc-repo-id), [`$.repo.node_id`](#ccc-repo-node-id),
  [`$.repo.default_branch`](#ccc-repo-default-branch),
  and [`$.repo.created_at`](#ccc-repo-created-at)
  are automatically filled.
- For all team members defined under [`$.team`](#ccc-team)
  (including the automatically added [`$.team.owner`](#ccc-team-owner)),
  their full information is fetched from GitHub, including their full name,
  email, bio, profile picture, affiliation, and linked social accounts,
  and added to the respective keys in their [`Entity`](#cccdef-entity) mapping.


### Publications

For any team member defined under [`$.team`](#ccc-team)
who has an [`orcid.id`](#cccdef-entity-orcid-id) and has set [`orcid.get_pubs`](#cccdef-entity-orcid-get-pubs),
|{{ ccc.name }}| uses the [ORCiD API](https://info.orcid.org/documentation/features/public-api/)
to retrieve a list of their publications, and for each publication,
it fetches full metadata and citation information from the
[Crossref](https://www.crossref.org/documentation/retrieve-metadata/rest-api/)
[DOI](https://www.doi.org/the-identifier/resources/factsheets/doi-resolution-documentation) APIs.
These are then added to the [`orcid.pubs`](#cccdef-entity-orcid-pubs) key
of the respective team member's [`Entity`](#cccdef-entity) mapping.
