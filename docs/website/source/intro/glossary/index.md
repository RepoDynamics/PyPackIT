# Glossary

:::{glossary}
:sorted:

Action
  An [Action](https://docs.github.com/en/actions/sharing-automations/creating-actions/about-custom-actions)
  is a reusable application for the {term}`GHA` platform
  to perform specific tasks within an automated workflow.
  Actions can be written in JavaScript, Python, or as Docker containers
  and are used to encapsulate functionality such as running tests,
  deploying code, or managing infrastructure.
  Actions can be created by users or sourced from the [GitHub Marketplace](https://github.com/marketplace),
  where thousands of pre-built actions are available.
  By combining multiple actions, developers can define complex workflows
  for CI/CD pipelines and other automated tasks in a GitHub repository.

Anaconda.org
  [Anaconda.org](http://www.anaconda.org/)
  is a language-agnostic package hosting and management service
  by [Anaconda Inc.](http://anaconda.com/)
  for sharing [conda packages](https://docs.conda.io/projects/conda/en/stable/user-guide/concepts/packages.html)
  and [standard Python packages](https://docs.anaconda.com/anacondaorg/user-guide/packages/standard-python-packages/)
  in private and public repositories.
  Supporting multiple programming languages, it is a popular choice
  for publishing Python packages with non-Python dependencies,
  which are common in high-performance computing applications.
  Similar to {term}`PyPI` using {term}`pip`,
  Anaconda.org integrates with the {term}`conda` package manager, 
  allowing users to easily download and install packages 
  hosted on the platform using command-line tools.

CCA
  Continuous Configuration Automation (CCA)
  refers to the automated management and maintenance
  of configuration settings across IT infrastructure.
  It ensures that systems remain consistent, compliant,
  and aligned with predefined configurations while adapting to changes dynamically.
  CCA tools enable version-controlled, repeatable configuration changes,
  reducing manual effort and errors.
  By integrating with CI/CD pipelines, CCA supports scalability
  rapid deployments, and the enforcement of configuration policies in modern DevOps practices.

CM
  Continuous Maintenance (CM) is the ongoing process of updating,
  improving, and adapting software or systems to address evolving requirements,
  fix defects, and maintain performance and security.
  Unlike one-time maintenance tasks, CM
  is integrated into the software development life cycle,
  often leveraging automation tools and processes.
  It includes activities like patch management, refactoring,
  dependency updates, performance tuning, and responding to user feedback.
  CM ensures that software remains reliable, secure,
  and aligned with organizational or user needs over time, particularly in dynamic environments.

Conda
  [Conda](https://docs.conda.i) is an open-source package and environment manager
  for Python and other programming languages.
  It is designed to handle package dependencies, installations,
  and updates across platforms.
  Unlike {term}`pip`, conda manages both Python packages
  and non-Python dependencies, such as C libraries.
  It supports creating isolated virtual environments,
  allowing users to manage multiple projects with different dependencies.
  Conda is included with the [Anaconda](https://docs.anaconda.com/anaconda/)
  and [Miniconda](https://docs.anaconda.com/miniconda/) distributions,
  and works with repositories such as {term}`Anaconda.org` and {term}`conda-forge`.

conda-forge
  [conda-forge](https://conda-forge.org/) is a community-driven collection of recipes,
  build infrastructure, and packages for the {term}`conda` package manager.
  It provides a vast public repository of high-quality, up-to-date packages,
  many of which are not available in the [default Anaconda repository](https://repo.anaconda.com/pkgs/).
  Packages on conda-forge are automatically built
  and tested across multiple operating systems and architectures
  using Continuous Integration (CI) systems,
  and uploaded to the [conda-forge Anaconda channel](https://anaconda.org/conda-forge).
  It is a widely used source for Python and non-Python packages,
  especially in scientific computing and data science communities.

CR
  Continuous Refactoring (CR) is the practice of regularly and incrementally
  improving the internal structure of code without altering its external behavior.
  This process is integrated into the software development life cycle,
  ensuring that the codebase remains clean, maintainable, and scalable
  as new features are added or changes occur.
  CR focuses on reducing technical debt, improving performance,
  and enhancing readability, often following principles like the
  DRY (Don't Repeat Yourself) and SOLID principles.
  By addressing code quality iteratively, it minimizes the risk of
  large-scale rewrites and facilitates long-term development efficiency.

CT
  Continuous Testing is the practice of executing automated tests
  at every stage of the software development life cycle
  to provide rapid feedback on the health and functionality of the application.
  It integrates testing into CI/CD pipelines,
  ensuring that code changes are validated early and often.
  CT encompasses various types of tests, such as unit,
  integration, functional, performance, and security tests.
  Its goal is to identify defects as soon as they occur,
  reduce the risk of deployment failures,
  and maintain high software quality in agile and DevOps environments.

FOSS
  [Free and Open Source Software](https://en.wikipedia.org/wiki/Free_and_open-source_software) (FOSS)
  refers to software that is both free to use,
  modify, and distribute and whose source code is openly available.
  The "free" aspect emphasizes freedom rather than cost,
  granting users the rights to study, change, and improve the software.
  FOSS promotes collaboration, transparency, and innovation,
  often developed by distributed communities.
  Licenses like GNU General Public License (GPL), MIT, and Apache ensure these freedoms.
  Examples of FOSS include Linux, Python, and Firefox.
  It plays a critical role in software development
  by providing reusable tools and fostering a shared knowledge ecosystem.  

GHA
  [GitHub Actions](https://github.com/features/actions) (GHA)
  is an automation and cloud computing platform integrated into GitHub
  that enables developers to define workflows for building,
  testing, deploying, and managing projects.
  Workflows are defined using YAML files stored in a repository’s `.github/workflows` directory
  and can be triggered by events like commits, pull requests, or scheduled intervals.
  GHA supports a wide range of tasks through pre-built or custom actions,
  including CI/CD pipelines, automated code reviews, and deployment to cloud services.
  It integrates tightly with GitHub repositories, providing a scalable and flexible solution
  for automating development processes.

GHI
  [GitHub Issues](https://github.com/features/issues) (GHI)
  is a built-in {term}`ITS` within GitHub,
  used to document and manage tasks, bugs, feature requests,
  and other work items for a repository.
  Each issue serves as a discussion thread and can include labels,
  milestones, assignees, comments, and references to pull requests or commits.
  GHI supports project management workflows with features like Kanban-style project boards,
  templates, and automation through {term}`GHA`.
  It integrates seamlessly with GitHub’s version control system,
  making it a key tool for tracking and coordinating work in software development projects.

ITS
  An Issue Tracking System (ITS) is a software tool used to document,
  manage, and track issues, bugs, tasks, and feature requests throughout a project's life cycle.
  It enables teams to report problems, prioritize work, assign responsibilities, and monitor progress.
  Common features include categorization, tagging, status updates, comment threads,
  and integration with version control systems.
  Popular ITS tools include Jira, GitHub Issues, GitLab Issues, and Bugzilla.
  ITS platforms are essential for effective project management, fostering collaboration,
  and ensuring accountability in software development and other workflows.

Mamba
  [Mamba](https://mamba.readthedocs.io/) is a high-performance
  reimplementation of the {term}`conda` package manager in C++,
  as part of the {term}`conda-forge` ecosystem.
  It offers improved speed for resolving dependencies and installing packages
  while maintaining compatibility with the conda ecosystem.
  Mamba supports the same commands and functionality as conda,
  including managing environments and installing packages
  from repositories like {term}`Anaconda.org` and conda-forge.
  It also introduces efficient parallel downloads
  and optimized dependency resolution,
  making it particularly useful for users
  working with large or complex package environments.

OIDC
  [OpenID Connect](https://openid.net/connect/) (OIDC)
  is an identity layer built on top of the OAuth 2.0 protocol
  that enables secure authentication and authorization for web and mobile applications.
  OIDC allows applications to verify the identity of a user based on authentication
  performed by an identity provider and to obtain basic profile information about the user.
  Key features of OIDC include support for single sign-on (SSO), session management, 
  and compatibility with OAuth 2.0 for access delegation, making it a widely adopted standard 
  for identity management and user authentication in platforms such as
  [GitHub](https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect)
  and [PyPI](https://docs.pypi.org/trusted-publishers/).

PAT
  A [Personal Access Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) (PAT)
  is a secure, alphanumeric string used to authenticate a user
  to an application or service in place of a password.
  Commonly used in APIs and version control systems like GitHub,
  PATs allow granular access control by defining specific scopes or permissions,
  such as read-only access or write privileges to repositories.
  PATs enhance security by avoiding the direct use of passwords
  and can be easily revoked or regenerated if compromised.
  They are often used in automated workflows, scripts,
  or integrations requiring authenticated access.

PEP
  A [Python Enhancement Proposal](https://peps.python.org/) (PEP)
  is a formal document that outlines proposed changes, new features,
  or processes for the Python language and its ecosystem,
  serving as a reference for Python's development.
  PEPs are reviewed and approved by Python’s core developers
  and are a cornerstone of Python's open development model.
  Notable examples include [PEP 8](https://peps.python.org/pep-0008/) (style guide for Python code),
  [PEP 20](https://peps.python.org/pep-0020/) (The Zen of Python), and
  [PEP 440](https://peps.python.org/pep-0440/) (Version Identification and Dependency Specification).

pip
  [Pip](https://pip.pypa.io) is the default package manager for Python,
  maintained by {term}`PyPA`.
  It is a command-line tool, often included with Python distributions,
  and is essential for managing Python environments in software development workflows.  
  Pip can be used to download and install packages
  from source distributions and binary wheels available
  in online repositories such as {term}`PyPI`
  and version control systems like Git.

PR
  A Pull Request (PR) is a feature in distributed version control systems such as GitHub,
  which allows developers to propose changes to a codebase.
  It is created when a contributor pushes changes to a branch
  and requests their review and integration into the main or another target branch.
  PRs facilitate collaboration by enabling code reviews,
  discussions, and testing before merging.
  They often include a description of the changes, references to related issues, 
  and a summary of the intent or impact of the modification.
  PRs are a critical component of modern collaborative software development workflows.

PSF
  [Python Software Foundation](https://www.python.org/psf-landing/) (PSF)
  is a non-profit organization that manages the intellectual property rights
  for Python, oversees its licensing, and provides financial support
  for Python-related events and projects, such as PyCon conferences.
  It also fosters collaboration and education within the global Python community
  through grants, sponsorships, and outreach programs.

PyPA
  [Python Packaging Authority](https://www.pypa.io/) (PyPA)
  is a working group that maintains and develops tools, standards,
  and libraries for Python package management and distribution.
  PyPA oversees key projects such as {term}`pip` and {term}`setuptools`,
  and manages specifications like the
  [Python Packaging User Guide](https://packaging.python.org/en/latest/)
  and standards such as {term}`PEP` [517](https://peps.python.org/pep-0517/)
  and {term}`PEP` [621](https://peps.python.org/pep-0621/).

PyPI
  [Python Package Index](https://pypi.org/) (PyPI)
  is the official software repository for Python packages.
  Run by the {term}`PSF`, PyPI provides a centralized public platform
  to publish and share reusable software.
  It serves as the default package source for tools like {term}`pip`,
  enabling users to download and install packages
  directly into their Python environments.

Setuptools
  [Setuptools](https://setuptools.pypa.io/) is a Python library by {term}`PyPA`
  designed to facilitate the packaging, distribution, and installation of Python projects.
  It extends Python's standard distutils library,
  offering additional features such as dependency management,
  support for plugins, and creating Python package distributions
  like source archives and {term}`wheel`s.
  It is a core component of the Python packaging ecosystem
  and is widely used to prepare projects for distribution on repositories like {term}`PyPI`.

TOML
  [Tom's Obvious Minimal Language](https://toml.io) (TOML)
  is a human-readable configuration file format
  with support for hierarchical data structures,
  offering an alternative to formats like JSON and YAML.
  TOML files, such as Python's `pyproject.toml`,
  are commonly used in software projects
  to define configurations in a structured and machine-parsable format.
  [Learn TOML in Y Minutes](https://learnxinyminutes.com/docs/toml/)

Wheel
  [Wheel](https://packaging.python.org/en/latest/glossary/#term-Wheel) is the standard
  [binary distribution format](https://packaging.python.org/en/latest/specifications/binary-distribution-format/#binary-distribution-format)
  for Python packages, designed to expedite the installation process
  by eliminating the need for building packages from source.
  A wheel archive contains all the necessary files
  for a Python package, including compiled binaries for specific platforms if needed.
  As a platform-independent standard defined in [PEP 427](https://www.python.org/dev/peps/pep-0427/),
  wheels are widely supported by tools like {term}`pip`,
  replacing the older [Egg](https://packaging.python.org/en/latest/glossary/#term-Egg) format.
:::
