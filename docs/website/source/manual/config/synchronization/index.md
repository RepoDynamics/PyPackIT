(manual-cc-sync)=
# Synchronization

|{{ ccc.name }}|'s CCA pipeline automatically
applies all control center configurations
to corresponding components,
ensuring that your entire project is always
in sync with your specifications.
The CCA pipeline is automatically triggered on GHA
whenever commits are pushed to a branch,
and during scheduled Continuous maintenance pipelines.
In addition, they can also be invoked manually both on GHA
and on local machines.
During each run, |{{ ccc.name }}| first compiles your control center settings by
reading all your configuration files,
augmenting them with dynamically generated data,
resolving all templates and inherited configurations,
filling in missing values with defaults,
and validating all configurations against a predefined schema.
This full version of your project configurations is then used
to automatically generate content for your project
and configure its different components via tool-specific APIs
and configuration files.
It is also written to a single JSON file at `.github/repodynamics/metadata.json`,
from which your entire project configurations can be easily accessed both locally and online.
For example, the content of the `metadata.json` file
is automatically passed to your website during builds,
essentially rendering your entire documentation dynamic.


The exact steps of |{{ ccc.name}}|'s CCA pipeline are as follows:

1. The `metadata.json` file in the current branch is loaded and validated.
   This is used as a reference for the current state of the repository (i.e., before synchronization),
   which is needed by some routines that generate data based on changes.
   If the pipeline is being run GHA, the metadata file is loaded from the latest
   commit hash **before** the event.
2. The `metadata.json` file in the main branch (if not the same as the current branch)
   is loaded and validated.
   This is used as a reference for current project-wide configurations,
   such as branch and tag name specifications.
3. Initialization hooks are executed, if specified.
4. The control center configuration files in the current branch are loaded
   and merged. Inherited configurations are resolved and merged as well,
   either using cached data (if a non-expired cache exists),
   or by retrieving the resources via HTTP requests.
5. Load hooks are executed, if specified.
6. Loaded configurations are validated against the schema.
7. Load validation hooks are executed, if specified.
8. Configurations are augmented with automatically generated data,
   such as various repository information and statistics,
   team member information, and license data.
9. Augmentation hooks are executed, if specified.
10. Augmented configurations are validated against the schema.
11. Augmentation validation hooks are executed, if specified.
12. All templates are recursively resolved in configurations.
13. Templating hooks are executed, if specified.
14. The complete set of configurations is validated against the schema,
    filling all remaining default values defined by the schema.
15. Templating validation hooks are executed, if specified.
16. The local cache file is updated with all newly retrieved data.
17. All dynamic files are generated from the new configurations,
    and compared to the current state of the repository (cf. step 1)
    to determine which files to create, delete, duplicate, move, and/or modify.
18. Configurations for dynamic directories are compared as well,
    to determine which directories to create, delete, or move.
19. Output generation hooks are executed, if specified.
20. Necessary changes are applied to all dynamic files and directories in the branch,
    including the `metadata.json` file, which now reflects
    the current state of the repository after synchronization.
21. Synchronization hooks are executed, if specified.
22. Comprehensive reports are generated, detailing all applied changes.


Furthermore, if the pipeline is being run on GHA,
further actions are performed depending on the triggering event and your configurations:

- If changes are made to dynamic files and directories,
  they are committed and pushed to the repository.
  This is done either directly to the current branch, or to a new branch
  from which a pull request will be automatically created.
  In cases where this is not desired or possible (e.g., when pull requests from forks are synchronized),
  the pipeline will either emit a failure code (e.g., for pull request status checks)
  or simply return the report, without actually applying any changes.
- If the current branch is the main branch, project-wide configurations
  are applied to the repository. This is done either via the GitHub API
  (e.g., for updating branch/tag names and protection rules, labels, and other repository settings)
  or through the updated dynamic configuration files that are only recognized on the main branch
  (e.g., issue and discussion forms, license, citation, funding).
