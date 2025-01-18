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
   such as PyPI, Anaconda, Zenodo, and various Docker registries and BinderHub instances.


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
in line with the latest {term}`PyPA` standards {cite}`PythonPackagingUserGuide`.
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

Furthermore, PyPackIT can dynamically generate Markdown documents in various flavors, 
from declarative instructions in the control center. 
This is mainly used to add platform-specific 
[community health files](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file#supported-file-types) 
and [README file](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
for GitHub and other indexing repositories like PyPI. 
The READMEs serve as the front page of the repositories, 
featuring a clean design with key project information 
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

|{{ ccc.name }}| establishes an automated pull-based development workflow,
in which new tasks in the project start by submitting an issue ticket to its ITS,
enabling the community to readily propose changes and ensuring that the entire evolution
of the software library is properly documented
in a traceable and transparent way.
To facilitate this, |{{ ccc.name }}| automatically configures and maintains the repository's GHI,
according to customizable configurations in the control center.
For example:

- Submission options are provided for different issue types,
  such as requesting bug fixes, new features, and other changes in various project components,
  including the library, test suite, documentation website, and control center settings.
- Specialized submission forms are supplied for each issue type
  according to best practices {cite}`WhatMakesAGoodBugReport, NeedsInBugReports, QualityOfBugReportsInEclipse`,
  offering relevant instructions to users and
  collecting type-specific information via machine-readable input types.
- Dynamic input options in submission forms are automatically updated,
  eliminating the need for frequent manual maintenance.
  These include lists of supported releases, operating systems, and Python versions,
  which let users easily specify issue details from dropdown menus.
- Labels are automatically created and updated,
  providing useful categorization options for issues and PRs.


Furthermore, |{{ ccc.name }}| automates the bulk of management activities throughout the workflow.
After an issue is submitted, it processes ticket inputs
to perform several tasks, including:

- **Formatting**:
  User inputs are formatted to provide a consistent and concise overview for each ticket.
- **Labeling**:
  Tickets are labeled based on issue type, user inputs, and current stage
  to facilitate the organization and findability of the project's ongoing and finished tasks.
- **Assignment**:
  Tasks are assigned to maintainers according to a declarative project governance model
  in the control center, which defines member roles and privileges.
- **Documentation**:
  A standardized form is attached to tickets to facilitate the documentation
  and tracking of the development process.
  The form contains a structured template for documenting software requirements specification,
  design description, implementation plans, and other development details,
  with a timeline that is automatically updated by |{{ ccc.name }}| with important milestones
  to reflect the progress.

Therefore, after ticket submission, notified maintainers only need to triage the issue,
which is also facilitated by |{{ ccc.name }}|.
For example, by posting a comment under an issue,
project maintainers can command |{{ ccc.name }}| to automatically test
a specific version of the library in a specific environment with given test cases.
This greatly accelerates bug report triage,
eliminating the need for manual branch creation and test suite modification and execution.
If the new test cases fail, |{{ ccc.name }}| automatically adds them to the project's test suite
and initiates a bug fix task, thus providing a streamlined solution
for continuously turning bugs into new test cases,
to validate the fix and prevent future recurrences
according to best practices {cite}`BestPracticesForSciComp, 10SimpleRulesOnWritingCleanAndReliableSciSoft`.

After triage, maintainers can command |{{ ccc.name }}| to perform various tasks
by changing the ticket's status label.
For example, rejected tickets are automatically closed
and the documentation is updated to specify the reason and details.
On the other hand, when a ticket is labeled ready for implementation,
|{{ ccc.name }}| creates a new development branch from each affected release branch,
as specified in ticket data.
These development branches are then automatically linked to the issue ticket on GitHub.
Additionally, an empty commit is added to them containing issue data in the commit message,
maintaining a clear and information-rich history on Git.


(overview-ci)=
## Continuous Integration

When an issue is ready for implementation, |{{ ccc.name }}| automatically opens a draft PR
for each created development branch,
filled with information from the corresponding issue data,
and labeled accordingly.
Developers can thus immediately start implementing the specified changes.
With each commit on a development branch,
|{{ ccc.name }}| runs a CI pipeline to integrate the new changes into the code base
according to best practices {cite}`CICDSystematicReview, ModelingCI, ContinuousSoftEng`:

- **Configuration Synchronization**:
  Modifications in control center settings are applied to dynamic files in the branch.
- **Code Formatting**:
  [Black](https://black.readthedocs.io/) code style is applied to changed source files.
- **Code Analysis**:
  Static code analysis and type checking is performed
  using well-established linters such as [Ruff](https://docs.astral.sh/ruff/}{Ruff),
  [Mypy](https://mypy.readthedocs.io/), and [CodeQL](https://codeql.github.com/)
  to detect potential errors, code violations, security issues, and other code smells
  in both Python and supported data file.
- **Data File Analysis**:
  Data files in JSON, YAML, and TOML formats
  are checked for syntax errors.
- **Refactoring**:
  Available fixes such as end-of-file and end-of-line standardization
  and safe refactoring suggestions by Ruff are automatically applied.
- **Dependency Review**:
  Changed dependencies are analyzed for security and license issues,
  using GitHub's [Dependency-Review Action](https://github.com/actions/dependency-review-action).
- **Build**: Source and binary distributions are built and attached when package files are modified.
- **Testing**: Test suite is executed on a matrix of supported operating systems and Python versions
  to verify the correctness and compatibility of changes applied to source files.
- **Website Build**: Documentation website is built and attached to the CI
  to reflect the latest changes in package and website source files and configurations.
- **Report**:
  Comprehensive reports are generated for each step to
  improve the visibility of integration status and facilitate reviews.
- **Progress Tracking**
  The draft PR is updated to reflect the progress,
  automatically marking tasks as complete based on commit messages and CI outputs.

When package-related changes are successfully integrated,
a new developmental release is automatically versioned, tagged, and published to TestPyPI.
This serves several purposes {cite}`CICDSystematicReview`:

- The library is automatically tested in a production-like environment,
  ensuring that it works as intended after download and installation on user machines.
- New features and developments can be easily shared with other collaborators,
  enabling early feedback and reviews during the implementation phase.
- The entire development progress leading to each final release
  is permanently documented in a clear and transparent manner.

When all implementation tasks specified in a PR are marked as complete,
|{{ ccc.name }}| automatically initiates the process to merge the changes into production:

- Reviewers are automatically designated to the PR
  according to rules defined in the control center
  based on several different factors, such as changed files or issue type.
- The status and outputs of CI pipelines are displayed in the PR,
  and automatically updated after each revision during the review process.

When the PR is approved by reviewers, |{{ ccc.name }}| automatically performs the merging:

- Changelogs are updated using
  issue ticket and PR data, maintaining chronological records
  of all key aspects of the development process for both users and developers of the library.
  |{{ ccc.name }}| automatically correlates each implementation task with a specific changelog section
  based on [Conventional Commits](https://www.conventionalcommits.org) types defined in the control center.
  For example, tasks marked as `fix` are added to `Bug Fixes` section of the user changelog for library's public API.
- A consistent and clear Git history is maintained by squash merging the development branch
  into the corresponding release branch.
  To establish issue–commit links and reflect the development documentation in the project's VCS,
  the commit message contains the issue ticket number and other details such as type, scope, and description.
- When changes are merged into the repository's main branch,
  all project-wide configurations such as repository and workflow settings
  are updated according to control center content.


(overview-cd)=
## Continuous Deployment

If the merged changes correspond to a new release or pre-release of the library,
the CD pipeline carries out additional deployment tasks:

- [Source distributions](https://packaging.python.org/en/latest/glossary/#term-Source-Distribution-or-sdist)
  (sdists) is generated, allowing for customized installations and reproducible builds according to
  [PyPA guidelines](https://packaging.python.org/en/latest/tutorials/packaging-projects/#generating-distribution-archives).
- [Built distributions](https://packaging.python.org/en/latest/glossary/#term-Built-Distribution)
  ([wheels](https://packaging.python.org/en/latest/glossary/#term-Wheel) are included as well,
  facilitating installation on different platforms.
  |{{ ccc.name }}| uses PyPA's [Build](https://build.pypa.io/) and [Cibuildwheel](https://cibuildwheel.pypa.io/)
  tools to automatically create platform-independent wheels for pure-Python packages,
  and platform-dependent binaries for packages with extension modules
  written in compiled languages like C and C++.
  This is crucial for many libraries that rely on extension modules for compute-heavy calculations.
- Documentation website is updated and deployed online.
  A banner is added to announce the new release, and a blog post is created with release notes.
- Distribution packages are versioned, tagged, and published on GitHub,
  along with the test suite, documentation website, and detailed release notes.
- Package is also deployed to [Python Package Index](https://pypi.org/) (PyPI),
  Pythons's official software repository.
  This makes the library easily installable with [Pip](https://pip.pypa.io/),
  Python's official package manager.
  Moreover, it enables the community to discover the library based on its keywords, classifiers,
  and other attributes, while an automatically generated [PyPI-friendly README file](ttps://packaging.python.org/en/latest/guides/making-a-pypi-friendly-readme/)
  provides a complete project overview.
  The deployment is automated using [trusted publishing](https://docs.pypi.org/trusted-publishers/) with
  [PyPA's official GHA application](https://github.com/pypa/gh-action-pypi-publish),
  which only requires a one-time account configuration on PyPI.
- Following a one-time account configuration on [Zenodo](https://zenodo.org/)—an open-access
  repository for research outputs, the release will also be permanently available and uniquely indexed
  with a DOI, facilitating reproducibility and citations.


(overview-cm)=
## Continuous Maintenance, Refactoring, and Testing

To ensure long-term software sustainability,
|{{ ccc.name }}| periodically runs Continuous pipelines on a scheduled basis
to check for problems and perform automatic fixes and updates.
In addition to CCA mentioned above, tasks include:

- **CT**: To ensure compatibility with up-to-date environments,
  previous releases are periodically tested with the latest available dependencies,
  including new Python versions, according to the project's version specifiers.
- **CR**: Code analysis and formatting tasks are performed using updated tools
  and standards to curb the ever-increasing code complexity
  and maintain quality and consistency during both development and support phases.
- **CM**: To maintain the health of the development environment,
  the repository and its components are frequently cleaned up,
  removing outdated development artifacts, such as builds, logs, and reports.

During each run, |{{ ccc.name }}| automatically applies updates and fixes to a new branch,
and creates a PR for review by maintainers.
After approval, changes are automatically merged into the project
and applied to all components. Similarly, if a problem is found,
a new issue ticket is automatically submitted to the issue tracking system,
notifying project maintainers to take action.
These automated processes significantly simplify
and encourage maintenance activities {cite}`CanAutoPRsEncourageDepUpgrade`,
facilitating the prolonged development and support of software.


(overview-license)=
## Licensing

|{{ ccc.name }}| greatly facilitates project licensing and copyright management,
in accordance with best practices for {term}`FOSS`
{cite}`QuickGuideToLicensing, BarelySufficientPracticesInSciComp, ELIXIRSoftwareManagementPlan, SustainableResearchSoftwareHandOver, ShiningLight, 10RuleForSoftwareInCompBio`
and the upcoming [PEP 639](https://peps.python.org/pep-0639/),
by integrating with the System Package Data Exchange ([SPDX](https://spdx.org/)) license standard.
This allows users to define complex licenses for their projects
using a simple [SPDX license expression](https://spdx.github.io/spdx-spec/v3.0.1/annexes/spdx-license-expressions/).
|{{ ccc.name }}| supports all [SPDX License List](https://spdx.org/licenses/) entries
as well as user-defined licenses.
It can automatically customize licenses with project-specific information and
produce visually appealing Markdown and plain-text outputs
that are valid according to the SPDX License List
[matching guidelines](https://spdx.github.io/spdx-spec/v3.0.1/annexes/license-matching-guidelines-and-templates/).

By default, new projects are licensed under the [`MIT` License](https://spdx.org/licenses/MIT.html),
which is a permissive [OSI-approved](https://opensource.org/licenses) and
[FSF Free](https://www.gnu.org/licenses/license-list.en.html) license
that supports {term}`FOSS` commercialization {cite}`SettingUpShop`
and fulfils the Bayh–Dole requirements for patenting publicly funded products {cite}`BayhDole`.
Another recommended option is the GNU Affero General Public License
([`AGPL-3.0-or-later`](https://www.gnu.org/licenses/agpl-3.0)),
which is a strong copyleft license promoting FOSS by enforcing downstream source disclosure.
To change the project license, users only need to provide the corresponding expression
in the control center (e.g., `MIT OR (AGPL-3.0-or-later WITH GPL-3.0-linking-exception)`);
|{{ ccc.name }}| will then automatically download the required license data and integrate it into the project:

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
  and added to the repository according to
  [GitHub specifications](https://github.blog/changelog/2022-05-26-easily-discover-and-navigate-to-multiple-licenses-in-repositories/),
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
  By default, protection rules are applied to repository branches and tags,
  requiring passing status checks and admin approvals before changes can be made
  to important repository references (cf. [Manual](#branch-protection-rules)).
  This prevents accidental or unauthorized changes to resources
  that may compromise the integrity of the development environment
  or the software itself.
- **Security Vulnerability Scanning**:
  Several code analysis tools are integrated into CI/CD pipelines
  to ensure that changes do not introduce
  security vulnerabilities into the codebase.
- **Dependency Monitoring**:
  GitHub's Dependabot and Dependency-Review Action are used to continuously monitor
  project dependencies, to alert maintainers of any issues
  and propose updates when possible.
- **PR Approval**:
  External PRs require project maintainers' approval before CI/CD pipelines can run,
  to prevent malicious code from being executed.
- **Workflow Security**:
  GHA workflows are developed according to best practices
  {cite}`AutoSecurityAssessOfGHAWorkflows, GHADocsSecurity`
  to prevent security issues that may arise through command injection,
  use of untrusted applications, exposure of tokens and secrets,
  and loose workflow permissions, among others.

Moreover, to ensure that |{{ ccc.name }}| itself is highly secure,
its entire infrastructure is natively implemented and self-contained.
With the exception of a handful of fundamental [GHA actions](#bg-gha) and Python libraries
from trusted vendors like GitHub and PyPA,
|{{ ccc.name }}| does not rely on other third-party dependencies.
This gives the |{{ ccc.name }}| team full control over the software stack,
allowing us to rapidly respond to issues
and continuously improve the product,
while making |{{ ccc.name }}| fully transparent and easily auditable by the community.
