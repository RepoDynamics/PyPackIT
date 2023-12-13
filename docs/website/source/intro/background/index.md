# Background


## Python

[Python](https://www.python.org/) is a general-purpose, multi-paradigm programming language,
created by Guido van Rossum and first released in 1991.[^python-timeline]
It has since evolved into one of the most popular programming languages in the world,
consistently ranking among the top five throughout the last decade, and topping the list since 2021,
according to the [TIOBE Index](https://www.tiobe.com/tiobe-index/).

[^python-timeline]: [G. van Rossum (2009). A Brief Timeline of Python. The History of Python](https://python-history.blogspot.com/2009/01/brief-timeline-of-python.html)

Python was designed with an emphasis on code readability and simplicity;
its high-level abstractions and straightforward syntax
have made software development accessible to a wider range of users,
while still being powerful and robust enough to support advanced applications.
Python is a dynamically typed, interpreted language, with automatic memory management,
which allows for rapid prototyping and implementation of complex concepts,
enabling users to readily develop their ideas and share them with others.

Owing to an active community of open-source developers, Python's rich ecosystem of libraries
and frameworks has grown exponentially over the years,
making it a powerful and versatile tool for a wide range of applications,
from web development, to data science, artificial intelligence, and machine learning.
Not only do large organizations like Google, NASA, and CERN use Python in many of their projects,
but it has also become the language of choice for many startups,
small businesses, and academic research groups.
For example, the majority of scientific software across various disciplines of computational sciences
are now being published as Python packages.


## GitHub

The growth of the Python ecosystem and its open-source libraries has been further accelerated
by the emergence of cloud-based platforms for version control systems (VCSs),
such as [GitHub](https://github.com),
which marked a significant shift in how software is developed, shared, and maintained.
Their purpose is to facilitate collaborative software development,
by providing a centralized location for storing code, tracking changes,
and managing contributions from multiple developers.
They are especially crucial for open-source projects,
where developers from various backgrounds contribute to a shared codebase,
and feedback from the community is an integral part of the development process.

GitHub, launched in 2008, has quickly risen to prominence
as the world's largest host of source code,
with more than 100 million developers working on over 372 million repositories,
as of November 2023.[^github-stats]
In addition to its user-friendly interface, GitHub offers an extensive set of features
that have solidified its position in the software development landscape, including:
- **Version Control**: At its core, GitHub provides git-based version control,
  enabling developers to track changes, revert to previous states,
  and manage different versions of their code efficiently.
- **Issue Tracking**: GitHub includes an issue tracking system that allows developers
  to report bugs, request features, and discuss improvements within the platform.
- **Collaboration Tools**: Features such as pull requests, code reviews, and branch management
  facilitate collaboration among developers, making it easier to contribute to and maintain projects.
- **Automation Tools**: GitHub allows for building continuous integration, deployment, and
  testing (CI/CD/CT) pipelines, enabling automatic testing, building, and deployment of software projects,
  directly from GitHub repositories and without the need for third-party platforms.
- **Web Hosting**: GitHub provides free web hosting for static websites stored in GitHub repositories,
  making it easier to publish documentation and other project-related content.
- **Integration**: GitHub can be readily integrated with various development tools and services,
  enhancing its utility in different stages of software development.

[^github-stats]: [GitHub (2023). Octoverse: The state of open source and rise of AI in 2023.](https://github.blog/2023-11-08-the-state-of-open-source-and-ai/)


## State of the Art

The Python programming language and its vibrant ecosystem have made software development
more accessible and efficient than ever before, enabling a diverse community of users,
from professional developers and researchers, to amateur programmers and enthusiasts,
to promptly implement their novel ideas and share their valuable work with the world.
In addition, the rise of comprehensive cloud-based services like GitHub has undeniably revolutionized
the software development process, making it easier to collaborate on projects and share code,
and streamlining the process of building, testing, documenting, deploying, and maintaining software.

However, despite these significant advancements, the current landscape of Python software development
is still not without its challenges; these render the goal of rapid development, publishing,
and maintenance of professional and effective Python software a non-trivial task,
particularly for smaller teams or projects that lack dedicated developers for each step of the process.

The following sections discuss several challenges in the current landscape of software development,
which often act as significant barriers to smaller development teams,
inadvertently hampering innovation and growth within the Python community.
The focus is on common tasks and chores that are an essential part of every software development process;
these are often repetitive, time-consuming and tedious tasks
that require a significant amount of effort and resources,
and a broad range of skills and expertise to perform correctly.
While being crucial for the successful development and maintenance of every software,
these tasks are not directly related to the idea and vision behind the project itself,
and are rather chores that can be automated and streamlined to save time and effort
for the development team, allowing them to solely focus on the creative aspects of their work.


### Repository Setup

As one of the first steps in starting a new software project,
setting up a GitHub repository is a crucial part of the development process;
it lays the foundation for the project's structure and workflows,
and sets the general tone for the entire development lifecycle.
The role of the repository extends far beyond just code hosting;
it often acts as the central headquarters for the project,
where the team members meet to lay out the roadmap,
contribute code, review each other's work, discuss issues and new ideas,
maintain the project, and plan for the future.
The repository also serves as the main storefront and the public face of the project,
where users can learn about the software and track its progress,
provide feedback, and contribute to its development.
Therefore, having a robust and professional GitHub repository is
one of the key requirements for a successful software project,
influencing its development and maintainability,
affecting its visibility and accessibility to potential contributors and users,
and ultimately, determining its overall adoption, growth, and longevity.

Considering the integral and multifaceted role of the GitHub repository in software projects,
setting up a professional and robust repository involves numerous steps,
and requires a broad range of knowledge and expertise,
not only on GitHub and its various features, configurations, and options,
but also on every aspect of software development and maintenance,
and a variety of other subjects, such as graphic design, user experience, security,
community and project management, and marketing.
Large and well-established organizations often have dedicated teams for each of these aspects,
who can work together to set up and maintain a professional repository for their projects.
However, for smaller teams or individual developers,
who may not have the necessary resources or expertise to perform these tasks,
this can be a daunting and time-consuming process,
involving a steep learning curve and a significant amount of effort and resources.

While several tools and resources are available
to help developers with some of the involved tasks in isolation,
to the best of our knowledge, there is currently no comprehensive solution
that can automate and streamline the entire process.
Therefore, developers still need to have a broad understanding of the various aspects involved,
to know which tools to use and how to configure them correctly,
and spend a significant amount of time and effort to find the right combination of tools and services,
only to be able to cover a small subset of the requirements.

The following is a list of some of the most important aspects that must be considered
when setting up a GitHub repository for a software project:

- [**Accessibility**]{.primary-color}: For a project to be successful,
  it must first be easily discoverable by its target audience.
  This is especially important for independent projects that do not have the backing of a large organization,
  where the repository acts as the first point of contact for potential users and collaborators.
  Developers can increase the visibility of their projects by adding an expressive description
  and a list of related [keywords](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics)
  (aka topics) to the repository, which are used by GitHub to categorize the project,
  and help users better find it through various
  [search](https://docs.github.com/en/search-github/searching-on-github/searching-for-repositories)
  and [filtering](https://docs.github.com/en/search-github/searching-on-github/searching-topics) options.
- [**Appearance**]{.primary-color}: The appearance of the repository is another important factor
  that can influence the first impression of potential users and collaborators.
  Next to the repository's description and keywords,
  its main [README file](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes),
  which is automatically displayed on the repository's homepage,
  is usually the first thing that users notice when they visit the repository.
  Acting as the front page of the repository,
  it is thus crucial to have an informative, engaging, and visually appealing README
  that captures the attention of visitors and provides them with a clear overview of the project.
  Ideally, a well-structured README should also include dynamic information,
  such as various statistics and status indicators that are automatically updated
  to reflect the current state of the project.
  However, GitHub requires READMEs to be written in
  [GitHub Flavored Markdown](https://github.github.com/gfm/),
  and performs additional post-processing and sanitization after rendering the contents to HTML,
  due to security concerns.
  This means that only a [limited subset of HTML features](https://docs.github.com/en/get-started/writing-on-github)
  are supported, with no support for CSS or JavaScript,
  which makes creating visually appealing and dynamic READMEs
  a non-trivial and challenging task for many developers.
  Another often neglected aspect is
  [adding a custom Open Graph image](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview)
  to the repository, to improve its appearance on platforms with [Open Graph](https://ogp.me/) support,
  such as social media and search engines.
- [**Structure**]{.primary-color}: The directory structure of the repository defines the layout
  and the overall organization of the project; it is an important factor that can have a significant impact
  on the development process and maintainability of the project.
  A well-structured repository should have a clear directory structure,
  with a logical separation between different components of the project,
  and a consistent and standardized naming scheme for files and directories.
  This makes it easier for developers to navigate the repository,
  locate the relevant files, and understand the overall structure of the project.
  In addition, GitHub and many other tools and services that are commonly used in the project development
  process rely on the repository's structure to locate and identify various components of the project.
  This requires developers to follow a specific directory structure and naming scheme
  when setting up their repositories, so that these tools can locate the relevant files and directories
  needed for their operation.
  Moreover, the repository structure is one of the first things that users notice when visiting the repository,
  and thus plays a vital role in establishing the project's credibility and professionalism.
- [**Security**]{.primary-color}: Security is a crucial aspect of software development,
  and should be considered at every stage of the development process.
  This is especially important for open-source projects,
  where the source code is publicly available and can be accessed by anyone.
  Therefore, implementing security measures and
  protocols for reporting and handling security issues in the repository
  is essential for ensuring software integrity and safeguarding the project against vulnerabilities.
  GitHub provides several [security features](https://docs.github.com/en/code-security/getting-started/github-security-features)
  that must be correctly configured to help developers
  identify, privately report, and fix potential security issues in their repositories,
  such as [code scanning](https://docs.github.com/en/code-security/code-scanning/introduction-to-code-scanning/about-code-scanning),
  [dependency review](https://docs.github.com/en/code-security/supply-chain-security/understanding-your-software-supply-chain/about-dependency-review),
  [secret scanning](https://docs.github.com/en/code-security/secret-scanning/about-secret-scanning),
  [security policies](https://docs.github.com/en/code-security/getting-started/adding-a-security-policy-to-your-repository),
  and [security advisories](https://docs.github.com/en/code-security/security-advisories/working-with-repository-security-advisories/about-repository-security-advisories).
  In addition, setting up various [branch protection rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
  for repository's release branches is another crucial security measure,
  safeguarding the main codebase and ensuring that changes are reviewed and tested before being merged.
  This practice, which is especially important
  for projects with multiple contributors and outside collaborators,
  not only maintains code quality but also fosters a disciplined development environment.
- [**License**]{.primary-color}: The license of a software project defines the terms and conditions
  under which the software can be used, modified, and distributed.
  It is an important aspect of software development, as it determines the legal status of the project,
  and can have a significant impact on its adoption and growth.
  A suitable license protects the rights of the creator while encouraging use and contribution from others.
  Therefore, it is crucial for developers to carefully choose a license that best suits their needs,
  and correctly [add it to the repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository#applying-a-license-to-a-repository-with-a-license-file)
  so that GitHub can automatically detect and display it on the repository's homepage,
  making it clear to users and collaborators
  under which terms they can use and contribute to the project.
- [**Maintenance**]{.primary-color}: Maintaining a software project is an ongoing process,
  which requires developers to regularly update the code and fix any issues that may arise.
  It is crucial to have a well-defined maintenance process in place,
  to ensure that the project is maintained in an effective and organized manner.
  An integral part of the development and maintenance process is the issue tracking system,
  where users and developers can report bugs, and request new features and other changes
  in the software and other components of the project.
  Professional repositories have a well-defined issue tracking system in place,
  with structured issue forms that guide contributors in providing the necessary details
  in a consistent standardized format.
  Equally important is a comprehensive labeling system to categorize and organize issues and pull requests.
  This makes it easier for maintainers to prioritize and manage issues,
  helps collaborators to find issues that they can contribute to,
  and facilitates efficient searching and tracking of the software's problems and progress by users.
  [GitHub Issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues)
  is a built-in feature that is available for all GitHub repositories,
  and can be [configured](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository)
  to provide a comprehensive issue tracking system for the project,
  with well-structured [issue forms](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms)
  that can be customized according to the needs of the project.
  Developers can also define a set of [labels](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels)
  for their GitHub repository, to categorize issues, pull requests, and discussions.
  Moreover, to further streamline the maintenance process,
  each issue form can be configured to automatically add a set of labels to the issue,
  along with a pre-defined set of assignees responsible for handling the issue.
- [**Support**]{.primary-color}: Maintaining a healthy and sustainable project
  involves more than just code management;
  providing support for users and contributors is another important aspect
  of software development, especially for open-source projects.
  It is crucial for developers to provide a clear and accessible way
  for the community to ask questions and discuss various topics related to the project, share their ideas,
  and participate in the decision-making process that shapes the future of the project.
  This can be achieved by adding a [GitHub Discussions](https://docs.github.com/en/discussions/collaborating-with-your-community-using-discussions/about-discussions)
  section to the repository, which provides a forum for community engagement and collaboration,
  fostering an environment where ideas, challenges, and solutions can be shared openly.
  It can be configured to organize discussions into various sections and categories,
  and add well-thought-out templates to each category to
  maintain a consistent and organized environment,
  and guide users on how to effectively participate in the discussions.
- [**Community**]{.primary-color}: Building a strong and vibrant community is an essential part
  of every project, as it fosters collaboration and innovation,
  and helps ensure the long-term sustainability of the project.
  To help build and maintain a healthy and collaborative environment for their open-source projects,
  GitHub allows developers to add a set of predefined [community health files](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file)
  to their repositories.
  When properly configured, links to these files are automatically displayed on the repository's homepage
  and various other related pages in the repository, making them easily accessible to the community,
  and ensuring that they are aware of the project's policies and guidelines. These files include:
  - [Code of Conduct](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/adding-a-code-of-conduct-to-your-project):
    Defining standards for how to engage in the community,
    expected behavior, and the consequences of violating these standards.
    It is an important aspect of community management, as it helps establish a safe and welcoming environment
    for all community members, and ensures that everyone is treated with respect and dignity.
  - [Contributing Guidelines](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/setting-guidelines-for-repository-contributors):
    Providing clear instructions and guidelines for how to contribute to the project,
    from opening issues for reporting bugs and requesting new features or changes,
    to implementing the code and submitting pull requests.
    This helps ensure that contributions are made in a consistent manner
    and are compatible with the project's workflow,
    thus saving time and effort for both the contributors and the maintainers.
  - [Security Policy](https://docs.github.com/en/code-security/getting-started/adding-a-security-policy-to-your-repository):
    Detailing the security disclosure policy of the project for users and security researchers/auditors,
    providing instructions on how to securely report security vulnerabilities in the project,
    clarifying the exact steps that are taken to handle and resolve the issue,
    and the expected response time.
  - [Support Resources](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/adding-support-resources-to-your-project):
    Providing information and resources on how to get help with the project,
    such as asking questions about the software,
    requesting clarifications and further information on various aspects of the project,
    reporting potential bugs and issues, and requesting new features or changes.
    This makes it easier for users to find the relevant resources,
    and helps reduce the number of duplicate issues and questions.
  - [Governance Model](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file#supported-file-types):
    Defining the governance model of the project, including the roles and responsibilities of the maintainers,
    the decision-making process, and the criteria for becoming a maintainer.
    This helps establish a clear and transparent governance model for the project,
    and provides a framework for the community to participate in the decision-making process.
- [**Funding**]{.primary-color}: Securing funding enables developers
  to dedicate more time and resources to their projects,
  and helps ensure the long-term sustainability of the project.
  This is especially an important challenge for independent open-source projects,
  where developers often rely on donations from users and sponsors to fund their work.
  GitHub allows projects to include [funding options](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/displaying-a-sponsor-button-in-your-repository)
  directly on their repository homepage, to increase their visibility and open avenues for financial support.
  Funding options can be configured for various platforms,
  including [GitHub Sponsors](https://docs.github.com/en/sponsors/getting-started-with-github-sponsors/about-github-sponsors),
  several pre-defined external platforms such as [Tidelift](https://tidelift.com/) and [Patreon](https://www.patreon.com/),
  and any other platform of choice.


### Code Quality and Testing

Code quality assurance and testing are crucial aspects of every software development process,
ensuring that the code is functional, secure, robust, reliable, maintainable, and sustainable.
These encompass a wide range of activities and practices, from formatting and static code analysis routines,
to various dynamic testing methods, such as unit testing, integration testing, and end-to-end testing:

- [**Formatting**]{.primary-color}: The Python interpreter imposes little to no restrictions
  on the formatting of the source code, such as naming conventions,
  annotations, indentation, line length, whitespace, and other layout and styling aspects.
  This can lead to vastly different formatting styles between developers,
  preventing them from easily following, reviewing, and maintaining each other's code.
  Therefore, it is important for developers to follow a consistent code style,
  especially in open-source collaborative projects, where the code is publicly available
  and the long-term sustainability of the project depends on the contributions from the community.
  Code formatting in Python has been greatly simplified by the introduction of
  a standardized style guide in the [Python Enhancement Proposal (PEP) 8](https://peps.python.org/pep-0008/),
  and the availability of powerful automated code formatting tools, such as
  [Black](https://github.com/psf/black) and [YAPF](https://github.com/google/yapf).
- [**Linting**]{.primary-color}: Static code analysis, also known as linting,
  is the process of analyzing the source code without actually executing it.
  It is usually the first line of defense in ensuring code quality,
  used to detect security vulnerabilities, syntax errors, suspicious constructs, and potential bugs;
  enforce styling rules; identify unused variables and imports, and perform various other checks.
  The Python ecosystem offers several powerful linting tools, such as
  [Pylint](https://github.com/pylint-dev/pylint), [Flake8](https://github.com/PyCQA/flake8),
  and [Bandit](https://github.com/PyCQA/bandit).
  More recently, [Ruff](https://github.com/astral-sh/ruff) has emerged as a rapidly growing
  and promising alternative, offering up to 100x performance improvement over existing tools.
  Written in Rust, Ruff not only introduces its own set of unique features,
  but also implements most functionalities of other linters and code formatters; as of version 0.1.7,
  Ruff can be used as a drop-in replacement for Flake8, Isort, and Black,
  while full parity with Pylint and Bandit is expected in the near future.
  More importantly, Ruff is able to automatically fix a number of issues it detects,
  in contrast to other linters that only report the issues and require manual intervention.
- [**Type Checking**]{.primary-color}: While Python is a dynamically typed language,
  it supports optional type annotations, as introduced in [PEP 484](https://www.python.org/dev/peps/pep-0484/).
  These can be extremely useful for documenting the code, and improving its readability and maintainability,
  especially in larger projects.
  More importantly, they can be used by type checking tools, such as [Mypy](https://github.com/python/mypy),
  which perform static code analysis to detect type-related errors in the code that may otherwise go unnoticed.
- [**Testing**]{.primary-color}: As one of the most important aspects of software development,
  dynamic testing refers to the process of executing the code with a given set of test cases
  to validate its functionality and correctness.
  As the complexity of software projects increases,
  it becomes increasingly difficult to ensure that the software behaves as expected in all possible scenarios,
  and that changes do not introduce new bugs or break existing functionalities.
  Therefore, it is crucial to have a comprehensive test suite in place,
  to ensure that the code is thoroughly tested and validated before being released.
  [Pytest](https://github.com/pytest-dev/pytest) is one of the most well-known testing frameworks
  for Python projects, allowing developers to write various types of tests for their software,
  including unit tests, integration tests, end-to-end tests, and functional tests.
  These can then be incorporated in the development workflows of the project,
  to ensure the integrity and functionality of the code at every stage of the development process.

While the Python ecosystem offers a comprehensive set of powerful tools to help developers
carry out these tasks, successfully integrating them into the development process
can be challenging and time-consuming, especially in the current rapidly evolving landscape:
Developers must maintain a broad and up-to-date overview
of the various tools and best practices involved,
to select the right set of tools for their project.
These tools usually offer a wide range of configuration options, which must be carefully set
to ensure that they are compatible with the project's workflow.
Integrating multiple tools, each with its own configuration and usage nuances,
into a single coherent workflow can be complex.
Ensuring that these tools work seamlessly together,
and with the project's existing infrastructure, requires significant setup and maintenance effort.
Additionally, balancing the strictness of rules
against the practicality of day-to-day development is a nuanced task.
More importantly, enforcing coding standards and testing practices
across all contributors can be challenging in collaborative projects.
It requires clear guidelines and often the implementation of automated checks
that are integrated into the development workflow,
such as pre-commit hooks or continuous integration pipelines.


### Documentation

Documentation is an essential aspect of software development,
weaving together the intricacies of code with the clarity of language,
and contributing significantly to the usability, maintenance, and longevity of projects.
Comprehensive documentation acts as a guide, explaining functionalities, providing examples,
and clarifying complex concepts, to ensure that users, regardless of their experience level,
can fully understand and effectively utilize the software.
Moreover, in a collaborative environment, clear documentation aids new contributors in maintaining the code;
it provides a reference to the current design and functionalities of the software,
making it easier to identify and fix issues, thereby speeding up the development process.

[Sphinx](https://www.sphinx-doc.org/),
a static site generator originally created for documenting the Python language itself,
is one of the most popular documentation tools in the Python ecosystem.
With features like automatic API documentation generation,
support for various output formats, and extensive customization through themes and extensions,
Sphinx is a powerful tool that can be used to create professional and user-friendly documentation websites.
However, versatility and flexibility often come at the cost of complexity;
the default website generated by Sphinx's quickstart tool is merely a bare-bones template
that still requires a significant amount of time and effort to become a fully functional, professional,
and user-friendly documentation site.
This demands a comprehensive knowledge of Sphinx's vast functionalities and configuration options,
along with a deeper understanding of web development tools and concepts, such as HTML, CSS, and JavaScript.
While a large number of pre-built themes and extensions are available to simplify this process,
utilizing them effectively still requires developers to be familiar with all the available options,
and know which ones to use and how to configure them correctly.

Even with a fully developed and well-designed layout at hand,
developers still need to spend a significant amount of time and effort
to write all the contents of the documentation website from scratch,
and carefully structure and organize them into a coherent and user-friendly format.
Moreover, since all the contents are by default static,
any changes to the project must be manually reflected in the documentation website.
This requires developers to maintain a detailed overview of all the places
where each piece of information is used,
and update them accordingly whenever necessary,
to ensure that the documentation stays up to date with the evolving project.

Deployment and web hosting are other critical aspects;
since the website is static, it must be rebuilt and redeployed
on the web hosting service after every change.
Integrating the documentation website with the version control system
and setting up continuous integration and deployment pipelines are thus crucial steps
that ensure that the documentation is consistently updated alongside changes.
While free web hosting services like [GitHub Pages](https://pages.github.com/)
and [Read the Docs](https://about.readthedocs.com/) provide convenient solutions
that can automate much of this process, they still require careful configuration
that can be challenging and time-consuming for many developers.

In summary, while a variety of powerful tools and services are available to help with creating
and hosting documentation websites, setting up and maintaining a professional,
comprehensive, and user-friendly website is still a non-trivial and time-consuming process.
Developers must possess a broad understanding of the various tools and aspects involved,
from choosing the right set of tools and configuring them correctly,
to writing the contents and structuring them into a coherent and user-friendly format.
While this process can be vastly standardized, automated and simplified,
to the best of our knowledge, there is currently no comprehensive solution
that can generate, deploy, and maintain a fully developed professional documentation website
with little to no effort from the developers.


### Development Workflow

:::{admonition} 🚧 Under Construction 🚧
:class: danger

This subsection is currently under construction.
:::

In addition, a well-structured repository should also have a clear and consistent workflow,
  and a well-defined process for reviewing and merging contributions.
  This helps streamline the development process,
  and makes it easier for new contributors to get started with the project.

- **Continuous Integration and Deployment**: Continuous integration and deployment (CI/CD) pipelines
  automate the process of building, testing, and deploying software,
  enabling developers to quickly and efficiently release new versions of their projects.
- [**Workflow**]{.primary-color}: The development workflow defines the exact process
  by which changes are made to the project, from the initial idea to the final implementation.
  It is crucial for developers to have comprehensive and well-defined workflows in place,
  to ensure that changes are made in a consistent and organized manner.
- **Branching Model**: The branching model of the repository must be designed
    to support the development workflow of the project.
    For example, the repository may follow a [Gitflow](https://nvie.com/posts/a-successful-git-branching-model/)
    branching model, where the `master` branch is used for stable releases,
    and the `develop` branch is used for development.
    Alternatively, it may follow a [GitHub Flow](https://guides.github.com/introduction/flow/)
    branching model, where the `master` branch is used for development,
    and releases are tagged from the `master` branch.


### Packaging and Distribution

For software to be usable by others,
it must first be [packaged](https://packaging.python.org/en/latest/overview/) in a standardized format
and distributed on an online software repository (aka package index),
which provides a centralized location for publishing and sharing packages,
so that users can find, download, and install it on their systems.
There are two major software repositories for Python packages:
- [Python Package Index (PyPI)](https://pypi.org/): The official software repository for Python,
  run by the [Python Software Foundation (PSF)](https://www.python.org/psf-landing/).
- [Anaconda.org](https://anaconda.org/): A language-agnostic platform
  with support for multiple programming languages, which makes it a popular choice
  for publishing Python packages with non-Python dependencies,
  as is often the case for scientific software.

Each of these platforms has its own package management system,
which is the software that users use to download and install packages from the repository:
- [pip](https://pip.pypa.io/en/stable/): The official package manager for Python,
  maintained by the [Python Packaging Authority (PyPA)](https://www.pypa.io/en/latest/),
  and the recommended tool for downloading, installing, and managing packages from PyPI.
- [conda](https://docs.conda.io/en/latest/)
  (and its more performant twin, [mamba](https://mamba.readthedocs.io/en/latest/)):
  Cross-platform package managers for Python and other programming languages,
  used to download, install, and manage packages from Anaconda.org.

The packaging and distribution process involves several steps:
1. The source code must first be structured into one or several
   [import packages](https://packaging.python.org/en/latest/glossary/#term-Import-Package),
   to ensure that it can be seamlessly imported and used by other Python projects.
   This requires developers to follow a specific directory structure and naming scheme,
   so that the package and its components can be correctly recognized
   by the package manager and the Python interpreter.

   For example, a typical Python application containing a single top-level import package
   has a hierarchical directory structure; the top-level directory must at least contain
   a special file called `__init__.py`, which is used to mark the directory as a package,
   and can be used to define a namespace and execute package initialization code.
   The name of this directory defines the import name of the package,
   and must adhere to the [naming conventions](https://www.python.org/dev/peps/pep-0008/#package-and-module-names)
   defined in PEP 8. All the source code of the package must be placed inside this directory,
   organized into subpackages and modules, which can be further nested to any depth.
2. A variety of instructions, requirements, and metadata must be provided
   in several configuration files, each with its own syntax and standardized format,
   to ensure that the package can be correctly built, recognized and installed by the package manager.
   These include:
   - [**Build System Specifications**]{.primary-color}: Instructions for the package manager
     on how to build and install the package from source, such as the build backend to use
     (e.g., [setuptools](https://setuptools.pypa.io),
     [hatch](https://hatch.pypa.io),
     [flit](https://flit.pypa.io),
     [poetry](https://python-poetry.org),
     [pdm](https://pdm-project.org)),
     additional build dependencies, and the commands to run.
     These must adhere to a standardized format defined in
     [PEP 517](https://www.python.org/dev/peps/pep-0517/) and
     [PEP 518](https://www.python.org/dev/peps/pep-0518/).
   - [**Build Backend Configurations**]{.primary-color}: Specific configurations
     for the selected build backend, such as the location of the source code,
     files to include/exclude, and how to handle different aspects of the build process.
     The exact format and syntax of these configurations depend on the selected build backend.
   - [**Name**]{.primary-color}: The name of the package on the online repository,
     used by the package manager to uniquely identify and locate the package.
     The package name must follow the [PyPA specifications](https://packaging.python.org/en/latest/specifications/name-normalization/)
     introduced in [PEP 503](https://peps.python.org/pep-0503/#normalized-names)
     and [PEP 508](https://peps.python.org/pep-0508/#names).
   - [**Version**]{.primary-color}: The version identifier of the package, used by the package manager
     to identify and install the correct version of the package.
     It must be a valid public version identifier according to the
     [PyPA specifications](https://packaging.python.org/en/latest/specifications/version-specifiers/#version-specifiers)
     first introduced in [PEP 440](https://www.python.org/dev/peps/pep-0440/),
     and must be incremented for every new release of the package,
     following [specific rules](https://packaging.python.org/en/latest/specifications/version-specifiers/#version-ordering-across-different-metadata-versions).
   - [**Python Version**]{.primary-color}: The minimum Python version required by the package,
     used by the package manager to ensure that the package is compatible with the user's Python interpreter.
     It must be a valid version specifier according to the
     [PyPA specifications](https://packaging.python.org/en/latest/specifications/version-specifiers/#id4),
     and must be incremented whenever the package drops support for older Python versions.
   - [**Dependencies**]{.primary-color}: The required and optional dependencies of the package
     (i.e., other software that the package depends on to function correctly),
     which are automatically installed by the package manager along with the package.
     These must be specified in a standardized format defined in
     [PEP 508](https://www.python.org/dev/peps/pep-0508/),
     and must be kept up to date and synchronized with the dependencies used in the source code.
   - [**Entry Points**]{.primary-color}: The entry points of the package,
     such as console scripts, GUI scripts, and other callable objects,
     which are automatically registered by the package manager and made available to the user.
     These must follow the [PyPA specifications](https://packaging.python.org/en/latest/specifications/entry-points/),
     and must refer to actual objects (e.g., functions) defined in the source code.

   In addition, several other metadata must be provided so that the online package index
   can correctly categorize and display the package, facilitating its discovery by users,
   and providing them with a clear overview of the project.
   These include:
   - [**Description**]{.primary-color}: A short description of the package,
     which is displayed on the package index and used by the package manager
     to provide a brief overview of the project.
   - [**Keywords**]{.primary-color}: A list of keywords describing the package,
     which are used by the package index to categorize the package,
     and help users find it through various search and filtering options.
   - [**License**]{.primary-color}: The license of the package,
     so that users can know under which terms they can use the project.
   - [**Authors and Maintainers**]{.primary-color}: Names and emails of the
     authors and maintainers of the package,
     so that users can know who is responsible for the project and how to contact them.
   - [**Project URLs**]{.primary-color}: A list of URLs related to the project,
     such as the project's homepage, documentation, source code, issue tracker, and changelog,
     which are displayed on the package index and used by the package manager
     to provide users with additional information and resources for the project.
   - [**Classifiers**]{.primary-color}: A list of [Trove classifiers](https://pypi.org/classifiers/)
     as defined in [PEP 301](https://peps.python.org/pep-0301/#distutils-trove-classification),
     to describe each release of the package (e.g., development status, supported Python versions and operating systems,
     project topics, intended audience, natural language, license, etc.).
     These standardized classifiers are used by the package index to categorize the package,
     and help users find it through various search and filtering options.
   - [**README**]{.primary-color}: A README file similar to the repository's README,
     containing a detailed and up-to-date description of the package,
     which is displayed on the package index to provide users with a clear overview of the project.
     As the first thing that users notice when viewing the project on the package index,
     it is crucial to have an informative, engaging, and visually appealing README
     that captures the attention of visitors and provides them with all the necessary information
     and resources for the project.
     Both PyPI and Anaconda.org support markup languages such as Markdown and reStructuredText
     for defining the contents of the README file.
     However, like GitHub, they impose several restrictions on the supported features,
     and perform additional post-processing and sanitization after rendering the contents to HTML.
     For example, PyPI uses the [Readme Renderer](https://github.com/pypa/readme_renderer) library
     to render the README file, which only supports a limited subset of HTML
     [tags](https://github.com/pypa/readme_renderer/blob/9c2eb81301bc230f2795cf7e6dc2c23f5815ea41/readme_renderer/clean.py#L20-L31)
     and [attributes](https://github.com/pypa/readme_renderer/blob/9c2eb81301bc230f2795cf7e6dc2c23f5815ea41/readme_renderer/clean.py#L33-L65).
     Since these do not completely overlap with the features supported by GitHub,
     a separate [PyPI-friendly README](https://packaging.python.org/en/latest/guides/making-a-pypi-friendly-readme/)
     must be provided for PyPI, to ensure that the contents are correctly rendered on the package index.
3. The import package(s) must be transformed into
   [distribution packages](https://packaging.python.org/en/latest/glossary/#term-Distribution-Package),
   which are versioned archives containing the import packages and other required files and resources.
   Distribution packages are the files that are actually uploaded to the online package index,
   to be downloaded and installed for the end-users via the package manager.
   There are two major distribution formats for Python packages:
   - [**Source Distributions**](https://packaging.python.org/en/latest/glossary/#term-Source-Distribution-or-sdist):
     Source distributions (aka sdist) are `tar.gz` archive files providing the source code of the package,
     along with the required configuration files, metadata, and resources
     that are needed for generating various built distributions.
   - [**Built Distributions**](https://packaging.python.org/en/latest/glossary/#term-Built-Distribution):
     Built distributions are [binary archives](https://packaging.python.org/en/latest/specifications/binary-distribution-format/)
     containing files and metadata that only need to be moved to the correct location on the target system,
     to be installed.
     Currently, PyPI/pip uses the [Wheel](https://packaging.python.org/en/latest/glossary/#term-Wheel) format
     (originally introduced in [PEP 427](https://www.python.org/dev/peps/pep-0427/),
     replacing the older [Egg](https://packaging.python.org/en/latest/glossary/#term-Egg) format),
     while Anaconda/conda uses the
     [`.conda` format](https://docs.conda.io/projects/conda/en/latest/user-guide/concepts/packages.html#conda-file-format)
     superseding the older `.tar.bz2` format.
     These can be either platform-independent or platform-specific,
     depending on whether the package is pure Python or contains compiled extensions
     (cf. [pure-Python wheels](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#pure-python-wheels) for pip,
     and [Noarch Packages](https://docs.conda.io/projects/conda/en/latest/user-guide/concepts/packages.html#noarch-packages) for conda).

   PyPA [recommends](https://packaging.python.org/en/latest/tutorials/packaging-projects/#generating-distribution-archives)
   always uploading a source distribution to PyPI,
   along with one or more built distributions for each supported platform.
   These can be generated using the [build](https://github.com/pypa/build)
   (for source distributions and pure-Python wheels)
   and [cibuildwheel](https://github.com/pypa/cibuildwheel) (for platform-specific wheels)
   packages provided by PyPA.
   Similarly, conda built distributions can be generated using the
   [conda-build](https://github.com/conda/conda-build) package provided by the [conda community](https://conda.org/).
4. The distribution packages must be uploaded to the online package index,
   so that users can find, download, and install them on their systems.
   - For PyPI, this requires developers to create an account on the platform,
     generate an API token for authentication,
     and use the [twine](https://github.com/pypa/twine/) library to upload the packages.
     Alternatively, [trusted publishing](https://docs.pypi.org/trusted-publishers/)
     ([OpenID Connect](https://openid.net/developers/how-connect-works/) standard) can be used
     in conjunction with the [PyPI publish GitHub Action](https://github.com/pypa/gh-action-pypi-publish)
     to publish packages directly from GitHub Actions, without the need for an API token.
   - Similarly, for Anaconda.org, developers must [create an account](https://docs.anaconda.com/free/anacondaorg/user-guide/work-with-accounts/)
     on the platform and use the [anaconda-client](https://github.com/Anaconda-Platform/anaconda-client) library
     to [upload the package](https://docs.anaconda.com/free/anacondaorg/user-guide/packages/conda-packages/#uploading-conda-packages)
     to their Anaconda.org repository/channel.
     However, distributing packages through personal repositories/channels is not recommended,
     as it requires users to manually add the repository/channel to their conda configuration,
     and does not provide any guarantees on the availability and reliability of the package.
     Instead, developers are encouraged to use the [conda-forge](https://conda-forge.org/)
     community repository, which provides a curated collection of high-quality packages
     that are automatically built and tested on a variety of platforms.
     Conda-forge has its own process for [contributing packages](https://conda-forge.org/docs/maintainer/adding_pkgs.html),
     which involves submitting a [conda-build recipe](https://docs.conda.io/projects/conda-build/en/stable/concepts/recipe.html)
     to the [staged-recipes repository](https://github.com/conda-forge/staged-recipes) on GitHub,
     where it is reviewed and tested by the community before being merged into the repository.
     Once merged, the package is automatically built and uploaded to the conda-forge channel,
     and made available to the users.

Correctly performing all these steps requires developers to have a comprehensive understanding
of the packaging and distribution process in the Python ecosystem,
and the various tools and best practices involved.
Since PyPI and Anaconda.org are independent platforms with their own package management systems,
developers must also be familiar with the specific requirements and nuances of each platform.
For example, most configurations and metadata for PyPI/pip must be provided
in a declarative fashion using the [TOML](https://toml.io) format in a file named
[`pyproject.toml`](https://packaging.python.org/en/latest/specifications/pyproject-toml/),
while Anaconda/conda uses the [YAML](https://yaml.org/) format to define metadata in a file named
[`meta.yaml`](https://docs.conda.io/projects/conda-build/en/stable/resources/define-metadata.html),
and requires [build scripts](https://docs.conda.io/projects/conda-build/en/stable/resources/build-scripts.html)
to be defined separately for Linux/macOS and Windows in `build.sh` and `bld.bat` files, respectively.
Moreover, due to the rapidly evolving standards in the Python ecosystem,
developers must constantly keep up to date with the latest changes
to ensure that their workflows are compatible with the current guidelines and best practices.
For example, the `pyproject.toml` file was first introduced
in 2016 in [PEP 518](https://www.python.org/dev/peps/pep-0518/),
and only established as a standard in 2021,
after the acceptance and implementation of
[PEP 621](https://www.python.org/dev/peps/pep-0621/) and
[PEP 660](https://www.python.org/dev/peps/pep-0660/),
to replace the older `setup.py` and
[`setup.cfg`](https://setuptools.pypa.io/en/latest/userguide/declarative_config.html) files.
In addition, since many of the packaging and distribution steps must be repeated for every release,
developers must maintain a detailed overview of the whole process and all the places
where each piece of information is used, and update them accordingly whenever necessary.
All these make the packaging and distribution process a time-consuming and error-prone task,
hampering the development process and slowing down the release cycle of the project.
Therefore, there is a need for a comprehensive solution that can automate and streamline
the entire packaging and distribution process, from start to finish,
to save time and effort for the developers, and ensure that the process is carried out correctly.


### Maintenance
:::{admonition} 🚧 Under Construction 🚧
:class: danger

This subsection is currently under construction.
:::

applying changes requires modifying multiple files at multiple locations.


## Summary

The rise of high-level, versatile programming languages, such as Python,
and the emergence of comprehensive cloud-based VCS platforms, such as GitHub,
have made software development more accessible and efficient than ever before.
Nevertheless, developing and maintaining a high-quality, useful, and sustainable software project
is still a non-trivial task, involving numerous steps
and requiring a broad range of skills and expertise in various other fields and subjects,
from graphic design and user experience, to project management and DevOps.
These often act as significant barriers to smaller independent projects
that lack dedicated teams for each aspect of the development process,
inadvertently hampering innovation and growth within the Python community.
While being crucial for the ultimate success of every project,
many aspects of the development process are not directly related
to the idea and vision behind the project itself,
and are rather repetitive, time-consuming and tedious chores
that can be automated and streamlined
to save time and effort for the development team,
allowing them to solely focus on the creative aspects of their work.
Although several tools and resources are available
to help developers with some of the involved tasks in isolation,
to the best of our knowledge, there is currently no comprehensive solution
that can seamlessly automate and streamline the entire software development process.
This underscores the need for a fully automated, plug-and-play software project management tool,
which enables aspiring and experienced developers alike to rapidly build professional software,
readily share them with the world, and effortlessly maintain their projects,
thereby empowering the development of open-source Python projects.
