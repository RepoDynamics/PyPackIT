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
  [discussions](https://docs.github.com/en/discussions/collaborating-with-your-community-using-discussions/about-discussions) etc.
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


A prominent feature of {{ pp_meta.name }} is the centralized control center it provides;
