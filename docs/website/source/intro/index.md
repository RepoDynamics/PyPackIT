---
ccid: intro
---

# Introduction

PyPackIT is an open-source, ready-to-use, cloud-based automation tool
that streamlines the initiation, configuration, development, publication,
maintenance, management, and support of FAIR scientific software projects
in line with the latest research software engineering best practices. 
To facilitate interoperability, reusability, and adoption, 
PyPackIT is specialized in the production of software libraries in Python, 
the leading programming language for scientific applications. 
Promoting accessibility and collaboration, it supports open-source development on GitHub, 
one of the most popular and suitable social coding platforms for research software. 
PyPackIT is readily installable in both new and existing GitHub repositories, 
providing them with a comprehensive and robust project infrastructure, including:

- **Control Center**: A centralized user-interface to automatically control all project metadata and settings 
  according to DevOps practices like IaC and CCA. 
  It enables dynamic configuration management for the entire project infrastructure,
  simplifying project setup, customization, and maintenance via automatic data templating,
  inheritance, and synchronization features that instantly apply modifications to all project components.
  Pre-configured according to research software requirements,
  it requires most users to only fill project-specific metadata.
- **Python Package**: A build-ready package skeleton with pre-configured source files and configuration files,
  automatically customized according to project metadata and settings. 
  Users only need to add scientific code to the provided source files, 
  while PyPackIT automates all packaging, versioning, licensing, distribution, and indexing tasks. 
  To facilitate research software findability and usage, each new release is published 
  to PyPI, Zenodo, and GitHub, with a persistent DOI 
  ensuring reliable citation and reproducibility of computational studies.
- **Test Suite**: A fully operational testing infrastructure enabling the 
  immediate adoption of test-driven methodologies. 
  Requiring users to only write test cases in the provided package, 
  PyPackIT automatically performs unit, regression, end-to-end, and functional testing 
  throughout the development life-cycle, ensuring research software quality and correctness, 
  while improving awareness of software health status via notifications and reports. 
  The test suite is automatically packaged and distributed along each release, 
  facilitating the reproducibility of test results for verification of software functionality and performance.
- **Documentation**: An automated documentation website deployed online to GitHub Pages 
  and Read The Docs platforms, leaving users with no documentation tasks 
  other than writing issue tickets and docstrings. 
  Fully designed and pre-filled with detailed developer and user manuals, 
  the website is also automatically updated with project information, 
  software API documentation, and comprehensive release notes and changelogs. 
  Most website elements are dynamic and easily customizable via PyPackIT's control center,
  requiring no knowledge in web design.

After installation, PyPackIT automatically activates in response to various repository events, 
executing appropriate tasks on the GitHub Actions cloud computing platform. 
It thus establishes an automated software development workflow tailored to research software needs, 
based on a well-tested pull-based model for collaborative research software engineering. 
PyPackIT's workflow accelerates progress and innovation by promoting community engagement and feedback, 
while ensuring project continuation and sustainability by emphasizing proper task management, 
software inspection, and documentation. 
It includes comprehensive Continuous software engineering pipelines 
that use the latest tools and technologies to provide an automated Agile software development process, 
enabling the experimental and highly iterative development of research software, 
while reducing variance, complexity, cost, and risk. 
PyPackIT's workflow automates the bulk of repetitive engineering and management activities 
throughout the software life-cycle, including:

- **Issue Management**: The project's ITS is dynamically maintained, 
  supplied with specialized issue submission forms to collect type-specific user inputs 
  in a structured and machine-readable format. 
  This allows PyPackIT to automate issue management activities, 
  such as ticket labeling and organization, bug triage, 
  task assignment, design documentation, and progress monitoring.
- **Version Control**: To enable rapid project evolution 
  while ensuring the reproducibility of earlier computational results, 
  PyPackIT implements a specialized branching model and version scheme for 
  simultaneous publication and support of multiple releases. 
  Fully integrating with Git, PyPackIT's workflow automates version control tasks, 
  such as branching, tagging, merging, and commit management.
- **Continuous Integration and Deployment**: PyPackIT's CI/CD pipelines automate tasks 
  such as code style formatting, static code analysis, type checking, testing, build, and release, 
  thus eliminating the need for dedicated integration and deployment teams, 
  while increasing control, integrity, scalability, security, and transparency of the Agile development process.
- **Continuous Maintenance, Refactoring, and Testing**: To ensure the long-term sustainability of projects 
  and maintain the health of research software and its development environment, 
  PyPackIT periodically performs automated maintenance tasks, 
  such as testing and refactoring code, updating dependencies and development tools, 
  cleaning up the repository, and removing outdated development artifacts such as builds, logs, and reports.

Therefore, PyPackIT's comprehensive, dynamic, and highly customizable project skeleton 
and cloud-native development environment eliminate the need for project setup and configuration, 
enabling scientific Python projects to immediately begin the actual implementation of software, 
even directly from the web browser. 
PyPackIT's automated development workflow greatly simplifies the research software development process, 
limiting manual tasks to writing issue tickets, scientific code, test cases, and minimal documentation, 
while other activities are automatically carried out on the cloud, 
consistently enforcing best practices throughout the software development life-cycle. 
Since these repetitive software engineering and management activities are 
the most common cause of problems in scientific software projects, 
their automation significantly improves product quality, 
while allowing developers to solely focus on the scientific aspects of their project. 
PyPackIT thus greatly benefits research software engineering 
that is often faced with challenges regarding funding, time, and staffing, 
by accelerating development and enabling the consistent and reliable production of high-quality software 
with minimal cost and effort. 
As the scientific inquiry process increasingly relies on research software, 
PyPackIT can be a valuable asset to computational studies 
that are now an integral part of many scientific fields. 






































Serving as a starting point for new users,
this section provides an introduction to
{{ccc.name}}, its motivations, objectives, and capabilities,
along with a summary of related fundamental concepts and useful background information.
If this is your first time using {{ccc.name}},
we highly recommend that you at least read through the [overview](overview/index.md) page,
before proceeding to the [user manual](../manual/index.md).


::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} Outline
:link: outline/index
:link-type: doc
:class-title: sd-text-center

An abstract of the {{ccc.name}} project,
outlining its motivations, purpose, and objectives,
along with a short summary of its capabilities and functionalities.
:::

:::{grid-item-card} Background
:link: background/index
:link-type: doc
:class-title: sd-text-center

A background review of the state of the art in the software development process
within the Python ecosystem, and its current challenges and problems.
:::

:::{grid-item-card} Overview
:link: overview/index
:link-type: doc
:class-title: sd-text-center

An in-depth high-level overview of {{ccc.name}} and all its functionalities,
the problems they address, and the value they bring to your project.
:::

:::{grid-item-card} Basics
:link: basics/index
:link-type: doc
:class-title: sd-text-center

A summary of basic concepts and related background information,
essential to fully understanding and utilizing {{ccc.name}}.
:::

::::

```{bibliography}
```