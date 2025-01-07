---
ccid: overview
---

# Overview

This section offers a more detailed overview of
some of PyPackIT's key components, features and capabilities.


## Continuous Configuration Automation

Software projects rely on various tools and services throughout the development life cycle,
each requiring separate configuration via specific files or user interfaces.
This can lead to several maintenance challenges {cite}`BestPracticesForSciComp, DevOpsInSciSysDev`:
Tool-specific formats and requirements result in data redundancy,
since many settings are shared.
As configuration files are often static,
they require manual intervention to reflect each change.
Otherwise they quickly fall out of sync with the current state of the project,
leading to conflicts and inconsistencies.
Moreover, configurations via interactive user interfaces
complicate the tracking and replication of settings,
as they must be manually recorded and applied.

DevOps practices such as Continuous Configuration Automation (CCA)
and Infrastructure-as-Code (IaC) were developed to tackle these issues,
enabling dynamic configuration management of software infrastructure
through machine-readable definition files {cite}`InfrastructureAsCode`.
However, due to a lack of publicly available tools,
most projects still rely on a combination of different configuration files and manual settings,
which are hard to manage, modify, and reproduce.

|{{ ccc.name }}| enables automatic project configuration, customization, and management
by introducing a centralized control mechanism based on CCA and IaC practices.
It provides a [control center](#manual-cc) as the singular user interface
to manage the entire project, and even multiple projects at once.
PyPackIT's control center unifies and structures all project configurations,
metadata, and variables into declarative definitions in [YAML](#yaml)—a
standard human-readable data serialization format.
These are consolidated into one repository location under version control,
allowing for easy tracking of settings throughout the project lifespan,
and eliminating the need for maintaining multiple configuration files in
different formats and locations.
Using APIs and dynamically generated files, PyPackIT automatically applies all 
control center settings to corresponding components,
replacing manual configurations with replicable declarations and
making the entire project highly dynamic and customizable.
To further simplify dynamic project configuration and content management,
the control center is equipped with several key features:

- **Preconfiguration**:
  For all generic configurations,
  default settings are provided based on the latest standards and best practices,
  requiring only project-specific metadata to be declared.
- **Augmentation**:
  Additional data are dynamically generated at runtime
  by analyzing the repository and retrieving information from web APIs
  to minimize manual inputs and updates.
- **Templating**:
  Data reuse is facilitated by templating features that enable
  dynamic referencing of all control center contents throughout project files,
  removing redundancy and allowing for centralized and automatic updates.
- **Inheritance**:
  Data can be dynamically inherited from external sources,
  allowing for consistent creation and centralized maintenance
  of multiple projects with shared settings.
- **Synchronization**:
  Changes to control center contents are automatically propagated
  throughout the project, ensuring consistency across all components
  without the need for manual intervention.
- **Validation**:
  All inputs are validated against detailed predefined schemas
  to ensure correctness and notify users of any errors or inconsistencies
  with comprehensive reports.
- **Customization**:
  Additional configurations can be added either declaratively in YAML files
  or dynamically via Python scripts executed at runtime,
  further facilitating user customization.
- **Caching**:
  To speed up processing and reduce web API usage,
  all retrieved data can be cached both locally and on GHA,
  with user-defined retention times.


## Python Package

PyPackIT provides a comprehensive infrastructure for Python packages,
in line with the latest {term}`PyPA` standards {cite}`PythonPackagingUserGuide`.
For new projects, it provides a build-ready distribution package,
pre-configured according to the latest best practices for scientific Python libraries.
The package skeleton includes all necessary configuration files
like `pyproject.toml`, `MANIFEST.in`, and `requirements.txt`,
along with a top-level \href{https://packaging.python.org/en/latest/glossary/#term-Import-Package}{import package}
filled with essential source files and added functionalities,
e.g., for data file support and command-line interface development.

The package is dynamically maintained via PyPackIT's control center,
enabling facile management and tracking of all settings
throughout the software development process.
Automatically maintained components include:

- **Metadata**:
  Distribution and import names, tagline, description, keywords,
  classifiers, URLs, license, authors, maintainers, and typing information
  are automatically derived from project information and highly customizable.
- **Version**:
  Version information such as version number, commit hash, and release date
  are automatically calculated during each build and injected into package metadata and select source files.
- **Configurations**:
  Build system specifications, Python and OS requirements, dependencies,
  entry points, included data files, and build tool settings
  are specified in the control center and used to dynamically generate configuration files.
- **Source Files**:
  Users can define dynamic docstrings, comments, and code snippets to be automatically inserted
  at certain locations in selected source files.

Therefore, the only task remaining for users is writing application code
in the provided skeleton files, while all integration and deployment tasks
including refactoring, formatting, testing, versioning, packaging, distribution, and indexing
are automatically carried out by PyPackIT's CI/CD pipelines on the cloud.


## Test Suite


Code quality assurance and testing are
crucial aspects of every software development process,
ensuring that the application is functional, correct,
secure, and maintainable {cite}`CompSciError, BestPracticesForSciComp, 5RecommendedPracticesForCompSci, BestPracticesInBioinfSoftware, SurveySEPracticesInScience, ELIXIRSoftwareManagementPlan, DLRSoftEngGuidelines`.
To prevent the accumulation of errors into complex problems,
it is highly recommended to use test-driven development methodologies
{cite}`10SimpleRulesOnWritingCleanAndReliableSciSoft, SciSoftDevIsNotOxymoron, SurveySEPracticesInScience`.
This involves early and frequent unit and regression testing
to validate new code components and ensure existing features
remain functional after changes {cite}`10SimpleRulesOnWritingCleanAndReliableSciSoft, SurveySEPracticesInScience, BarelySufficientPracticesInSciComp, 10SimpleRulesOnWritingCleanAndReliableSciSoft, BestPracticesForSciComp`.
To ensure testing effectiveness, coverage metrics must be frequently monitored to identify
untested components {cite}`DLRSoftEngGuidelines, 10SimpleRulesOnWritingCleanAndReliableSciSoft`.
Users should also be able to run tests locally
to verify software functionality and performance on their machines {cite}`ELIXIRSoftwareManagementPlan, DLRSoftEngGuidelines`,
necessitating the tests to be packaged and distributed along with the software 
{cite}`BarelySufficientPracticesInSciComp, 10MetricsForSciSoftware, BestPracticesInBioinfSoftware`.
Other crucial quality assurance routines include formatting
to improve readability and establish a consistent coding style,
and static code analysis such as linting and type checking
to identify issues undetected by tests,
and refactor code to improve quality, security, and maintainability
{cite}`DLRSoftEngGuidelines, BestPracticesForSciComp, SurveySEPracticesInScience, 10SimpleRulesOnWritingCleanAndReliableSciSoft, NLeScienceSoftDevGuide`.

To ensure effective quality assurance, code analysis and testing practices
need to be automated in the project's development workflow
{cite}`BestPracticesForSciComp, 10MetricsForSciSoftware, 10SimpleRulesOnWritingCleanAndReliableSciSoft`.
This is however a challenging task {cite}`StairwayToHeaven`,
resulting in the prevalence of slow and ineffective testing methods especially in FOSS projects
{cite}`ProblemsOfEndUserDevs, TestingResearchSoftwareSurvey, SoftEngForCompSci, SurveySEPracticesInScience, SurveySEPracticesInScience2`.
Consequently, software products may contain hidden bugs
that do not interrupt the execution of the program
but generate incorrect outputs.
In sensitive areas like governmental and military applications,
such bugs can compromise critical scientific conclusions
and result in multi-million-dollar losses
{cite}`CompSciError, SoftwareChasm, ApproxTowerInCompSci, NightmareRetraction, RetractionChang, RetractionMa, RetractionChang2, RetractionJAmCollCardiol, RetractionMeasuresOfCladeConfidence, RetractionsEffectOfAProgram, CorrectionHypertension, CommentOnError, CommentOnError2, CommentOnError3, CommentOnError4, CommentOnError5, ClusterFailureFMRI`.


:::{admonition} |{{ ccc.name}}|'s Solution
:class: tip

Accordingly, PyPackIT offers a fully automated quality assurance and testing infrastructure
for the entire development life-cycle, fulfilling all requirements, including coverage monitoring,
documentation, and test-suite distribution.
:::


PyPackIT simplifies software testing with a fully automated testing infrastructure
using [PyTest](https://pytest.org/), one of the most popular testing frameworks for Python.
This enables projects to easily perform unit, regression, end-to-end, and functional testing,
which are integrated into PyPackIT's Continuous pipelines and automatically executed
during software integration, deployment, and maintenance.
For each test run, PyPackIT generates comprehensive test results and coverage reports
using plugins such as [PyTest-Cov](https://github.com/pytest-dev/pytest-cov),
and provides them in various machine and human-readable output formats on the repository's GHA dashboard.
After a one-time configuration on [Codecov](https://codecov.io/),
reports are also automatically uploaded to this code coverage analysis platform as well,
which offers features to assess testing effectiveness.
The entire testing infrastructure is preconfigured,
requiring users to only write test cases in a ready-to-use test suite skeleton.
The test suite is included in the project's repository as an individual Python package,
with same features as the project's main package, offering several benefits:

- Dynamic maintenance of configurations and source files are enabled via PyPackIT's control center.
- Test suite is easily installable via Pip,
  eliminating the complexities of setting up a testing environment.
- A built-in command-line interface is included by PyPackIT,
  enabling straightforward execution of the test suite by abstracting the details of running PyTest.
- The test suite is automatically packaged and distributed with each release,
  allowing users to readily test and benchmark the software library on their machine with detailed reports.
- Modularization and reusability of code components are enabled by the package structure,
  simplifying the development of new test cases and improving testing quality.
- Compatibility and size of the software library are improved, as the test suite
  and its dependencies are isolated from the main package.


## Documentation

Documentation is a key factor in software quality and success,
ensuring users understand how to install, use, and exploit the software's capabilities
while recognizing its limitations {cite}`10SimpleRulesForOpenDevOfSciSoft, BestPracticesForSciComp, GoodEnoughPracticesInSciComp, WhatMakesCompSoftSuccessful, SciSoftDevIsNotOxymoron, NamingThePainInDevSciSoft, CompSciError, BarelySufficientPracticesInSciComp`.
This is especially important for {term}`FOSS`,
which often suffers from knowledge loss due to high developer turnover rates {cite}`HowToSupportOpenSource, RecommendOnResearchSoftware, EmpStudyDesignInHPC, SoftwareSustainabilityInstitute`.
As software evolves, documenting and publishing changelogs with each release
allows existing users to assess the update impact and helps new users and contributors 
understand the software's progression {cite}`ELIXIRSoftwareManagementPlan, GoodEnoughPracticesInSciComp, SustainableResearchSoftwareHandOver`.
As community building is crucial for FOSS success {cite}`HowToSupportOpenSource, WhatMakesCompSoftSuccessful`,
project documentation should also include contribution guidelines,
governance models, and codes of conduct {cite}`SurveySEPracticesInScience, BestPracticesForSciComp, BestPracticesInBioinfSoftware, SustainableResearchSoftwareHandOver, 4SimpleRecs, ELIXIRSoftwareManagementPlan, DLRSoftEngGuidelines, NLeScienceSoftDevGuide`.

However, high-quality documentation requires time, effort, and skills,
including web development knowledge to create user-friendly websites
that stay up to date with the latest project developments {cite}`SurveySEPracticesInScience, WhatMakesCompSoftSuccessful`. 
Although tools exist to aid documentation {cite}`TenSimpleRulesForDocumentingSciSoft, WhatMakesCompSoftSuccessful, BestPracticesForSciComp`,
developers must still invest time in setting them up.
Consequently, FOSS is often not well-documented {cite}`SoftEngForCompSci, ProblemsOfEndUserDevs, AnalyzingGitHubRepoOfPapers, DealingWithRiskInSciSoft`,
creating barriers to use and leading to software misuse and faulty results {cite}`HowScientistsReallyUseComputers, HowScientistsDevSciSoftExternalRepl, CompSciError`.


:::{admonition} |{{ ccc.name}}|'s Solution
:class: tip

Therefore, PyPackIT puts great emphasis on documentation,
providing infrastructure and automated solutions that enable projects to maintain
high-quality documentation with minimal effort.
:::

PyPackIT offers an automated solution for generating,
deploying, and maintaining a comprehensive documentation website
according to best practices {cite}`TenSimpleRulesForDocumentingSciSoft, WhatMakesCompSoftSuccessful`,
leaving users with no documentation tasks other than writing docstrings and short software descriptions.
It includes a fully configured [Sphinx](https://www.sphinx-doc.org) website template,
designed using a standardized layout
based on the popular [PyData](https://pydata-sphinx-theme.readthedocs.io/) theme.
All configurations and design elements, including logo, color scheme, font, and icons
are dynamically managed by PyPackIT's control center,
enabling rapid customization and consistent maintenance.
Moreover, [Jinja](https://jinja.palletsprojects.com/) templating is enabled
for all website files and the entire control center content is made available during builds.
This enables the creation of sophisticated content that are dynamically updated
according to control center content.
It also allows PyPackIT to prefill the website with content
that are automatically customized with project-specific information
and complemented with additional data throughout the development process
to reflect the project's progress. These include:

- **Homepage**: Logo, abstract, keywords, and highlights,
  with descriptions of main documentation sections and links to key resources.
- **Project Information**: License, copyright, team members, governance model, and contact information.
- **Package Information**: Python and OS requirements, dependencies, entry points, and version scheme.
- **Installation Guide**: Detailed instructions on how to install the package from various sources.
- **API Reference**: Documentation of all package modules, classes, methods, functions, and attributes,
  automatically generated and continuously updated using docstrings in source code.
- **Changelogs**: Chronological documentation of the development process,
  including important changes such as bug fixes, improvements,
  and modified features, requirements, and dependencies,
  automatically generated by processing issue tickets, PR data, and control center configuration changes.
- **Release Notes**:
  Summaries of each release version, including design documents, implementation details,
  and changelogs, posted on the website's news blog
  along with temporary announcement banners to notify users.
- **Contribution Guide**: Manuals on how to report issues and security vulnerabilities,
  request changes, contribute artifacts, and maintain the software library.
- **Navigation Guide**: Instructions for library users to navigate the website,
  find information, and get support.
- **External Resources**: Links to project codebase, issue tracker, discussion forums,
  and indexing repositories such as PyPI, Zenodo, and conda-forge.

To add further documentation content such as detailed overviews and tutorials,
both plain text and markup languages like
reStructuredText (reST) and [MyST Markdown](https://mystmd.org/)
are supported, providing flexibility in typography.
Moreover, rich features are made available via simple configurations and directives,
using powerful extensions such as:

- [MyST-NB](https://myst-nb.readthedocs.io/en/latest/):
  Elements for writing technical documentation,
  such as executable code blocks, diagrams, charts, figures, tables, and mathematical notation.
- [Sphinx-Design](https://sphinx-design.readthedocs.io/):
  Web components like grids, cards, dropdowns, tabs, admonitions, buttons, and icons,
  for a beautiful and responsive design.
- [ABlog](https://ablog.readthedocs.io/):
  A news blog, with support for RSS web feeds, searching, and categorization.
- [SphinxContrib-BibTeX](https://sphinxcontrib-bibtex.readthedocs.io/):
  Referencing and citation options with support for BibTeX bibliographies.
- [Giscus](https://giscus.app/):
  Comment section for blog entries and other webpages, using GiHub Discussions.
- [SphinxExt-OpenGraph](https://github.com/wpilibsuite/sphinxext-opengraph)
  Adding [Open Graph](https://ogp.me/) metadata in webpages
  for search engine optimization (SEO), rich previews on social media,
  and enhanced project findability and visibility.

Build and deployment of the website are also automated by PyPackIT's CI/CD pipelines.
Changes affecting the website trigger the build process,
providing a preview for review.
Once approved, the updated website is deployed on
[GitHub Pages](https://pages.github.com/), a free static web hosting service,
publicly accessible via a default URL.
To use a custom domain, users only need to provide it in the control center.
Additionally, hosting on the [Read The Docs](https://readthedocs.org/) platform is supported,
requiring only an account configuration.

PyPackIT also generates several GitHub-specific documentation files for the repository.
These are automatically generated according to highly customizable
templates provided in PyPackIT's control center,
and include [community health files](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file#supported-file-types),
for [citation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files),
funding, support, security, contributing, governance, and code of conduct,
as well as a dynamic [README file](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
that presents a concise project overview on GitHub.
Acting as the front page of the repository, the README file
has a visually appealing graphic design,
and contains key project information with links to main sections of the documentation website.
Moreover, it includes a comprehensive collection of dynamic badges
according to best practices {cite}`RepositoryBadges`,
providing users and contributors with an up-to-date overview of project specifications,
status, health, progress, and other statistics.


## Version Control


Version control practices such as branching and tagging
are vital yet challenging tasks in software development {cite}`10MetricsForSciSoftware, ELIXIRSoftwareManagementPlan, EffectOfBranchingStrategies, BranchUseInPractice`.
Branching provides isolation for development and testing of individual changes,
while tags allow to annotate specific states of the code with version numbers
to clearly communicate and reference changes {cite}`ImportanceOfBranchingModels, CICDSystematicReview`.
Although established models like GitFlow and trunk-based development exist {cite}`TrunkBasedDev, GitFlow, GitHubFlow, GitLabFlow`,
they do not fully align with the evolving nature of {term}`FOSS`,
which often begins as a prototype and undergoes significant changes {cite}`UnderstandingHPCCommunity`.
A suitable model must, thus, support simultaneous development and
long-term maintenance of multiple versions, to facilitate rapid evolution
while ensuring the availability and sustainability of earlier releases {cite}`ConfigManageForLargescaleSciComp`. 


PyPackIT fully integrates with Git to automate tasks
like branch and commit management, tagging, and merging.
Motivated by well-established models such as
[Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)
and [GitLab Flow](https://about.gitlab.com/topics/version-control/what-is-gitlab-flow/),
PyPackIT implements a branching strategy that enables the rapid evolution of software
according to Continuous software engineering best practices {cite}`CICDSystematicReview`,
while ensuring the availability and sustainability of earlier releases.
The branching model includes persistent release branches and transient development
and prerelease branches:

- **Main Branch**:
  A special release branch that always contains the latest final release of the library,
  while its control center settings are used as the source of truth
  for all non-version-specific project configurations.
- **Development Branches**:
  Automatically created from target release branches,
  providing an isolated environment to integrate new changes
  before merging back into target branches and deploying to production.
  Each change can be implemented in a separate development branch,
  enabling the simultaneous development of multiple orthogonal features and release candidates.
- **Prerelease Branches**:
  Automatically created from development branches for publishing
  new package versions as a prereleases.
  They facilitate the implementation and documentation of modifications
  during the prerelease period, before the final product is merged into a release branch.
- **Release Branches**:
  Each contain the latest release of an earlier major version of the library.
  They are automatically created from the main branch
  each time a backward-incompatible change is about to be merged.
  This enables proof-of-concept software libraries to rapidly evolve into mature products,
  while all major versions are automatically preserved for long-term maintenance and support.

Moreover, to provide libraries with a clear and transparent development history
and ensure their long-term findability and accessibility,
all releases are automatically versioned and tagged.
For this, PyPackIT implements a version scheme based on
[Semantic Versioning](https://semver.org/) (SemVer),
which clearly communicates changes to the library's
public API {cite}`EmpComparisonOfDepIssues, WhatDoPackageDepsTellUsAboutSemVer`:

- Releases are denoted with a version number `X.Y.Z`, where `X`, `Y`, and `Z`
  are non-negative integers named major, minor, and patch versions, respectively.
- Release version `1.0.0` defines the library's public API.
- In each subsequent release, one of major, minor, or patch versions are incremented by 1
  while the lesser ones are reset to 0,
  depending on the type of most important change in the new public API:
  - **Major**: when backward-incompatible changes are made.
  - **Minor**: when new features are added while no backward-incompatible change is made.
  - **Patch**: when all changes are backward-compatible bug fixes or improvements.

PyPackIT uses correlated issue ticket data to determine whether each release
corresponds to a new major, minor, or patch version.
It then automatically calculates the full version number,
by comparing the latest version tags in the development branch and its target release branch.
Subsequently, for automatic deployment on indexing repositories such as PyPI and TestPyPI,
PyPackIT generates a canonical public version identifier
in accordance with [PyPA specifications](https://packaging.python.org/en/latest/specifications/version-specifiers/):

- Final releases are only denoted with a version number.
- Prerelease versions contain an additional segment,
  denoting the prerelease phase (alpha, beta, or release candidate)
  and the corresponding issue ticket number.
- Developmental releases are versioned by adding an extra segment to the corresponding prerelease version,
  which chronologically numbers each change during the implementation of upcoming package features.

In line with Continuous software engineering best practices {cite}`CICDSystematicReview`,
publishing developmental and prereleases allows the community to thoroughly investigate
upcoming changes and provide feedback, improving the quality of libraries
and reducing the risk of using buggy software in production.
By incorporating the issue ticket number as a unique identifier for these releases,
PyPackIT enables libraries to simultaneously develop
and publish multiple release candidates.
This facilitates frequent experimentation and modifications even within each iteration,
which are crucial for open-source software development
due to its uncertain and evolving nature {cite}`SurveySEPracticesInScience`.


## Issue Management

PyPackIT establishes a pull-based development workflow,
in which new tasks in the project start by submitting an issue ticket to its ITS,
enabling the community to readily propose changes and ensuring that the entire evolution
of the software library is properly documented
in a traceable and transparent way.
To facilitate this, PyPackIT automatically configures and maintains the repository's GHI,
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


Furthermore, PyPackIT automates the bulk of management activities throughout the workflow.
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
  with a timeline that is automatically updated by PyPackIT with important milestones
  to reflect the progress.

Therefore, after ticket submission, notified maintainers only need to triage the issue,
which is also facilitated by PyPackIT.
For example, by posting a comment under an issue,
project maintainers can command PyPackIT to automatically test
a specific version of the library in a specific environment with given test cases.
This greatly accelerates bug report triage,
eliminating the need for manual branch creation and test suite modification and execution.
If the new test cases fail, PyPackIT automatically adds them to the project's test suite
and initiates a bug fix task, thus providing a streamlined solution
for continuously turning bugs into new test cases,
to validate the fix and prevent future recurrences
according to best practices {cite}`BestPracticesForSciComp, 10SimpleRulesOnWritingCleanAndReliableSciSoft`.

After triage, maintainers can command PyPackIT to perform various tasks
by changing the ticket's status label.
For example, rejected tickets are automatically closed
and the documentation is updated to specify the reason and details.
On the other hand, when a ticket is labeled ready for implementation,
PyPackIT creates a new development branch from each affected release branch,
as specified in ticket data.
These development branches are then automatically linked to the issue ticket on GitHub.
Additionally, an empty commit is added to them containing issue data in the commit message,
maintaining a clear and information-rich history on Git.


## Continuous Integration

When an issue is ready for implementation, PyPackIT automatically opens a draft PR
for each created development branch,
filled with information from the corresponding issue data,
and labeled accordingly.
Developers can thus immediately start implementing the specified changes.
With each commit on a development branch,
PyPackIT runs a CI pipeline to integrate the new changes into the code base
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
PyPackIT automatically initiates the process to merge the changes into production:

- Reviewers are automatically designated to the PR
  according to rules defined in the control center
  based on several different factors, such as changed files or issue type.
- The status and outputs of CI pipelines are displayed in the PR,
  and automatically updated after each revision during the review process.

When the PR is approved by reviewers, PyPackIT automatically performs the merging:

- Changelogs are updated using
  issue ticket and PR data, maintaining chronological records
  of all key aspects of the development process for both users and developers of the library.
  PyPackIT automatically correlates each implementation task with a specific changelog section
  based on [Conventional Commits](https://www.conventionalcommits.org) types defined in the control center.
  For example, tasks marked as `fix` are added to `Bug Fixes` section of the user changelog for library's public API.
- A consistent and clear Git history is maintained by squash merging the development branch
  into the corresponding release branch.
  To establish issue–commit links and reflect the development documentation in the project's VCS,
  the commit message contains the issue ticket number and other details such as type, scope, and description.
- When changes are merged into the repository's main branch,
  all project-wide configurations such as repository and workflow settings
  are updated according to control center content.


## Continuous Deployment

If the merged changes correspond to a new release or pre-release of the library,
the CD pipeline carries out additional deployment tasks:

- [Source distributions](https://packaging.python.org/en/latest/glossary/#term-Source-Distribution-or-sdist)
  (sdists) is generated, allowing for customized installations and reproducible builds according to
  [PyPA guidelines](https://packaging.python.org/en/latest/tutorials/packaging-projects/#generating-distribution-archives).
- [Built distributions](https://packaging.python.org/en/latest/glossary/#term-Built-Distribution)
  ([wheels](https://packaging.python.org/en/latest/glossary/#term-Wheel) are included as well,
  facilitating installation on different platforms.
  PyPackIT uses PyPA's [Build](https://build.pypa.io/) and [Cibuildwheel](https://cibuildwheel.pypa.io/)
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


## Continuous Maintenance, Refactoring, and Testing

Modern software can remain useful and operational
for decades {cite}`SoftwareSustainabilityInstitute, SoftEngForCompSci`.
Considering the amounts of time and effort required
to develop high-quality software from scratch,
ensuring the long-term sustainability of available software
is crucial {cite}`BarelySufficientPracticesInSciComp`.
This requires continuous feedback from the community and active maintenance
to fix existing issues, improve functionalities, and add new features.
Maintaining software dependencies is equally important {cite}`FortyYearsOfSoftwareReuse`,
as software must remain compatible with diverse computer environments
and future dependency versions {cite}`EmpComparisonOfDepNetEvolution`.
However, many projects overlook outdated dependencies {cite}`DoDevsUpdateDeps`,
leading to incompatibilities and bugs {cite}`MeasuringDepFreshness, ThouShaltNotDepend, OnImpactOfSecVulnInDepNet`.

Open-source software development challenges such as funding {cite}`ManagingChaos, BetterSoftwareBetterResearch`,
small team sizes {cite}`SoftEngForCompSci, HowScientistsReallyUseComputers`,
and high developer turnover rates {cite}`RecommendOnResearchSoftware, EmpStudyDesignInHPC`
further hinder maintenance, exacerbated by technical debt and increased software entropy
from neglected software engineering best practices {cite}`BetterSoftwareBetterResearch, ProblemsOfEndUserDevs, SoftEngForCompSci, ManagingTechnicalDebt, 10SimpleRulesForOpenDevOfSciSoft, SoftDesignForEmpoweringSci, ManagingChaos, SoftwareSustainabilityInstitute`.
Consequently, the extra effort required for maintenance is a major barrier
to publicly releasing software {cite}`BetterSoftwareBetterResearch, PublishYourCode`,
often leaving it as an unsustainable prototype {cite}`SustainableResearchSoftwareHandOver, 10RuleForSoftwareInCompBio, PublishYourCode`.
To prevent such issues, quality assurance and maintenance tasks should be automated
and enforced from the beginning of the project {cite}`SoftEngForCompSci`.


:::{admonition} |{{ ccc.name}}|'s Solution
:class: tip

|{{ ccc.name }}| achieves this by several mechanisms, including its automated pull-based development model
that promotes collaboration and feedback, CI/CD pipelines that enforce software engineering best practices
throughout the development process, and Continuous Maintenance (CM) {cite}`ContinuousMaintenance`,
Refactoring (CR) {cite}`ContRefact`, and Testing (CT) {cite}`ContinuousSoftEng`
pipelines (abbreviated as CM/CR/CT) that periodically perform various automated tasks,
such as updating dependencies and development tools,
to maintain the health of the software and its development environment.
:::


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

During each run, PyPackIT automatically applies updates and fixes to a new branch,
and creates a PR for review by maintainers.
After approval, changes are automatically merged into the project
and applied to all components. Similarly, if a problem is found,
a new issue ticket is automatically submitted to the issue tracking system,
notifying project maintainers to take action.
These automated processes significantly simplify
and encourage maintenance activities {cite}`CanAutoPRsEncourageDepUpgrade`,
facilitating the prolonged development and support of software.


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
PyPackIT incorporates several security measures:

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
With the exception of a handful of fundamental {term}`Actions` and Python libraries
from trusted vendors like GitHub and PyPA,
PyPackIT does not rely on other third-party dependencies.
This gives the |{{ ccc.name }}| team full control over the software stack,
allowing us to rapidly respond to issues
and continuously improve the product,
while making |{{ ccc.name }}| fully transparent and easily auditable by the community.
