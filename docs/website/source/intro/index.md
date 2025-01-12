---
ccid: intro
---

(intro)=
# Introduction

|{{ ccc.name }}| is an open-source, ready-to-use, cloud-based automation tool
that streamlines every step of the software development life cycle,
from initiation and configuration to deployment and long-term maintenance.
In line with the latest software engineering best practices,
it ensures the quality and FAIRness (Findability, Accessibility, Interoperability, Reusability)
of software projects,
while significantly accelerating development
and lowering production costs at the same time.
Promoting adoption and collaboration,
|{{ ccc.name }}| specializes in the production of [Python](#bg-py) applications on [GitHub](#bg-gh)—the
most popular programming language and social coding platform, respectively.
|{{ ccc.name }}| is readily installable in both new and existing GitHub repositories,
providing them with a comprehensive and robust project infrastructure ({numref}`fig-features`) including:

- [**Control Center**](#overview-cc): A centralized user interface to automatically manage 
  all project metadata and settings according to [cloud-native](#bg-cloud-native) practices 
  like [Infrastructure-as-Code](#bg-iac) and [Continuous Configuration Automation](#bg-cca). 
  It enables dynamic content management for the entire project, 
  simplifying setup, configuration, and maintenance via built-in templating, 
  inheritance, and synchronization features 
  that automatically apply modifications to all project components. 
  Preconfigured according to the latest engineering best practices, 
  it only requires users to fill project-specific metadata,
  while allowing for extensive customization.
- [**Python Package**](#overview-pkg): A build-ready package skeleton
  with all necessary source files and configuration files, 
  automatically customized according to control center settings. 
  Users only need to add application code to the provided source files, 
  while |{{ ccc.name }}| automates all packaging, versioning, [licensing](#overview-license),
  build, distribution, and indexing tasks.
  |{{ ccc.name }}| supports automatic deployment to various indexing repositories, 
  including Anaconda, PyPI, Zenodo, GitHub Releases, and any Docker registry.
- [**Test Suite**](#overview-testsuite): A fully operational testing infrastructure 
  enabling immediate adoption of test-driven methodologies. 
  Requiring users to only write test cases in the provided package, 
  |{{ ccc.name }}| automatically performs unit, regression, end-to-end, 
  and functional testing throughout the development life cycle. 
  This ensures software quality and correctness, 
  while improving awareness of software health status via notifications and reports. 
  The test suite is automatically packaged and distributed along each release, 
  facilitating the reproducibility of test results 
  for verification of software functionality and performance.
- [**Documentation**](#overview-docs): An automated documentation website
  deployed on GitHub Pages and Read The Docs platforms, 
  leaving users with minimal documentation tasks such as writing issue tickets and docstrings. 
  The website comes fully designed and prefilled with detailed developer and user manuals, 
  and is automatically updated with project information, software API documentation, 
  and comprehensive release notes and changelogs. 
  Most website elements are dynamic and easily customizable via |{{ ccc.name }}|'s control center, 
  requiring no knowledge in web design. 
  The control center also enables the dynamic generation of any document file in Markdown format, 
  such as a repository README file with dynamic status badges
  and other self-updating project information.


:::{figure} /_media/figure/key_features_dark.svg
:alt: PyPackIT Key Features
:class: dark-light themed
:width: 600px
:align: center
:name: fig-features

|{{ccc.name}}|'s key infrastructure elements (left) and workflows (right).
:::

:::{image} /_media/figure/key_features_light.svg
:class: hidden
:::


After installation, |{{ ccc.name }}| automatically activates in response to various repository events, 
executing appropriate tasks on the GitHub Actions cloud computing platform. 
This establishes an automated pull-based software development workflow 
tailored to collaborative software engineering needs. 
|{{ ccc.name }}|'s workflow accelerates progress and innovation 
by promoting community engagement and feedback, 
while ensuring project continuation and sustainability 
by emphasizing proper task management, software inspection, and documentation. 
The workflow includes comprehensive Continuous software engineering pipelines 
that use the latest tools and technologies to establish an automated Agile software development process. 
This enables the experimental and highly iterative development of software, 
while reducing variance, complexity, cost, and risk.
Overall, |{{ ccc.name }}|'s workflow automates the bulk of 
repetitive engineering and management activities throughout the software life cycle, including:

- [**Issue Management**](#overview-its): The project's issue tracking system is dynamically maintained, 
  supplied with specialized submission forms to collect type-specific user inputs 
  in a structured and machine-readable format. 
  This allows |{{ ccc.name }}| to automate issue management activities, 
  such as ticket labeling and organization, bug triage, task assignment, 
  design documentation, issue–commit linkage, and progress monitoring.
- [**Version Control**](#overview-vcs): To enable rapid project evolution 
  while ensuring the long-term usability and sustainability of earlier releases, 
  |{{ ccc.name }}| implements a specialized branching model and version scheme 
  for simultaneous publication and support of multiple releases. 
  Fully integrating with Git, |{{ ccc.name }}|'s workflow automates version control tasks 
  such as branching, tagging, merging, and commit management.
- [**Continuous Integration**](#overview-ci) and [**Deployment**](#overview-cd):
  |{{ ccc.name }}|'s CI/CD pipelines automate tasks 
  such as code style formatting, static code analysis, type checking, testing, build, 
  containerization, and release, thus eliminating the need for dedicated integration and deployment teams, 
  while increasing control, integrity, scalability, security,
  and transparency of the Agile development process.
- [**Continuous Maintenance, Refactoring, and Testing**](#overview-cm):
  |{{ ccc.name }}| periodically performs 
  automated maintenance tasks to ensure the long-term sustainability of projects 
  and the health of the research software development environment. 
  These tasks include testing and refactoring code, 
  updating dependencies and development tools, 
  and cleaning up the repository to remove outdated development artifacts, 
  such as builds, logs, and reports.


In summary, |{{ ccc.name }}| provides Python projects on GitHub 
with a comprehensive, dynamic, and highly customizable project skeleton 
along with a ready-to-use cloud-native development environment. 
This eliminates the need for manual project setup and configuration, 
enabling developers to immediately begin the actual implementation of software, 
even directly from the web browser. 
|{{ ccc.name }}|'s automated development workflow
greatly simplifies the software development process, 
reducing manual tasks to writing issue tickets, 
application code, test cases, and minimal documentation. 
All other activities are automatically carried out on the cloud, 
consistently enforcing best practices throughout the software development life cycle. 
Since these repetitive software engineering and management activities 
are the most common cause of problems in many free and open-source software (FOSS) projects, 
their automation significantly accelerates development
and improves product quality with minimal cost and effort. 
|{{ ccc.name }}| thus allows projects to focus solely on creative aspects,
overcoming common challenges in FOSS development
such as limited funding, time, staffing, and technical expertise.


:::{admonition} Getting Started
:class: seealso

Continue to the [Motivation](#overview) section
where we outline key aspects of software engineering and
the challenges they present to FOSS projects,
highlighting |{{ ccc.name }}|'s solutions to these challenges.
If you can't wait to get started with |{{ ccc.name }}|,
skip to the [Overview](#overview) section for
a more in-depth summary of |{{ ccc.name }}|'s 
key features and capabilities, before proceeding to the
[User Manual](#manual) for detailed instructions
on how to install and use |{{ ccc.name }}| in your project.
The [Background](#bg) section offers
supplementary information on key concepts, methodologies, 
tools, and technologies used in |{{ ccc.name }}|,
and is referenced throughout the documentation.
:::
