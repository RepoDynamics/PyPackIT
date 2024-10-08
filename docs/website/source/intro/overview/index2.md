# Overview







The rest of this section offers a more detailed overview of some of PyPackIT's key components, features and capabilities.

## Control Center

Inspired by DevOps practices like IaC, PyPackIT introduces a centralized control mechanism; 
a singular interface to facilitate the management, maintenance, 
and customization of individual and collective research software projects:

- All project configurations and metadata are consolidated into one repository location 
  under version control, allowing for easy tracking of settings throughout the project's lifespan.
- Settings are unified and structured in \href{https://yaml.org/}{YAML} format—a standard, 
  concise, human-readable data serialization language, 
  eliminating the need to manage multiple formats and locations.
- Manual settings are replaced by declarative configuration definitions, 
  improving transparency and replicability of project configurations.
- Data are made accessible to the Python package, test suite, documentation website, 
  and other project tools and files, enabling dynamic content and configurations.
- Modifications are automatically applied to all project components 
  via APIs and dynamically maintained configuration files, 
  enhancing customizability and simplifying maintenance.
- Data reuse is facilitated by templating features that enable 
  dynamic referencing across settings, removing redundancy and streamlining modifications.
- Dynamic configuration management is enabled via inheritance 
  from other GitHub repositories, aiding in consistent creation and maintenance 
  of multiple software projects with shared settings.
- Additional information are automatically retrieved and cached 
  from various web-APIs to minimize manual data inputs and updates. 
  These include details on GitHub users involved in the project.
- CCA is enabled, periodically syncing dynamic settings including those inherited 
  from specified GitHub repositories or retrieved from web-APIs.
- Custom data can be added either declaratively in YAML files 
  or dynamically via Python scripts executed at runtime, further facilitating user customization.

For all generic configurations, PyPackIT provides defaults 
based on latest guidelines and best practices for research software. 
Thus, most projects need only to declare project-specific metadata, 
while extensive customization is readily available for particular needs. 
Control center options include:
- Project descriptors (name, keywords, tagline, summary) 
  and metadata (license, copyright, authors, funding options)
- Workflow configurations (Continuous pipelines, issue management, 
  version control, governance model, documentation, security)
- Package and test-suite settings (build configurations, dependency declarations, 
  entry-point definitions, metadata for software indexing repositories)
- Configurations for tools used in the development workflow 
  (testing frameworks, code analyzers, code formatters)
- Contents and settings for communication channels 
  (documentation website, repository README files, discussion forums, 
  citation file, community health files like contribution guidelines and code of conduct)
- Settings are incorporated into various project components, 
  facilitating centralized configuration. 
  For example, project descriptors and metadata are used in package and test-suite metadata, 
  documentation website, GitHub repository's settings, license files, and community health files.



${{ name }} provides a centralized control center for your repository,
where all available settings for ${{ name }} are gathered in one place
along with all information, configurations, and metadata of your project,
and thoughtfully organized and presented in a clear, consistent, and concise format,
mainly through the use of YAML files.
Whenever you commit changes to the control center files, they are automatically
applied to your repository, Python package,
test suite, documentation website, and all other tools and external services.
Therefore, instead of having to deal with multiple interfaces and diverse configuration
and metadata files scattered across your repository and each with its own format and syntax,
you can simply manage your entire project from within the control center,
using a single, unified, and consistent interface;
${{ name }} automatically translates your changes into the appropriate formats,
generates all necessary files in the required locations, and updates them dynamically.

The control center contains all key information and metadata of your project,
such as its name, description, keywords, license and copyright information,
authors/maintainers and their roles, contact information, citations,
and branding and styling information, to name a few.
On top of these, ${{ name }} automatically augments your project's metadata
with various dynamic information, so that you don't have to manually define and update them.
For example, all information on your GitHub repository, along with full details of
the project's owner, authors, maintainers, and contributors, are periodically retrieved
from GitHub, and a full list of your package's active releases and their corresponding
information are generated and maintained automatically.

Furthermore, the control center contains all configurations and metadata for your
GitHub/Git repository (e.g. general settings; branch protection rules; security configurations;
GitHub Pages settings; templates for issues, pull requests, and discussions; funding options;
health files contents; README files contents; description and topics; gitignore and gitattributes files),
Python package and test suite (e.g. build configurations; package metadata; dependencies
and other requirements; entry points and scripts declarations; manifest file content;
docstrings; PyPI and Conda settings),
documentation website (e.g. menu, navigation bar, and quicklinks items; theme and styling settings;
custom domain declaration; web analytics settings, announcement configurations),
and all other tools and external services that are utilized by your project
(e.g. settings for various linting, formatting, and testing tools such as
Ruff, Mypy, Pylint, Bandit, Isort, Black, Pytest, Pytest-cov, etc.;
pre-commit hooks configurations; settings for external platforms such as Codecov and ReadTheDocs).

In addition, to eliminate any redundancy and provide your project with a high degree of flexibility
and customization, ${{ name }} allows for complex and recursive templating within all contents of
the control center, meaning that you can reference and reuse any piece of configuration or data
in all other parts of the control center.
You can also command ${{ name }} to dynamically inherit any piece of configuration or data
from any other GitHub repository, allowing you to easily share and reuse specifications
across multiple projects.

## Python Package

PyPackIT provides a comprehensive infrastructure for Python packages, in line with the latest standards according to the \href{https://www.pypa.io/}{Python Packaging Authority} (PyPA) \cite{PythonPackagingUserGuide}. It includes a top-level \href{https://packaging.python.org/en/latest/glossary/#term-Import-Package}{import package} with pre-configured source files and configuration files required for build and deployment:

`__init__.py`: Initialization file necessary for Python to recognize the package, 
containing the package docstring and version information.
`__main__.py`: Module file pre-equipped with features to enable rapid development 
of a command-line interface for the library.
`pyproject.toml`: Main package configuration file, 
declaring build specifications, dependencies, 
entry points, metadata, and various tool settings.
`MANIFEST.in`: Definition file for including non-source files 
in the distribution package, such as license and data files.
`requirements.txt`: Dependency specification file required by various tools and services, 
such as automatic dependency updates and vulnerability alerts.

The package skeleton is dynamically maintained via PyPackIT's control center, 
enabling the facile management and tracking of package configuration and metadata 
throughout the software development process. 
Automatically updated elements include: 

- Configuration files such as \verb|pyproject.toml|, \verb|MANIFEST.in|, and \verb|requirements.txt|.
- Version information, which is automatically calculated during each build, and injected into package metadata and source files.
- Package docstring in the \verb|__init__.py| file, which includes the project's name, description, and copyright notice by default.
- Name and location of the top-level import package.

All generic settings, such as build system specifications and tool settings, 
are pre-configured according to latest best practices for scientific Python libraries, 
while \href{https://packaging.python.org/en/latest/specifications/pyproject-toml/#declaring-project-metadata-the-project-table}{package metadata}, 
such as authors, descriptions, license, classifiers, and project URLs, 
are automatically generated from project information. 
Therefore, the only remaining task for users is writing scientific code 
in the provided skeleton files, while packaging, distribution, 
and indexing tasks are automatically carried out by PyPackIT's CI/CD pipelines on the cloud. 
For example:

- \href{https://packaging.python.org/en/latest/glossary/#term-Source-Distribution-or-sdist}{Source distributions}
  (sdists) are generated for each release, 
  allowing for customized installations and reproducible builds according to 
  \href{https://packaging.python.org/en/latest/tutorials/packaging-projects/#generating-distribution-archives}{PyPA guidelines}.
- \href{https://packaging.python.org/en/latest/glossary/#term-Built-Distribution}{Built distributions}
  (\href{https://packaging.python.org/en/latest/glossary/#term-Wheel}{wheels}) are included as well, 
  facilitating installation on different platforms. 
  PyPackIT uses PyPA's \href{https://build.pypa.io/}{Build} and \href{https://cibuildwheel.pypa.io/}{Cibuildwheel} 
  tools to automatically create platform-independent wheels for pure-Python packages, 
  and platform-dependent binaries for packages with extension modules written in compiled languages like C and C++. 
  This is crucial for many scientific libraries that rely on extension modules 
  for compute-heavy calculations.
- Distribution packages are deployed to \href{https://pypi.org/}{Python Package Index} (PyPI), 
  Pythons's official software repository. 
  This makes the scientific library easily installable with \href{https://pip.pypa.io/}{Pip}, 
  Python's official package manager. 
  Moreover, it enables the community to discover the library based on its keywords, classifiers, 
  and other attributes, while an automatically generated \href{https://packaging.python.org/en/latest/guides/making-a-pypi-friendly-readme/}{PyPI-friendly README file} 
  provides a complete project overview. 
  The deployment is automated using \href{https://docs.pypi.org/trusted-publishers/}{trusted publishing} with 
  \href{https://github.com/pypa/gh-action-pypi-publish}{PyPA's official GHA application}, 
  which only requires a one-time account configuration on PyPI.
- Each release is published on GitHub, containing distribution packages, full source code, 
  test suite, and documentation. 
  Following a one-time account configuration on \href{https://zenodo.org/}{Zenodo}—an open-access 
  repository for research outputs, these releases will be permanently available and uniquely indexed 
  with a DOI, facilitating reproducibility and citations.

## Test Suite

PyPackIT facilitates software testing by offering a fully automated testing infrastructure 
based on \href{https://pytest.org/}{Pytest}, one of the most popular testing frameworks for Python. 
It allows projects to easily perform unit, regression, end-to-end, and functional testing. 
These are integrated into PyPackIT's Continuous pipelines and automatically executed 
during software integration, deployment, and maintenance. 
For each execution, PyPackIT generates comprehensive tests results and coverage reports 
using plugins such as \href{https://github.com/pytest-dev/pytest-cov}{Pytest-cov}, 
and provides them in various machine and human-readable output formats on the repository's GHA dashboard.
After a one-time configuration on \href{https://codecov.io/}{Codecov}, 
the reports will automatically be uploaded to this code coverage analysis platform as well, 
which offers features to assess testing effectiveness. 
The entire testing infrastructure is pre-configured, 
requiring users to only write test cases in a ready-to-use test suite skeleton. 
This is included in the project's repository as an individual Python package, 
with same features as the project's main package, offering several benefits:

- Dynamic maintenance of configurations and source files are enabled via PyPackIT's control center.
- The test suite is easily installable via Pip, 
  eliminating the complexities of setting up a testing environment.
- A built-in command-line interface is included by PyPackIT, 
  enabling straightforward execution of the test suite by abstracting the details of running Pytest.
- The test suite is automatically packaged and distributed with each release, 
  allowing users to readily test and benchmark the software library on their machine, by following the instructions provided by PyPackIT.
- Modularization and reusability of code components are enabled by the package structure, 
  simplifying the development of new test cases and improving testing quality.
- Compatibility and size of the software library are improved, as the test suite 
  and its dependencies are isolated from the main package.

## Documentation

PyPackIT offers an automated solution for generating, deploying, and maintaining a comprehensive documentation website according to best practices for research software \cite{TenSimpleRulesForDocumentingSciSoft, WhatMakesCompSoftSuccessful}, leaving users with no documentation tasks other than writing docstrings and short software descriptions. For this, a \href{https://www.sphinx-doc.org}{Sphinx} website template is included, fully designed using a standardized layout for scientific software libraries based on the popular \href{https://pydata-sphinx-theme.readthedocs.io/}{PyData theme}. Many features including logo, color scheme, font, and icons are dynamically managed by PyPackIT's control center, enabling rapid customization and consistent maintenance. The standardization of project components and development workflow allow PyPackIT to pre-fill the template with streamlined documentation materials for the project, including:

- Detailed contribution manuals on how to report issues and security vulnerabilities, request changes, contribute artifacts, and maintain the software library.
- Instructions, requirements, restrictions, and standards for the project's development workflow.
- Generic project structure and package information like version scheme.
- A code of conduct defining rules for proper social practices.
- Instructions for library users to navigate the website, find information, and get support.

Moreover, PyPackIT integrates templating capabilities into website source files, 
with full access to project's configurations and metadata. 
This enables PyPackIT to dynamically generate and maintain customized website content, including:

- Homepage featuring the project's name, logo, description, and key features.
- Detailed installation guides and package information like requirements and dependencies.
- A governance model clarifying the team structure and decision making processes of the project.
- Project information such as license, copyright, team member details, and contact information. 
- Links to the project's issue trackers, discussion forums, and repositories on GitHub, PyPI, and if applicable, conda-forge.

Additional documentation materials are automatically added during the development, 
reflecting the project's progress:

- A full API reference is continuously updated using docstrings in source code, providing documentation for all package components in a well-structured layout.
- Comprehensive release notes are generated by processing issue data and other project settings, documenting important changes in each new package release, such as bug fixes, improvements, and added, modified, or removed features and requirements. These are added to the user changelog, and posted on the website's news blog, along with temporary announcement banners to notify users.
- Developer changelogs are updated with structured information from merged PRs, maintaining a chronological documentation of the development process.

The documentation can be further enriched by providing a general overview of the motivations, 
objectives, and capabilities of the scientific software library. 
For adding such custom content, both plain text and markup languages 
like reStructuredText (reST) and \href{https://mystmd.org/}{MyST Markdown} are supported, 
offering numerous options for typography. 
Moreover, using powerful plugins, such as \href{https://myst-parser.readthedocs.io/}{MyST-Parser}, 
\href{https://sphinx-design.readthedocs.io/}{Sphinx-Design}, 
\href{https://sphinxcontrib-bibtex.readthedocs.io/}{SphinxContrib-BibTeX}, 
\href{https://ablog.readthedocs.io/}{ABlog}, and \href{https://giscus.app/}{Giscus}, 
rich features are made available via simple directives, including:

- Elements for writing scientific documentation, such as executable code blocks, diagrams, charts, figures, tables, and mathematical notation.
- Referencing and citation options with support for BibTeX bibliographies.
- Web components like grids, cards, dropdowns, tabs, admonitions, buttons, and icons, for a beautiful and responsive design.
- A news blog, with support for commenting, web feeds, searching, and categorization.

Build and deployment of the website are also automated by PyPackIT's CI/CD pipelines. 
Changes affecting the website trigger the build process, 
providing a preview for review. 
Once approved for production, the updated website is deployed on
\href{https://pages.github.com/}{GitHub Pages}—GitHub's free static web hosting service, 
publicly accessible via a default URL. 
To use a custom domain instead, users only need to provide it in the control center. 
Additionally, hosting on the \href{https://readthedocs.org/}{Read The Docs} platform is supported, 
requiring only an account specification. 
For enhanced project findability and visibility, \href{https://ogp.me/}{Open Graph} metadata 
are included on each website page using the \href{https://github.com/wpilibsuite/sphinxext-opengraph}{SphinxExt-OpenGraph} plugin, 
enabling search engine optimization (SEO) and rich previews on social media.

In addition to the website, PyPackIT also generates several GitHub-specific documentation files 
that are directly displayed on repositories. 
These are automatically generated according to highly customizable templates provided in PyPackIT's control center, 
and include \href{https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file#supported-file-types}{community health files} 
for \href{https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files}{citation}, 
funding, support, security, contributing, governance, and code of conduct, 
as well as a dynamic \href{https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes}{README file} 
that presents a concise project overview on GitHub. 
Acting as the front page of the repository, the README file 
has a visually appealing graphic design, 
and contains key project information with links to main sections of the documentation website. 
Moreover, it includes a comprehensive collection of dynamic badges 
according to best practices \cite{RepositoryBadges}, 
providing users and contributors with an up-to-date overview of project specifications, 
status, health, progress, and other statistics.

## Version Control

PyPackIT fully integrates with Git to automate tasks 
like branch and commit management, tagging, and merging. 
Motivated by well-established models such as 
\href{https://nvie.com/posts/a-successful-git-branching-model/}{Git Flow} 
and \href{https://about.gitlab.com/topics/version-control/what-is-gitlab-flow/}{GitLab Flow}, 
PyPackIT implements a branching strategy that enables the rapid evolution of research software 
according to Continuous software engineering best practices \cite{CICDSystematicReview}, 
while ensuring the reproducibility and sustainability of computational studies 
that depend on the library's earlier releases. 
The branching model includes persistent release branches and transient development 
and pre-release branches:

- The main branch of the repository is a special release branch. It always contains the latest final release of the library, while its control center settings are used as the source of truth for all non-version-specific project configurations.
- Development branches are automatically created from target release branches, providing an isolated environment to integrate new changes into the project, before they are merged back into target branches and deployed to production. Each change can be implemented in a separate development branch, enabling the simultaneous development of multiple orthogonal features and release candidates.
- Pre-release branches are automatically created from development branches when users decide to first publish a new package version as a pre-release. They facilitate the implementation and documentation of modifications during the pre-release period, before the final product is merged into a release branch.
- Release branches each contain the latest release of an earlier major version of the library. They are automatically created from the main branch each time a backward-incompatible change is about to be merged. This enables proof-of-concept scientific software libraries to rapidly evolve into mature products, while all major versions are automatically preserved for long-term maintenance and support.

Moreover, to provide scientific libraries with a clear and transparent development history 
and ensure their long-term findability and accessibility, 
all releases are automatically versioned and tagged. 
For this, PyPackIT implements a version scheme based on 
\href{https://semver.org/}{Semantic Versioning} (SemVer), 
which clearly communicates changes to the library's public API \cite{EmpComparisonOfDepIssues, WhatDoPackageDepsTellUsAboutSemVer}:

- Releases are denoted with a version number \verb|X.Y.Z|, where \verb|X|, \verb|Y|, and \verb|Z| are non-negative integers named major, minor, and patch versions, respectively.
- Release version \verb|1.0.0| defines the library's public API.
- In each subsequent release, one of major, minor, or patch versions are incremented by 1 while the lesser ones are reset to 0, depending on the type of most important change in the new public API:
  - Major: when backward-incompatible changes are made.
  - Minor: when new features are added while no backward-incompatible change is made.
  - Patch: when all changes are backward-compatible bug fixes or improvements.

PyPackIT uses correlated issue ticket data to determine whether each release 
corresponds to a new major, minor, or patch version. 
It then automatically calculates the full version number, 
by comparing the latest version tags in the development branch and its target release branch. 
Subsequently, for automatic deployment on indexing repositories such as PyPI and TestPyPI, 
PyPackIT generates a canonical public version identifier 
in accordance with the \href{https://packaging.python.org/en/latest/specifications/version-specifiers/}{latest PyPA specifications}:

- Final releases are only denoted with a version number.
- Pre-release versions contain an additional segment, denoting the pre-release phase (alpha, beta, or release candidate) and the corresponding ticket number.
- Developmental releases are versioned by adding an extra segment to the corresponding pre-release version, which chronologically numbers each change during the implementation of upcoming package features.

In line with Continuous software engineering best practices \cite{CICDSystematicReview}, 
publishing developmental and pre-releases allows the community to thoroughly investigate 
upcoming changes and provide feedback, improving the quality of scientific libraries 
and reducing the risk of using buggy software in research. 
By incorporating the ticket number as a unique identifier for these releases, 
PyPackIT enables scientific libraries to simultaneously develop 
and publish multiple release candidates. 
This facilitates frequent experimentation and modifications even within each iteration, 
which are crucial for research software development 
due to its uncertain and evolving nature \cite{SurveySEPracticesInScience}. 

## Issue Management

PyPackIT establishes a cloud-based development workflow, 
in which new tasks in the project start by submitting an issue ticket to its ITS, 
enabling the community to readily propose changes and ensuring that the entire evolution 
of the scientific software library is properly documented 
in a traceable and transparent way. 
To facilitate this, PyPackIT automatically configures and maintains the repository's GHI, 
according to customizable configurations in the control center. 
For example:

- Submission options are provided for individual issue types, such as requesting bug fixes, new features, and other changes in various project components, including the library, test suite, documentation website, and control center settings.
- Specialized submission forms are supplied for each issue type according to best practices \cite{WhatMakesAGoodBugReport, NeedsInBugReports, QualityOfBugReportsInEclipse}, offering relevant instructions to users and asking for type-specific information via machine-readable input types.
- Dynamic data are automatically updated in issue forms, eliminating the need for frequent manual maintenance. These include lists of supported releases, operating systems, and Python versions, which let users easily specify issue details from dropdown menus.
- Labels are automatically created and updated, providing useful categorization options for issues and PRs.


Furthermore, PyPackIT automates the bulk of management activities throughout the workflow. 
After an issue is submitted, it processes the machine-readable ticket inputs 
to perform several tasks, including:

- Formatting user inputs to provide a consistent and concise overview for each ticket.
- Labeling tickets based on issue type and details to facilitate the organization and findability of the project's ongoing and finished tasks.
- Assigning tasks to maintainers according to a declarative project governance model in the control center, which defines member roles and privileges.
- Attaching a standardized form to tickets to facilitate the documentation and tracking of the development process. The form contains a timeline that is automatically updated by PyPackIT with important milestones to reflect the progress. In addition, it contains a structured template for documenting software requirements specification, design description, implementation plans, and other development details.

Therefore, after ticket submission, notified maintainers only need to triage the issue, 
which is also facilitated by PyPackIT. 
For example, by posting a comment under an issue, 
project maintainers can command PyPackIT to automatically test 
a specific version of the library with given test cases and under given conditions. 
This greatly accelerates bug report triage, 
eliminating the need for manual branch creation and test suite modification and execution. 
If the new test cases fail, PyPackIT automatically adds them to the project's test suite 
and initiates a bug fix task, thus providing a streamlined solution 
for continuously turning bugs into new test cases, 
to validate the fix and prevent future recurrences 
according to best practices \cite{BestPracticesForSciComp, 10SimpleRulesOnWritingCleanAndReliableSciSoft}. 

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

## Continuous Integration and Deployment

When an issue is ready for implementation, PyPackIT automatically opens a draft PR 
for each created development branch, 
filled with information from the corresponding issue data, 
and labeled accordingly. 
Developers can thus immediately start implementing the specified changes. 
With each commit on a development branch, 
PyPackIT runs a CI pipeline to integrate the new changes into the code base 
according to best practices \cite{CICDSystematicReview, ModelingCI, ContinuousSoftEng}:

- Modifications in control center files are applied to all dynamic files in the branch.
- Code formatting standardization is applied to all changed files according the \href{https://black.readthedocs.io/}{Black} code style.
- Static code analysis including type checking is performed on changed source files to check for potential errors, code violations, security issues, and other code smells, using well-established Python linters such as \href{https://docs.astral.sh/ruff/}{Ruff}, \href{https://mypy.readthedocs.io/}{Mypy}, and \href{https://codeql.github.com/}{CodeQL}.
- Available fixes are automatically applied to committed files.
- Source and binary distributions are built when package files are modified.
- The test suite is executed on a matrix of supported operating systems and Python versions to verify the correctness and compatibility of changes applied to source files.
- Documentation website is built to reflect the latest changes in package and website source files and configurations.
- Reports and artifacts are attached to each CI run, including results of formatting, static code analysis, testing, CI logs, and built website and distribution packages, improving the visibility of integration status and facilitating reviews. 
- The draft PR is updated to reflect the progress. If the commit message matches one of the tasks in the implementation list of the issue ticket, that task is automatically marked as complete.

When package-related changes are successfully integrated, 
a new developmental release is automatically versioned, tagged, and published to TestPyPI. 
This serves several purposes \cite{CICDSystematicReview}:

- The library is automatically tested in a production-like environment, ensuring that it works as intended after download and installation on user machines.
- New features and developments can be easily shared with other collaborators, enabling early feedback and reviews during the implementation phase.
- The entire development progress leading to each final release is permanently documented in a clear and transparent manner.

When all implementation tasks specified in a PR are marked as complete, 
PyPackIT automatically initiates the process to merge the changes into production:

- Reviewers are automatically designated to the PR according to rules defined in the control center based on several different factors, such as changed files or issue type.
- The status and outputs of CI pipelines are displayed in the PR, and automatically updated after each revision during the review process. 

When the PR is approved by reviewers, PyPackIT automatically performs the merging:

- Project changelogs in the repository and documentation website are updated with information from the issue ticket and PR, maintaining detailed chronological records of all key aspects of the development process for both users and developers of the scientific library. PyPackIT automatically correlates each implementation task with a specific section of a specific changelog, based on \href{https://www.conventionalcommits.org/}{Conventional Commits} types defined in the control center. For example, details of implementation tasks marked with the \verb|fix| commit type are added to Bug Fixes section of the user changelog for library's public API.
- A consistent and clear Git history is maintained by squash merging the development branch into the corresponding release branch. To establish issue–commit links and reflect the development documentation in the project's VCS, the commit message contains the issue ticket number and other details such as type, scope, and description.
- When changes are merged into the repository's main branch, all project components are updated to reflect new configurations according to control center files. These include project-wide settings, for example for the development workflow, environment, and the repository.

If the merged changes correspond to a new release or pre-release of the library, 
the CD pipeline carries out additional deployment tasks:

- Release notes are generated from issue/PR information and changelogs, and by analyzing the package metadata before and after the changes.
- Distribution and binary packages are built, versioned, tagged, and published on PyPI, GitHub, and Zenodo, along with updated identifiers, metadata, release notes, and documentation.
- Documentation website is updated and deployed online, where a banner is added to announce the new release, and the release documentation is added as a new blog post.

## Continuous Maintenance, Refactoring, and Testing

To ensure the long-term sustainability of research software, 
PyPackIT periodically runs Continuous pipelines on a scheduled basis, 
to check for problems and perform automatic fixes and updates. 
In addition to CCA mentioned in \hyperref[section-controlCenter]{Section 2.1}, tasks include:

- **CT**: To ensure compatibility with up-to-date environments, 
  each software release is periodically tested using latest available dependencies, 
  including new Python versions, according to user-provided version specifiers.
- **CR**: Code analysis and formatting tasks are performed using updated tools 
  and standards to curb the ever-increasing code complexity 
  and maintain quality and consistency during both development and support phases. 
- **CM**: To maintain the health of the development environment, 
  the repository and its components are cleaned up, 
  removing outdated development artifacts, such as builds, logs, and reports.

During each run, PyPackIT automatically applies updates and fixes to a new branch, 
and creates a PR for review by maintainers. 
After approval, changes are automatically merged into the project 
and applied to all components. Similarly, if a problem is found, 
a new issue ticket is automatically submitted to the issue tracking system, 
notifying project maintainers to take action. 
These automated processes significantly simplify 
and encourage maintenance activities \cite{CanAutoPRsEncourageDepUpgrade}, 
facilitating the prolonged development and support of research software.

## Licensing

PyPackIT simplifies project licensing and copyright management,
in accordance with best practices for research software 
\cite{BarelySufficientPracticesInSciComp, ELIXIRSoftwareManagementPlan, SustainableResearchSoftwareHandOver, ShiningLight, 10RuleForSoftwareInCompBio}. 
It provides a variety of \href{https://opensource.org/licenses}{OSI-approved Open Source Licences} 
that support the commercialization of scientific software \cite{SettingUpShop} 
and fulfil the Bayh–Dole requirements for patenting publicly funded products \cite{BayhDole}. 
In the control center, users can select a license either from the included options, 
or by inputting details for any other license. 
By default, the \href{https://www.gnu.org/licenses/agpl-3.0.en.html}{GNU Affero General Public License v3.0} 
is selected for new projects, which is a strong copyleft license promoting open science 
by enforcing downstream source disclosure. 
Other available options include \href{https://spdx.org/licenses/MIT.html}{MIT}, 
\href{https://spdx.org/licenses/BSL-1.0.html}{BSL}, 
and various other \href{https://www.gnu.org/licenses/licenses.html}{GNU licenses}. 
The specified license is automatically integrated throughout the project:

- Licence and copyright notices are customized with project information 
  like name, owner, and start date.
- A license file is added to the repository, where GitHub can recognize and display it.
- The license file is incorporated in all package releases.
- License identifiers are added to the package metadata.
- Full license and copyright information are featured on the documentation website.
- A full copyright notice is included in library source files.
- A short copyright notice is added to the footer of all README files.

## Security

To enhance project security while supporting community collaboration, 
PyPackIT incorporates several security measures:

- Protection rules allow only PyPackIT and project administrators 
  to manage branches and tags, ensuring the integrity of the repository. 
- Security scanning performed by static code analysis tools 
  ensure that changes do not introduce security vulnerabilities into the code base.
- Dependency monitoring is carried out by GitHub's Dependabot, 
  alerting project maintainers in case of dependency issues, and proposing updates when possible.
- External PRs require an approval by project maintainers before CI/CD pipelines can run.
- GHA workflows are developed according to best practices 
  \cite{AutoSecurityAssessOfGHAWorkflows, GHADocsSecurity} 
  to prevent security issues that may arise through command injection, 
  use of untrusted applications, exposure of tokens and secrets, 
  and loose workflow permissions, among others.

Moreover, to ensure that PyPackIT itself is highly secure, 
its entire infrastructure is natively implemented and self-contained. 
With the exception of a handful of fundamental GitHub Actions and Python libraries 
from trusted vendors like GitHub and PyPA, 
PyPackIT does not rely on other third-party dependencies.
