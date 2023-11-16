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
- Building and deploying your website to [GitHub Pages](https://pages.github.com/).
- Managing and updating your [GitHub repository's settings](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features)
  and various features, such as
  [security analysis](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-security-and-analysis-settings-for-your-repository),
  [branch protection rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches),
  [labels](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels),
  [topics](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics),
  [funding options](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/displaying-a-sponsor-button-in-your-repository),
  [social media preview](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview),

- Adding and dynamically updating various GitHub configuration files, such as
  [README files](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes),
  [license files](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository),
  [issue templates](https://docs.github.com/en/issues/using-templates-for-issues-and-pull-requests/about-issue-and-pull-request-templates),
  [discussion templates](https://docs.github.com/en/discussions/setting-up-and-managing-discussions/configuring-a-discussions-template-for-your-repository),
  [pull request templates](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-issue-and-pull-request-templates),
  [code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners),
  [citation files](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files),

  [pre-commit hooks](https://pre-commit.com/),
  and [many more](#../manual/usage/meta.md#meta-files).


A prominent feature of {{ pp_meta.name }} is the centralized control center it provides;
