# GitHub Directory

Every repository must contain a `./.github` directory,
i.e., a directory named `.github` located at the root (`./`) of the repository.
This is where GitHub looks for GitHub Actions workflow files
(`.yaml` files in the `./.github/workflows` directory) and other configuration files,
such as issue-, discussion-, and pull request templates.

When a repository is first initialized from the {{pp_meta.name}} template,
the `./.github` directory will only contain workflow files.
These are configurations that define the continuous integration and delivery (CI/CD)
pipelines of the repository, allowing the whole development and maintenance process of your project
to be automatically managed by {{pp_meta.name}}.
In general, you should never modify these files directly, since all configurations and data that
are specific to each project are read automatically from the repository's `meta` content (discussed below).
The only exception is when you want to add a new feature/functionality to your pipelines,
which is not covered by {{pp_meta.name}} and is completely orthogonal to its functionalities.

After the repository is configured, a number of other files and directories
will also be automatically added to the `./.github` directory,
including issue-, discussion-, and pull request templates, and other GitHub configuration files.
{{pp_meta.name}} also uses the `./.github` directory to store some of its own data and settings,
as well as configuration files for other external tools that are used by {{pp_meta.name}}.
You must never modify these files directly, as they are dynamic files that are automatically
generated and updated by {{pp_meta.name}} according to the repository's `meta` content.
