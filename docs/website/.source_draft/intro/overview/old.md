# Overview

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
  by |{{ ccc.name }}|, such as
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
