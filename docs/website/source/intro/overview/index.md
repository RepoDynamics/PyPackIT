---
ccid: overview
---

# Overview

This section offers a more detailed overview of 
some of PyPackIT's key components, features and capabilities.


## Continuous Configuration Automation

{{ ccc.name }} facilitates project configuration, customization, and management
by introducing a centralized control mechanism
based on DevOps practices like IaC.
It provides a control center as the singular user interface
to manage the entire project, and even multiple projects at once.
The control center consolidates all project configurations, metadata,
and variable content into one repository location under version control,
allowing for easy tracking of all settings throughout the project lifespan.
To improve transparency and replicability of configurations
and eliminate the need to manage multiple file formats and locations,
manual settings are replaced by declarative configuration definitions,
all unified and structured in [YAML](https://yaml.org/) format—a standard, 
concise, human-readable data serialization language.
PyPackIT automatically applies all settings to corresponding project components 
via APIs and dynamically generated files, 
effectively rendering the entire project configuration and content dynamic.
To further simplify dynamic project configuration and content management,
the control center is equipped with several features:

- **Preconfiguration**:
  For all generic configurations, 
  default settings are provided based on the latest standards and best practices,
  requiring only project-specific metadata to be declared.
- **Templating**:
  Data reuse is facilitated by templating features that enable
  dynamic referencing of all control center contents throughout project files,
  removing redundancy and allowing for centralized and automatic updates.
- **Inheritance**:
  Data can be dynamically inherited from external sources, 
  allowing for consistent creation and centralized maintenance
  of multiple projects with shared settings.
- **Augmentation**:
  Additional dynamic data are generated during each run
  by analyzing the repository and retrieving information from web APIs
  to minimize manual inputs and updates.
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

Examples of dynamically maintained project components and settings include:

- **Project Descriptors**:
  Name, Title, Abstract, Keywords, Highlights
- **Project Metadata**:
  License, Citation, Funding, Team, Roles, Contacts
- **Package and Test Suite**:
  Build Configurations, Requirements, Dependencies, 
  Metadata, Version, Entry Points, Docstrings
- **Documentation**:
  API Reference, Installation Guide, Contribution Guide, Governance Model,
  Security Policy, README Files, Badges, Website and Theme Configurations
- **Issue Tracking**:
  GHI Settings, Issue Submission Forms, Labels, Pull Request Templates,
  Design Documents, Discussion Forms
- **Version Control**:
  Git/GitHub Repository Settings, Branch and Tag Configurations,
  Protection Rules, Commit Types, Changelogs, Release Notes
- **Workflows**:
  Continuous Pipeline Configurations, Tool Settings, Development Environment Specifications


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


## Continuous Deployment


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



## Continuous Maintenance, Refactoring, and Testing

To ensure long-term software sustainability, 
{{ ccc.name }} periodically runs Continuous pipelines on a scheduled basis 
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

{{ ccc.name }} greatly facilitates project licensing and copyright management,
in accordance with best practices for {term}`FOSS`
{cite}`QuickGuideToLicensing, BarelySufficientPracticesInSciComp, ELIXIRSoftwareManagementPlan, SustainableResearchSoftwareHandOver, ShiningLight, 10RuleForSoftwareInCompBio`
and the upcoming [PEP 639](https://peps.python.org/pep-0639/),
by integrating with the System Package Data Exchange ([SPDX](https://spdx.org/)) license standard.
This allows users to define complex licenses for their projects
using a simple [SPDX license expression](https://spdx.github.io/spdx-spec/v3.0.1/annexes/spdx-license-expressions/).
{{ ccc.name }} supports all [SPDX License List](https://spdx.org/licenses/) entries
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
{{ ccc.name }} will then automatically download the required license data and integrate it into the project:

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

Moreover, to ensure that {{ ccc.name }} itself is highly secure, 
its entire infrastructure is natively implemented and self-contained. 
With the exception of a handful of fundamental {term}`Actions` and Python libraries 
from trusted vendors like GitHub and PyPA, 
PyPackIT does not rely on other third-party dependencies.
This gives the {{ ccc.name }} team full control over the software stack,
allowing us to rapidly respond to issues
and continuously improve the product,
while making {{ ccc.name }} fully transparent and easily auditable by the community.
