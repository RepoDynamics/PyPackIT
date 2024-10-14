---
ccid: intro
---

(intro)=
# Introduction

PyPackIT is an open-source, cloud-based software suite
hosted on GitHub at https://github.com/RepoDynamics. 
It comprises several {term}`Actions` and Python applications, 
which can be installed in GitHub repositories to perform automated tasks on {term}`GHA`. 
To facilitate installation, PyPackIT includes a template repository at
https://github.com/RepoDynamics/PyPackIT.
There, by clicking the
{{ '[{{bdg-success}}`Use this template`](https://github.com/new?template_name={}&template_owner={})'.format(ccc.repo.name, ccc.team.owner.github.id) }}
button, users can create a new GitHub repository 
that automatically contains all the necessary files to run PyPackIT,
such as GHA workflows and configuration files. 
Installation in existing repositories is supported as well, 
simply requiring users to add these files (cf. [Installation Guide](#install)).


:::{figure} /_media/figure/key_features_dark.svg
:alt: PyPackIT Key Features
:class: dark-light themed
:width: 600px
:align: center
:name: fig-features

{{ccc.name}}'s key infrastructure elements (left) and workflows (right).
:::
:::{image} /_media/figure/key_features_light.svg
:class: hidden
:::


PyPackIT is a ready-to-use automation tool,
fully configured in accordance with the latest software engineering guidelines and best practices. 
Upon installation, users only need to invest a few minutes in basic tasks
such as filling project-specific information in the provided configuration files. 
PyPackIT then takes over, automatically setting up the repository 
and generating a complete infrastructure for the project ({numref}`fig-features`), 
including a python package, test suite, documentation website, license, 
configuration files for various development tools and services, 
and community files such as a dynamic repository README. 
The documentation website along with an initial release of the library 
can be immediately deployed online, registering the project in indexing repositories 
and facilitating its discovery from the beginning of the project {cite}`4SimpleRecs, CICDSystematicReview`. 
All metadata and settings are readily customizable via PyPackIT's configuration files, 
which form a unified control center enabling {term}`CCA` 
for the entire project infrastructure and development environment
throughout the software life-cycle.

After installation, PyPackIT establishes an automated software development workflow ({numref}`fig-workflow`)
tailored to user needs, 
based on a well-tested pull-based model for collaborative research software engineering.
It includes comprehensive Continuous software engineering pipelines 
that use the latest tools and technologies
to provide an automated Agile software development process, 
enabling the experimental and highly iterative development of software, 
while reducing variance, complexity, cost, and risk.
PyPackIT's workflow activates automatically in response to various repository events,
such as submission of issue tickets, commits, and pull requests.
It then analyzes the triggering event and the current state of the repository
to execute appropriate tasks on {term}`GHA`.
This automates the bulk of repetitive engineering and management activities 
throughout the software life-cycle,
leaving users with only four manual tasks:

1. **Report**: Each task in the project starts by submitting a ticket to its {term}`ITS`. 
   PyPackIT facilitates reports by automatically configuring and maintaining {term}`GHI`
   to provide users with dynamic submission forms specialized for various issue types.
   Following a ticket submission, PyPackIT automatically performs issue management tasks,
   reducing the triage process to a simple decision on whether to implement the task.
2. **Design**: After an issue ticket is approved,
   developers only need to write a short design document 
   by filling a form attached to the ticket. 
   PyPackIT's automated version control then activates, 
   creating a ready-to-use branch for implementation, 
   along with a dynamically maintained {term}`PR` for progress tracking. 
3. **Commit**: With PyPackIT's comprehensive infrastructure, 
   implementation is simplified to writing essential code, docstrings,
   and test cases in the provided skeleton files 
   or modifying project configurations in the control center files, depending on the task. 
   With each commit, PyPackIT's CI/CD pipelines
   automatically integrate the new changes into the repository, 
   performing various quality assurance and testing tasks, 
   while producing reports and artifacts for review.
4. **Review**: When the implementation is finished,
   PyPackIT automatically sends review requests to designated maintainers. 
   After review, PyPackIT's CI/CD pipelines merge the changes into the project's mainline, 
   updating all affected project components and documenting the entire development process. 
   If changes correspond to the library's public API, 
   a new release version is published along with
   automatically generated release notes and changelogs, 
   distributed to several online indexing repositories.


:::{figure} /_media/figure/workflow_dark.svg
:alt: PyPackIT Workflow
:class: dark-light themed
:align: center
:name: fig-workflow

PyPackIT's software development workflow.
Labeled arrows represent manual tasks performed by users: Report, Design, Commit, and Review.
All other activities are automated,
which fall into four main categories (issue management, version control, CI/CD, and CM/CR/CT),
spanning different stages of the software development life-cycle.
:::
:::{image} /_media/figure/workflow_light.svg
:class: hidden
:::


Moreover, PyPackIT also activates periodically on a scheduled basis,
executing CM/CR/CT pipelines that perform various maintenance and monitoring tasks 
on the repository and each released library version, 
sustaining the health of the software and its development environment. 
If an action is required, these pipelines automatically submit 
issue tickets (when manual implementation is needed)
and PRs (when an automatic fix is available but needs review), 
or directly apply updates to the project. 

Therefore, PyPackIT's comprehensive, dynamic, and highly customizable project skeleton 
and cloud-native development environment eliminate the need for project setup and configuration, 
enabling Python projects to immediately begin the actual implementation of software, 
even directly from the web browser. 
PyPackIT's automated development workflow greatly simplifies the software development process, 
limiting manual tasks to writing issue tickets, essential code, test cases, and minimal documentation, 
while other activities are automatically carried out on the cloud, 
consistently enforcing best practices throughout the software development life-cycle. 
Since these repetitive software engineering and management activities are 
the most common cause of problems in open-source software projects, 
their automation significantly improves product quality, 
while allowing developers to solely focus on the creative aspects of their project. 
PyPackIT thus greatly benefits open-source software engineering 
that is often faced with challenges regarding funding, time, and staffing, 
by accelerating development and 
enabling the consistent and reliable production of high-quality software 
with minimal cost and effort. 

:::{admonition} Getting Started
:class: seealso

If you can't wait to get started with PyPackIT,
skip to the [User Manual](#manual) for detailed instructions
on how to install and use PyPackIT in your project.
Otherwise, continue for a background review of the state of the art
and current challenges in open-source software development,
and how PyPackIT addresses them to elevate your project.
:::
