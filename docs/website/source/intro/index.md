# Intro
:::{toctree}
:hidden:

overview/index
fundamentals/index
:::

{{ pp_meta.name }} is provided as a
[GitHub template repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository),
and uses [GitHub Actions](https://github.com/features/actions)
to automate the entire development and maintenance process of your project.
When you [create a new repository from the {{ pp_meta.name }} template](#../manual/getting-started/new-repo.md),
or [integrate {{ pp_meta.name }} into your existing repository](#../manual/getting-started/existing-repo.md),
fully configured [GitHub Actions workflows](https://docs.github.com/en/actions/using-workflows/about-workflows)
are added to your repository,
which will automatically run GitHub Actions every time a supported event occurs in your repository.
These workflows use {{ pp_meta.name }}'s own
[custom actions](https://docs.github.com/en/actions/creating-actions/about-custom-actions),
most notably the [RepoDynamics Action](https://github.com/RepoDynamics/init),
which is entirely powered by our [RepoDynamics Python package](https://github.com/RepoDynamics/RepoDynamics).
This package, being the brain of the {{ pp_meta.name }} software suite,
is responsible for analyzing the event that triggered the workflow,
along with the current state of the repository, and automatically performing a variety of tasks accordingly.
These include:
- Versioning, tagging, building and publishing new releases of your package to
  [PyPI](https://pypi.org/) and [TestPyPI](https://test.pypi.org/) platforms.
- Generating release notes, updating changelogs, and creating
  [GitHub releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases),
  blog posts and website announcements for each package release.
- Updating, building and deploying your website to [GitHub Pages](https://pages.github.com/).
- Processing and managing your project's
  [issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues),
  [pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests),
  [branches](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-branches),
  [tags and releases](https://docs.github.com/en/repositories/releasing-projects-on-github/viewing-your-repositorys-releases-and-tags),
  and [discussions](https://docs.github.com/en/discussions/collaborating-with-your-community-using-discussions/about-discussions),
  including assigning issues to maintainers, dynamically labeling issues and pull requests,
  creating development branches for issues, opening pull requests and requesting reviews,
  merging pull requests, and creating and updating tags, releases, and branches.
- Managing and updating your [GitHub repository's settings](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features)
  and various features, such as
  [security analysis](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-security-and-analysis-settings-for-your-repository),
  [branch protection rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches),
  [labels](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels),
  [topics](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics),
  [funding options](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/displaying-a-sponsor-button-in-your-repository),
  [social media preview](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview) etc.
- Adding and dynamically updating various GitHub configuration files, such as
  [README files](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes),
  [license files](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository),
  [issue templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates#issue-templates),
  [discussion templates](https://docs.github.com/en/discussions/managing-discussions-for-your-community/creating-discussion-category-forms),
  [pull request templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates#pull-request-templates),
  [code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners),
  [citation files](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files),
  and other [community health files](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file)
  such as [code of conduct](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/adding-a-code-of-conduct-to-your-project),
  [contributing guidelines](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/setting-guidelines-for-repository-contributors),
  [security policy](https://docs.github.com/en/code-security/getting-started/adding-a-security-policy-to-your-repository),
  [support resources](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/adding-support-resources-to-your-project),
  and governance policy.
- Adding and dynamically updating configuration files for other external tools that are used/supported
  by {{ pp_meta.name }}, such as
  [Read The Docs](https://readthedocs.org/) website,
  [Codecov](https://codecov.io/) test coverage reports,
  branch-specific [pre-commit](https://pre-commit.com/) configuration files,
- Adding and dynamically updating git-specific files, such as [gitignore](https://git-scm.com/docs/gitignore)
  and [gitattributes](https://git-scm.com/docs/gitattributes).
- Providing and dynamically updating Python-specific files for your package and test-suite,
  including [`requirements.txt` files](https://pip.pypa.io/en/stable/reference/requirements-file-format/),
  [`MANIFEST.in` files](https://packaging.python.org/en/latest/guides/using-manifest-in/), and
  fully configured `pyproject.toml` files with specifications for the [build process](https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/)
  and [packaging with Setuptools](https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html),
  [PEP 621 metadata](https://packaging.python.org/en/latest/specifications/declaring-project-metadata/#declaring-project-metadata),
  and settings for various tools such as
  [versioningit](https://versioningit.readthedocs.io/en/stable/)
  (for automatic version determination based on repository tags),
  [Ruff](https://docs.astral.sh/ruff/), [Mypy](https://mypy.readthedocs.io),
  [Pylint](https://pylint.readthedocs.io/), [black](https://black.readthedocs.io)
  and [isort](https://pycqa.github.io/isort/) (for code linting and formatting),
  and [pytest](https://docs.pytest.org/) and [coverage.py](https://coverage.readthedocs.io/) (for testing and code coverage).
- Updating all directory-specific README files throughout the repository.

Another prominent feature of {{ pp_meta.name }} is the centralized control center it provides;
all metadata, configurations, and settings required for the above tasks are thoughtfully structured
and gathered in one place, under a single directory in your repository, called the `meta` directory.
When you apply a change to the repository's `meta` content, {{ pp_meta.name }} will automatically
apply the corresponding changes to the entire repository and its contents, and update all relevant files,
configurations, and settings accordingly. Therefore, besides your source code, unit tests, and documentation content,
all other aspects of your project are automatically managed by {{ pp_meta.name }} according to your specifications
in the `meta` directory. {{ pp_meta.name }} also allows for complex and recursive templating for all the `meta` content,
meaning that you can reference and use any part of the `meta` content in all other parts, eliminating the need for
redundant and repetitive configurations and data, which are hard to modify.
This provides a high degree of customization and flexibility,
as you can easily change a single variable, and have it automatically applied to the entire `meta` contents
and consequently the entire project.
To further reduce unnecessary redundancies, {{ pp_meta.name }} also lets you dynamically inherit
specific `meta` contents of other repositories, allowing you to easily create and maintain
multiple repositories with centralized configurations and settings.

On top of this, {{ pp_meta.name }} also automatically extends your project's metadata
by fetching additional information from external sources.
For example:
- Name and the owner of the repository are automatically detected, and their full information
  is retrieved from the [GitHub API](https://docs.github.com/en/rest?apiVersion=2022-11-28).
- Information on the repository owner and all specified authors and maintainers,
  such as full name, email, bio, profile picture, affiliation, and linked social accounts,
  is fetched from the GitHub API.
- If the owner specifies their [ORCiD](https://orcid.org/) ID in their GitHub profile,
  their ORCiD profile information is automatically fetched from the [ORCiD API](https://info.orcid.org/documentation/features/public-api/),
  a list of their publications is extracted, and full metadata and citation information
  for each publication is retrieved from the
  [Crossref](https://www.crossref.org/documentation/retrieve-metadata/rest-api/)
  and [DOI](https://www.doi.org/the-identifier/resources/factsheets/doi-resolution-documentation) APIs.
