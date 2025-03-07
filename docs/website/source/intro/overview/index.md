---
ccid: overview
---

(overview)=
# Overview

|{{ ccc.name }}| is a ready-to-use automation tool,
fully configured in accordance with the
latest software engineering guidelines and best practices.
It is an open-source, cloud-based software suite
hosted on [GitHub](#bg-gh) at https://github.com/RepoDynamics,
comprising several [GitHub Actions](#bg-gha) (GHA) [actions](#bg-gha)
and [Python](#bg-py) applications.
These can be installed in GitHub repositories
to perform automated tasks on the GHA cloud framework.
To facilitate [installation](#install), |{{ ccc.name }}| includes a
[repository template](#bg-ghrt) at https://github.com/RepoDynamics/|{{ ccc.name }}|.
There, by clicking the
|{{ '[{{bdg-success}}`Use this template`](https://github.com/new?template_name={}&template_owner={})'.format(ccc.repo.name, ccc.team.owner.github.id) }}|
button, users can create a [new GitHub repository](#install-new)
that automatically contains all the necessary files to run |{{ ccc.name }}|,
such as GHA [workflows](#bg-gha-workflow) and configuration files.
Installation in [existing repositories](#install-existing) is supported as well,
simply requiring users to add these files.

Upon installation, users only need to invest a few minutes
filling project-specific information in the provided configuration files.
|{{ ccc.name }}| then takes over, automatically setting up the repository
and generating a complete infrastructure for the project,
including a build-ready python package,
fully automated test suite,
comprehensive documentation website,
license and citation files,
community health files such as a dynamic repository README,
and configuration files for various development tools and services.
An initial release of the software along with its test suite and documentation website
can be immediately deployed online, registering the project in various indexing repositories
and facilitating its discovery from the beginning.
All metadata and settings are readily customizable via |{{ ccc.name }}|'s configuration files,
which form a unified control center enabling Continuous Configuration Automation
for the entire project infrastructure and development environment
throughout the software life cycle.


:::{image} /_media/figure/workflow_light.svg
:class: hidden
:::
:::{figure} /_media/figure/workflow_dark.svg
:alt: |{{ ccc.name }}| Workflow
:class: dark-light themed
:align: center
:name: fig-workflow

|{{ ccc.name }}|'s software development workflow.
Labeled arrows represent manual tasks performed by users:
**Report**, **Design**, **Commit**, and **Review**.
All other activities are automated,
which fall into four main categories
spanning different stages of the software development life-cycle:
**Issue Management**, **Version Control**, **Continuous Integration and Deployment**,
and **Continuous Maintenance, Refactoring, and Testing**.
:::


After installation, |{{ ccc.name }}| establishes an automated
software development workflow ({numref}`fig-workflow`) tailored to user needs,
based on a well-tested pull-based model
for collaborative software development.
It includes comprehensive Continuous software engineering pipelines
that use the latest tools and technologies
to enable a cloud-native Agile software development process,
allowing for highly iterative and experimental software development,
while reducing variance, complexity, cost, and risk.
|{{ ccc.name }}| activates automatically in response to various repository events,
such as submission of issue tickets, commits, and pull requests.
It then analyzes the triggering event and the current state of the repository
to execute appropriate tasks on [GHA](#bg-gha),
thus automating the bulk of repetitive engineering
and management activities throughout the software life cycle,
which leaves users with only four manual tasks:

1. **Report**: Each task in the project starts by submitting a ticket to its {term}`ITS`.
   |{{ ccc.name }}| facilitates reports by automatically configuring and maintaining [GHI](#bg-ghi)
   to provide users with dynamic submission forms specialized for various issue types.
   Following a ticket submission, |{{ ccc.name }}| automatically performs issue management tasks,
   reducing the triage process to a simple decision on whether to implement the task.
2. **Design**: Once an issue ticket is approved,
   users only need to write a short design document
   by filling out a form attached to the ticket.
   |{{ ccc.name }}|'s automated version control then activates,
   creating a ready-to-use branch for implementation,
   and a dynamically maintained {term}`PR` for tracking progress.
3. **Commit**: With |{{ ccc.name }}|'s comprehensive infrastructure,
   implementation is simplified to writing essential code, docstrings,
   and test cases in the provided skeleton files
   or modifying project configurations in the control center, depending on the task.
   With each commit, |{{ ccc.name }}|'s CI/CD pipelines
   automatically integrate the new changes into the repository,
   performing various quality assurance and testing tasks,
   while producing reports and artifacts for review.
4. **Review**: When the implementation is finished,
   |{{ ccc.name }}| automatically sends review requests to designated maintainers.
   Once approved, |{{ ccc.name }}|'s CI/CD pipelines merge the changes into the project's mainline,
   updating all affected project components and
   generating changelogs that document the entire development process.
   If changes correspond to the software's public interfaces,
   a new version is generated along with release notes and various artifacts,
   which can be automatically published to user-selected indexing repositories and cloud services,
   such as [PyPI](#bg-pypi), [Anaconda](#bg-anaconda-org), Zenodo, and various Docker registries and BinderHub instances.


Moreover, |{{ ccc.name }}| also activates on a scheduled basis,
executing Continuous Maintenance, Refactoring, and Testing pipelines
that perform various maintenance and monitoring tasks
on the repository and each released library version,
sustaining the health of the software and its development environment.
When actions are required, these pipelines automatically submit
issue tickets for manual implementation,
PRs for automatic fixes that require review,
or they directly apply updates to the project.
To further support developers during the implementation phase,
|{{ ccc.name }}| encapsulates the project's development environment into
[development containers](https://containers.dev).
Powered by [GitHub Codespaces](https://github.com/features/codespaces) and
[Visual Studio Cod](https://code.visualstudio.com) (VSCode),
these containers can run both locally and on the cloud,
providing all contributors with a consistent,
ready-to-use workspace with all required tools preinstalled and configured.

The rest of this section offers a more detailed overview
of some of |{{ ccc.name }}|'s key components, features and capabilities.


(overview-cc)=
## Continuous Configuration Automation

|{{ ccc.name }}| enables automatic [project configuration](#motiv-cca),customization, and management
by introducing a centralized control mechanism based on [CCA](#bg-cca) and [IaC](#bg-iac) practices.
It provides a [control center](#manual-cc) as the singular user interface
to dynamically manage the entire project, and even multiple projects at once.
|{{ ccc.name }}|'s control center unifies and [structures](#manual-cc-structure) all project configurations,
metadata, and variables into declarative definitions in [YAML](#yaml)—a
standard human-readable data serialization format.
These are consolidated into one repository [location](#manual-cc-location) under version control,
allowing for easy tracking of settings throughout the project lifespan,
and eliminating the need for maintaining multiple configuration files in
different formats and locations.
Using APIs and dynamically generated files, |{{ ccc.name }}| automatically applies all
control center settings to corresponding components,
replacing manual configurations with replicable declarations and
making the entire project highly dynamic and customizable.
To further simplify dynamic project configuration and content management,
the control center is equipped with several features:

- [**Preconfiguration**](#manual-cc-preconfig):
  Default settings are provided based on the latest standards and best practices,
  requiring only project-specific metadata to be declared.
- [**Augmentation**](#manual-cc-augment):
  Project information and statistics are automatically generated at runtime
  by analyzing the repository and retrieving information from web APIs,
  minimizing manual inputs.
- [**Templating**](#manual-cc-templating):
  Dynamic data generation and reuse is enabled for the entire repository
  by a specialized templating engine,
  eliminating redundancy and allowing for centralized and automatic updates.
- [**Inheritance**](#manual-cc-inheritance):
  Configurations can be automatically inherited from external sources over HTTP requests,
  allowing for consistent creation and centralized maintenance
  of multiple projects with shared settings.
- [**Customization**](#manual-cc-hooks):
  Additional configurations and workflow routines can be added
  either declaratively in YAML files or dynamically via Python plugins executed at runtime,
  maximizing customizability.
- [**Validation**](#manual-cc-options):
  Inputs are thoroughly validated against predefined schemas,
  providing comprehensive error reports for any inconsistencies.
- [**Synchronization**](#manual-cc-sync):
  Changes are automatically propagated throughout the project,
  ensuring consistency across all components without the need for manual intervention.
- [**Caching**](#manual-cc-cache):
  Intermediate data such as those retrieved from web APIs can be cached both locally and on GHA
  to speed up the process, with configurable retention times.


(overview-pkg)=
## Python Package

|{{ ccc.name }}| provides a comprehensive infrastructure for Python packages,
in line with the latest [PyPA](#bg-pypa) standards {cite}`PythonPackagingUserGuide`.
It offers a build-ready [import package](https://packaging.python.org/en/latest/glossary/#term-Import-Package)
containing key source files with basic functionalities for data file support,
error handling, and command-line interface development.
Users simply need to extend these files with their application code,
while PyPackIT's control center automatically provides all package configurations
and allows for dynamic modification of modules,
e.g., to add docstrings, comments, and code snippets.

In addition to pure-Python packages, PyPackIT also supports packages
with extension modules and non-Python dependencies.
This is crucial for many applications that rely on extensions
and dependencies written in compiled languages like C and C++ for compute-heavy calculations.
All necessary build configuration files such as
[pyproject.toml](https://packaging.python.org/en/latest/specifications/pyproject-toml/)
and [Conda-build recipes](https://docs.conda.io/projects/conda-build/en/latest/concepts/recipe.html)
are automatically generated using control center settings,
providing extensive project metadata to facilitate packaging,
publication, and installation in PyPI and Anaconda ecosystems.

Unique identifiers such as version numbers, DOIs, and release dates
are also automatically generated for each build and added to the package.
This dynamic package skeleton allows users to focus on writing application code,
while PyPackIT ensures quality and FAIRness by automatically taking care of
other tasks such as testing, refactoring, licensing, versioning, packaging,
and distribution to multiple indexing repositories
with comprehensive metadata and persistent identifiers.


(overview-testsuite)=
## Test Suite

|{{ ccc.name }}| simplifies software testing
by providing a fully automated testing infrastructure
built on [PyTest](https://pytest.org/),
one of the most popular testing frameworks for Python.
The testing infrastructure supports unit, regression, end-to-end, and functional testing,
which are integrated into PyPackIT's Continuous pipelines
and automatically executed during software integration, deployment, and maintenance.
For writing tests, PyPackIT provides a separate Python package skeleton
next to the project's main package.
This test suite includes the same
automation and preconfiguration features as the main package,
requiring users to only add test cases.
It can be easily installed via Pip and Conda,
replacing complex testing environment setups.
PyPackIT also adds a command-line interface to the test suite,
simplifying its execution by abstracting the details of running Pytest.
During each release, the test suite is automatically licensed, versioned, packaged,
and distributed along the software,
allowing users to run tests and benchmarks on their machines and get detailed reports.
Moreover, isolating the tests from the main package
improves compatibility and reduces the overall size of the software.
Structuring tests into a package also enhances modularity and reusability,
simplifying the development of new test cases.

PyPackIT generates detailed test results and coverage reports
in both machine and human-readable formats,
using plugins such as [PyTest-Cov](https://github.com/pytest-dev/pytest-cov).
These reports are made available on the repository's GHA dashboard for each run,
and can be automatically uploaded to coverage analysis platforms like [Codecov](https://codecov.io/)  
to provide deeper insights into testing effectiveness.
Testing outcomes are also automatically reflected in PRs and READMEs
via dynamic badges and notifications,
informing project members and users about the software's health status.
By default, PyPackIT also enables branch and tag protection rules
requiring all PRs to pass quality assurance and testing status checks
before they can be merged into the mainline.


(overview-docs)=
## Documentation

|{{ ccc.name }}| offers an automated solution for generating,
deploying, and maintaining a comprehensive documentation website
according to best practices {cite}`TenSimpleRulesForDocumentingSciSoft, WhatMakesCompSoftSuccessful`,
significantly reducing the manual effort down to writing docstrings and brief software descriptions.

It includes a fully configured [Sphinx](https://www.sphinx-doc.org) website,
designed using a standardized layout
based on the popular [PyData](https://pydata-sphinx-theme.readthedocs.io/) theme.
Website configurations and content
are dynamically managed by |{{ ccc.name }}|'s control center,
enabling rapid customization and consistent updates.
Moreover, [Jinja](https://jinja.palletsprojects.com/) templating is enabled
for all documentation files, with access to the entire control center.
This enables the creation of sophisticated dynamic content
from control center data,
allowing |{{ ccc.name }}| to automatically generate project-specific
documentation materials that are continuously updated throughout the development process.
These include:

- **Homepage**: Logo, abstract, keywords, highlights,
  and links to various internal and external project resources.
- **Project Information**: License, copyright, citation, contributors, governance model, and contact information.
- **Package Metadata**: Python and OS requirements, dependencies, entry points, and versioning scheme.
- **Installation Guide**: Detailed instructions on how to install the package from available sources.
- **API Reference**: Documentation of all package components
  extracted from source code docstrings.
- **Changelogs**:
  Chronological record of the entire development process,
  auto-generated from issue tickets, PR data, and configuration changes.
- **Release Notes**:
  Detailed summaries for each release, providing a complete list of changes
  along with related identifiers and links to resources.
- **Contribution Guide**: Manuals on how to report issues,
  request changes, contribute artifacts, and maintain the software project.
- **Support Guide**: Instructions on how to find resources, fix common problems, ask questions,
  and seek further support.

The website is further equipped with plugins such as
[MyST-NB](https://myst-nb.readthedocs.io/en/latest/),
[Sphinx-Design](https://sphinx-design.readthedocs.io/),
and [SphinxContrib-BibTeX](https://sphinxcontrib-bibtex.readthedocs.io/),
which enable executable code blocks, diagrams, charts, math notation, figures,
tables, bibliographies, and responsive elements like admonitions, grids, and drop-down components.
These are available via simple directives in powerful markup languages like
[MyST Markdown](https://mystmd.org/) and reStructuredText (reST),
allowing for rich and technical documents.
Moreover, a news blog with support for commenting,
searching, content categorization and RSS feeds is integrated using
[ABlog](https://ablog.readthedocs.io/) and [Giscus](https://giscus.app/),
establishing communication between the project and its community.
PyPackIT can also automate blog posting for events like new releases and critical bug fixes,
further simplifying the documentation effort.

Website build and deployment are also automated by |{{ ccc.name }}|'s CI/CD pipelines.
Changes affecting the website trigger an automatic build process,
which provides a preview for review.
Once approved, the updated website is deployed on
[GitHub Pages](https://pages.github.com/)---a free static web hosting service---accessible
online through a default `github.io` domain.
If preferred, users can also specify a custom domain in the control center.
Additionally, hosting on the [Read The Docs](https://readthedocs.org/) platform is supported,
requiring only an account configuration.
To improve project visibility and searchability,
[Open Graph](https://ogp.me/) metadata is embedded into each page using the
[SphinxExt-OpenGraph](https://github.com/wpilibsuite/sphinxext-opengraph) plugin,
enabling search engine optimization (SEO) and rich social media previews.

Furthermore, PyPackIT can dynamically generate [Markdown](#bg-markdown) documents in various flavors,
from declarative instructions in the control center.
This enables the creation of complex documents without writing any Markdown.
Instead, users simply declare the type and content of elements,
which PyPackIT can use to generate Markdown files for different specifications.
When an element is not supported in a specification, PyPackIT can automatically
generate a similar supported element.
This is mainly used to add
[community health files](#bg-gh-health-files)
and platform-specific README files
for [GitHub](#bg-gh-writing)
and other indexing repositories like [PyPI](#bg-pypi-readme),
which have specific restrictions for README files.
Serving as the front page of the repositories,
the generated READMEs feature a clean design including key project information
and links to the main sections of the documentation website.
Moreover, they include a set of dynamic badges {cite}`RepositoryBadges`
that provide an up-to-date overview of project specifications, status, and progress.


(overview-vcs)=
## Version Control

|{{ ccc.name }}| fully integrates with Git to automate tasks
like branch and commit management, versioning, tagging, and merging.
Motivated by well-established models such as
[GitLab Flow](https://about.gitlab.com/topics/version-control/what-is-gitlab-flow/),
|{{ ccc.name }}| implements a branching strategy that enables the rapid evolution of software
according to Continuous software engineering best practices {cite}`CICDSystematicReview`,
while ensuring the availability and sustainability of earlier releases.
[|{{ ccc.name }}|'s branching model](#manual-branching)
includes persistent release branches hosting stable versions,
alongside transient branches for simultaneous development and deployment of multiple prereleases.
Moreover, to provide software with a clear and transparent development history
and ensure its long-term findability and accessibility,
all developmental, pre-, and final releases are automatically versioned and tagged.
For this, PyPackIT implements a versioning scheme based on
[Semantic Versioning](#bg-semver) (SemVer),
which clearly communicates changes to the library's public API {cite}`EmpComparisonOfDepIssues, WhatDoPackageDepsTellUsAboutSemVer`.

For [automatic versioning](#manual-versioning),
PyPackIT uses correlated issue ticket data
to determine whether changes correspond to a new major, minor, or patch release.
It then calculates the full version number
by comparing the latest version tags in the development branch
and its target release branch.
Subsequently, for automatic deployment on indexing repositories such as PyPI and Anaconda,
PyPackIT generates a canonical public version identifier
in accordance with the latest [PyPA specifications](#bg-pep440).
This is done by adding additional segments to the SemVer release number
in order to uniquely identify all developmental, pre-, and post-releases.
By incorporating the correlated issue ticket number
as a unique identifier in prerelease versions, PyPackIT enables projects
to simultaneously develop and publish multiple release candidates,
for example to test different approaches for solving the same problem.
Publishing developmental and prereleases allows the community
to thoroughly investigate upcoming changes and provide feedback,
improving software quality and reducing the risk of using
buggy applications in production {cite}`CICDSystematicReview`.


(overview-its)=
## Issue Management

|{{ ccc.name }}| establishes an automated pull-based development workflow
based on a well-tested strategy for FOSS projects {cite}`ConfigManageForLargescaleSciComp`:
New tasks in the project start by submitting a ticket to its ITS,
promoting community collaboration while ensuring thorough documentation of software evolution.
PyPackIT automatically configures and maintains GHI
according to customizable configurations in the control center.
By default, it includes a comprehensive set of issue forms
allowing users to submit type-specific tickets,
such as bug reports and feature requests
for the application or its test suite and documentation.
Designed according to best practices
{cite}`WhatMakesAGoodBugReport, NeedsInBugReports, QualityOfBugReportsInEclipse`,
these forms collect essential type-specific user inputs in a machine-readable format.
They also include selectable options for inputs
such as currently available version numbers and API endpoints,
which are automatically kept up to date by PyPackIT's CCA pipeline.

After an issue is submitted, PyPackIT processes user inputs
to automate the bulk of issue management activities.
It uses a customizable template to generate
a standardized software development [protocol](#manual-protocols) for the issue,
which is attached to the ticket.
By default, this document includes formatted user inputs
under User Requirements Document (URD),
and contains other standard sections like Software Requirements Document (SRD)
and Software Design Document (SDD) for maintainers' inputs.
It also includes dynamic components that are updated by PyPackIT
to reflect current status and progress,
such as a list of completed/remaining tasks,
related pull requests, and activity logs.
To improve ITS organization and searchability,
PyPackIT uses inputs to automatically
[label](#manual-labels) tickets based on issue type, affected versions, API endpoints,
and other configurable options.
Ticket inputs can also be used
to automatically assign specific team members to each ticket,
as defined by the project's [governance model](#manual-governance) in the control center.

After triage, project members can communicate with PyPackIT through issue comments and labels.
For example, by posting a semantic comment under the issue,
members can command PyPackIT to automatically test
a certain version of the software in a specific environment with given test cases.
This greatly accelerates bug triage,
eliminating the need for manual branch creation,
test suite modification, and execution.
If the new test cases fail,
PyPackIT automatically adds them
to the test suite and initiates a bug fix cycle,
streamlining the process of turning bugs into tests
to validate fixes and prevent future recurrences
{cite}`BestPracticesForSciComp, 10SimpleRulesOnWritingCleanAndReliableSciSoft`.
Furthermore, changing the ticket's status label tells PyPackIT to perform additional tasks.
Rejected tickets are automatically closed with updated documentation,
while tickets labeled ready for implementation trigger
the creation of development branches from affected release branches.
These branches are automatically prepared for development
and linked to the issue ticket on GitHub.
For example, a new entry is added to the changelog file,
and the README file is temporarily modified to reflect development on the branch.
Changes are added with a commit message containing issue data,
ensuring a clear and informative history on Git.


(overview-ci)=
## Continuous Integration

When an issue is ready for implementation,
PyPackIT opens a draft PR from each created development branch.
Similar to issue tickets, PRs are also
automatically labeled, assigned, and documented.
If the PR corresponds to a new release,
PyPackIT also creates draft releases
on selected platforms like GitHub Releases and Zenodo.
Contributors can thus immediately start the implementation
in the provided development containers,
requiring only a web browser.
With each commit on a development branch,
PyPackIT runs its CI pipeline
to integrate changes into the codebase
according to best practices
{cite}`CICDSystematicReview, ModelingCI, ContinuousSoftEng`,
while generating comprehensive build artifacts and reports for review.
Similar to other project components,
the CI pipeline is highly customizable
through PyPackIT's control center,
allowing users to modify defaults or add additional tasks.
By default, the pipeline carries out the following tasks:

:**CCA**:
    Dynamic files and content in the branch are synchronized
    with updated control center configurations.
:**Formatting**:
    Changed source files are formatted according to
    Python's official style guide {cite}`PEP8`,
    using [Ruff](https://docs.astral.sh/ruff/) as
    a fast drop-in replacement for the popular
    [Black](https://black.readthedocs.io/) formatter.
:**Code Analysis**:
    Static code analysis and type checking is performed
    to detect code violations, errors, and security issues,
    using well-established linters such as [Ruff](https://docs.astral.sh/ruff/}{Ruff),
    [Mypy](https://mypy.readthedocs.io/), and [CodeQL](https://codeql.github.com/).
:**Data Validation**:
    Data files in JSON, YAML, and TOML formats
    are checked for issues and syntax errors.
:**Refactoring**:
    Available fixes such as end-of-file and end-of-line standardization
    and safe refactoring suggestions by Ruff
    are automatically applied to affected files.
:**Dependency Review**:
    Changed dependencies are analyzed for security and license issues,
    using GitHub's [Dependency-Review Action](https://github.com/actions/dependency-review-action).
:**Build**:
    [Source](https://packaging.python.org/en/latest/specifications/source-distribution-format/)
    ([sdist](https://packaging.python.org/en/latest/glossary/#term-Source-Distribution-or-sdist))
    and [built](https://packaging.python.org/en/latest/specifications/binary-distribution-format/)
    ([wheel](https://packaging.python.org/en/latest/glossary/\#term-Built-Distribution))
    distributions are generated for package and test suite
    according to [PyPA guidelines](https://packaging.python.org/en/latest/tutorials/packaging-projects/#generating-distribution-archives).
    PyPackIT uses PyPA's [Build](https://build.pypa.io/) and [Cibuildwheel](https://cibuildwheel.pypa.io/)
    tools to create platform-independent wheels for pure-Python packages,
    and platform-dependent binaries for packages with extension modules.
    Conda distributions are also generated using the
    [Conda-build](https://docs.conda.io/projects/conda-build/en/stable/) tool.
:**Containerization**:
    A [Jupyter](https://jupyter.org/)-enabled Docker image is created using
    [JupyerHub](https://jupyter.org/hub)'s [Repo2docker](https://github.com/jupyterhub/repo2docker) application,
    with the package, test suite, and all requirements installed.
    In addition to Python and Conda dependencies,
    Debian packages can also be installed from [APT](https://wiki.debian.org/apt-get),
    enabling applications with complex environments to be easily distributed.
:**Testing**:
    Test suite is executed on all supported operating systems and Python versions
    to verify the correctness and compatibility of applied changes.
    This is done for both Python and Conda distributions, as well as the Docker image.
:**Website Build**:
    Documentation website is built with the latest changes and attached to the CI for offline preview.
    If deployment to Read The Docs is enabled, a link for online preview is also added to the PR.
:**Changelog Update**:
    Project's changelog file is updated with data from the corresponding issue, PR, and commits,
    along with identifiers such as DOI, version, commit hash, and date.
    The changelog contains machine-readable data in JSON,
    maintaining a chronological record of the entire project evolution.
    It is used to automatically generate release notes in Markdown format,
    according to a customizable template.
:**Draft Update**:
    All draft releases are updated with the latest configurations,
    documentation, and build artifacts.
    Release-specific metadata such as external contributors and acknowledgments
    can also be added using automated rules or semantic PR comments.
:**Progress Tracking**:
    Dynamic elements in the issue ticket and draft PR are updated to reflect the progress.
    PyPackIT uses commit messages to automatically mark corresponding tasks in the PR as complete. A
    s GHI displays the number of completed and remaining tasks in each issue ticket/PR,
    this provides a clear overview of overall progress in the project.
:**Report**:
    Comprehensive logs and reports are generated for each step,
    improving the visibility of integration status and facilitating reviews.
    These are displayed on GHA's terminal in real-time,
    and rendered as a responsive HTML document for download.


Furthermore, when release-related changes are successfully integrated,
a new developmental release is automatically versioned, tagged,
and published to selected indexing repositories,
e.g., Anaconda, TestPyPI, Zenodo Sandbox, and Docker registries.
This allows the application to be automatically tested in a production-like environment,
ensuring that it works as intended after download and installation on user machines.
It also greatly simplifies the sharing of new developments among collaborators,
enabling feedback and reviews during the implementation phase.
Moreover, the entire development progress leading to each final release
is clearly documented and permanently available {cite}`CICDSystematicReview`.

When all implementation tasks specified in the PR are marked as complete,
PyPackIT automatically initiates the review process by sending review requests
to designated members according to the project's governance model.
The CI pipeline is automatically triggered by changes during the review process as well,
providing team members with detailed status checks, reports, and build artifacts
to keep them informed about the outcomes of revisions.
After the PR is approved by reviewers, PyPackIT automatically merges the changes into production.
By default, this is done by squash merging the development branch
into the (pre)release branch to maintain a clear and linear Git history.
The commit message is automatically generated according to a template,
and can include issue ticket number and other details to establish issue–commit links
and reflect documentation in the VCS.
Moreover, when changes are merged into the main branch,
all project-wide configurations such as repository and workflow settings
are updated according to control center settings.


(overview-cd)=
## Continuous Deployment

PyPackIT's CD pipeline is activated when the merged changes correspond to a new (pre)release.
It generates a public version number to tag the release
and deploy it to user-specified indexing repositories ({numref}`tab-supported-repos`).
By default, the built Docker image is published to GHCR,
providing an isolated environment for running the application on any machine or HPC cluster.
PyPackIT also uses the Docker image to trigger a build on [mybinder.org](https://mybinder.org)—a free
[BinderHub](https://binderhub.readthedocs.io) instance
allowing users to interact with the image from their web browser
using a JupyterLab interface.
The build is cached on mybinder servers,
significantly shortening subsequent loading times.


:::{table} Indexing repositories supported by PyPackIT. Deployment is automated by PyPackIT's CD pipeline, requiring only a one-time setup. This can be done by configuring [Trusted Publishing](https://docs.pypi.org/trusted-publishers/) for the chosen indexing repository or by generating an access token and adding it as a secret to the GitHub repository.
:widths: auto
:name: tab-supported-repos

| Repository                                                                                             | Description                                                                                                                                                                                    | Requirement                   |
|--------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------|
| [PyPI](#bg-pypi)                                                                                       | Python's official software repository used by the [pip](#bg-pip) package manager.                                                                                                              | Trusted Publishing            |
| [Anaconda](#bg-anaconda-org)                                                                           | A popular language-agnostic repository used by the [conda](#bg-conda) package manager.                                                                                                         | Token                         |
| [Zenodo](https://zenodo.org/)                                                                          | A general-purpose repository capable of minting persistent DOIs for immutable depositions.                                                                                                     | Token                         |
| Docker                                                                                                 | Any Docker registry such as [Docker Hub](https://hub.docker.com/) or [GitHub Container Registry](https://github.blog/news-insights/product-news/introducing-github-container-registry/) (GHCR) | Token (not required for GHCR) |
| [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases) | GitHub's general-purpose repository for uploading build artifacts and release notes.                                                                                                           | No requirements               |
| [TestPyPI](https://test.pypi.org/)                                                                     | A separate instance of PyPI for testing purposes.                                                                                                                                              | Trusted Publishing            |
| [Zenodo Sandbox](https://sandbox.zenodo.org/)                                                          | A separate instance of Zenodo for testing purposes.                                                                                                                                            | Token                         |
:::


Further deployment tasks include finalizing and publishing
the draft releases on Zenodo and GitHub Releases,
which can contain any number of user-specified source and build artifacts.
By default, they include all distribution packages, built documentation,
citation and license files, and a `Dockerfile` pointing to the deployed Docker image.
The DOI minted by Zenodo is reserved before the deployment and included in all distributions' metadata.
Each release is therefore permanently available through a unique DOI,
enabling reliable citations.
FAIRness is further improved by uploading source and built distributions to PyPI and Anaconda repositories.
This allows for customized and reproducible builds
while facilitating installation on different platforms and architectures
using Pip and Conda package managers.
All distributions and releases automatically include up-to-date metadata,
documentation, and detailed release notes,
enabling the community to discover the application
based on various keywords, classifiers, and other identifiers.
The updated documentation website is deployed online as well,
with added banners and blog posts to announce the new release.


(overview-cm)=
## Continuous Maintenance, Refactoring, and Testing

In addition to CI/CD pipelines that integrate and deploy new changes,
PyPackIT also periodically runs other Continuous pipelines
to ensure the long-term sustainability of the project and its products.
For example, previous releases are tested with the latest versions
of their dependencies (within the specified range)
to confirm compatibility with up-to-date environments.
The CCA pipeline is also run to update dynamic configurations and content,
such as those inherited from external sources.
Code analysis, refactoring and style formatting tasks are performed as well,
using updated tools and standards to curb the ever-increasing code complexity
and maintain quality and consistency during both development and support phases.
To maintain the health of the development environment,
the repository and its components are frequently cleaned up,
removing outdated artifacts, such as builds, logs, and reports.

During each run, |{{ ccc.name }}| automatically applies updates and fixes to a new branch,
and creates a PR for review by maintainers.
After approval, changes are automatically merged into the project
and applied to all components.
Alternatively, users can opt in for automatic merging without the need for manual approvals.
Similarly, if a problem is found,
a new issue ticket is automatically submitted to the issue tracking system,
notifying project maintainers to take action.
These automated processes significantly simplify
and encourage maintenance activities {cite}`CanAutoPRsEncourageDepUpgrade`,
facilitating the prolonged development and support of software.


(overview-license)=
## Licensing

|{{ ccc.name }}| greatly facilitates project licensing and copyright management
according to best practices for {term}`FOSS`
{cite}`QuickGuideToLicensing, BarelySufficientPracticesInSciComp, ELIXIRSoftwareManagementPlan, SustainableResearchSoftwareHandOver, ShiningLight, 10RuleForSoftwareInCompBio`.
In line with the upcoming [PEP 639](https://peps.python.org/pep-0639/) for improving license clarity,
PyPackIT incorporates the [System Package Data Exchange](https://spdx.org/) (SPDX) license standard.
This allows users to define complex licenses for their projects
using simple [SPDX license expressions](https://spdx.github.io/spdx-spec/v3.0.1/annexes/spdx-license-expressions/).
|{{ ccc.name }}| supports all [SPDX License List](https://spdx.org/licenses/) entries
as well as user-defined licenses.
It can automatically customize licenses with project-specific information and
produce visually appealing Markdown and plain-text outputs
that are valid according to the SPDX License List
[matching guidelines](https://spdx.github.io/spdx-spec/v3.0.1/annexes/license-matching-guidelines-and-templates/).

By default, new projects are licensed under the [`MIT` License](https://spdx.org/licenses/MIT.html)—a
permissive [OSI-approved](https://opensource.org/licenses) and [FSF Free](https://www.gnu.org/licenses/license-list.en.html) license
supporting {term}`FOSS` commercialization {cite}`SettingUpShop`
and fulfilling the Bayh–Dole requirements for patenting publicly funded products {cite}`BayhDole`.
Another recommended option is the GNU Affero General Public License
([`AGPL-3.0-or-later`](https://www.gnu.org/licenses/agpl-3.0)),
which is a strong copyleft license promoting FOSS by enforcing downstream source disclosure.
To change the project license, users only need
to provide the corresponding expression in the control center.
|{{ ccc.name }}| then automatically downloads all required license data and integrates it into the project:

- **Validation**:
  User is notified if the provided license expression is invalid,
  uses deprecated or obsoleted components,
  or has conflicts with project dependencies.
- **Customization**:
  Placeholder values in license contents such as project name, copyright notice,
  and contact information are automatically replaced with project information
  according to control center configurations.
- **Documentation**:
  For each license component, syntactically valid and nicely formatted documents are generated
  and [added to the repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository#applying-a-license-to-a-repository-with-a-license-file)
  according to [GitHub specifications](https://github.blog/changelog/2022-05-26-easily-discover-and-navigate-to-multiple-licenses-in-repositories/),
  so that they are correctly recognized and displayed.
  These are also included in the project's website, along with other license details.
- **Annotation**:
  An SPDX [short-form identifier](https://spdx.dev/learn/handling-license-info/)
  is added as a comment in all source files and as a footer badge in all documentation files,
  clearly communicating license information in a standardized human and machine-readable manner.
  A short copyright notice can also be automatically added to all or certain module docstrings.
- **Distribution**:
  License files are automatically included in all future releases
  and distributed with the package and test suite.
  Platform-specific license metadata and identifiers are also added
  to facilitate license identification by indexing services and package managers.


## Security

To enhance project security while supporting community collaboration,
|{{ ccc.name }}| incorporates several security measures:

- **Protection Rules**:
  By default, release branches and version tags
  require passing status checks and admin approvals before changes can be made,
  ensuring the integrity of the project and its releases.
- **Vulnerability Scanning**:
  Code analysis tools integrated into CI/CD pipelines ensure changes
  do not introduce security vulnerabilities into the codebase.
- **Dependency Monitoring**:
  GitHub's Dependabot and Dependency-Review Action are used to continuously monitor
  project dependencies, alerting maintainers of issues
  and proposing updates.
- **PR Approval**:
  External PRs require project maintainers' approval before CI/CD pipelines can run,
  preventing the execution of untrusted code.
- **Workflow Security**:
  GHA workflows are developed according to best practices
  {cite}`AutoSecurityAssessOfGHAWorkflows, GHADocsSecurity`
  to prevent security issues like command injection,
  token/secret exposure, use of untrusted applications,
  and loose workflow permissions.

Moreover, to ensure that |{{ ccc.name }}| itself is highly secure,
its entire infrastructure is natively implemented and self-contained.
With the exception of well-established [GHA actions](#bg-gha) and Python libraries
from trusted vendors like GitHub and PyPA,
|{{ ccc.name }}| does not rely on other third-party dependencies.
This gives the |{{ ccc.name }}| team full control over the software stack,
allowing us to rapidly respond to issues
and continuously improve the product,
while making |{{ ccc.name }}| fully transparent
and easily auditable by the community.


## Publication

In addition to software engineering,
PyPackIT also facilitates scientific and technical publications.
It enables users to create papers, posters, and presentations
in a variety of formats including LaTeX and Markdown.
For this, PyPackIT provides a dedicated development container
that includes a full installation of [Tex Live](https://tug.org/texlive/)
and [Pandoc](https://pandoc.org), allowing for seamless conversion
and compilation of documents to PDF and other output formats.
The writing experience is enhanced using powerful tools and extensions
like [LaTeX-Workshop](https://github.com/James-Yu/LaTeX-Workshop),
which enable continuous compilation and preview in GitHub Codespaces
and VSCode—similar to online TeX-editing platforms like [Overleaf](https://www.overleaf.com/).
This setup allows research projects to keep their related publications
next to the underlying software under version control,
benefiting from features such as detailed change histories
and comprehensive revisions through commit messages,
issue tickets, and pull request reviews.
Additionally, it supports automation,
for example for generating figures and tables directly from code,
to ensure consistency between the software and its related publications.
