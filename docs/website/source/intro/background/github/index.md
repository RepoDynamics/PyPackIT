(bg-gh)=
# GitHub

[GitHub](https://github.com) is the world’s leading cloud-based platform 
for version control and collaborative software development, 
built on top of **Git**. 
It provides an all-in-one solution for managing code repositories, 
collaborating with teams, and automating workflows, 
making it an essential tool for developers, organizations, 
and open-source communities alike. 
GitHub is widely used across industries due to its scalability, 
flexibility, and deep integration with modern development tools and cloud services.

Originally launched in 2008, GitHub revolutionized the way software is built 
by introducing social coding concepts, such as pull requests and issues, 
that simplify team collaboration. 
Over the years, it has evolved beyond version control 
to support a full range of software development lifecycle (SDLC) activities—including 
project management, CI/CD automation, documentation, community engagement, 
and static website hosting.
With more than 100 million developers working on over 500 million projects,
GitHub is the world's largest social coding platform 
as of November 2024 {cite}`GitHubOctoverse2024`.


(bg-gh-repo)=
## Repository

[GitHub repositories](https://docs.github.com/en/repositories) 
are the primary organizational units 
for storing, managing, and collaborating on projects within the GitHub ecosystem. 
A repository houses all project-related files, 
including source code, configuration files, documentation, and other resources.
It lays the foundation for the project's structure and workflows,
and sets the general tone for the entire development lifecycle.
Additionally, repositories serve as a version control hub, 
tracking every modification and providing a full history of changes. 
This capability ensures that teams can revert to earlier versions, 
manage conflicting updates, and maintain project integrity.

As one of the first steps in starting a new software project,
setting up a GitHub repository is a crucial part of the development process.
It includes [configuration](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings)
and [customization](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository) 
tasks such adding a [README file](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes),
[license](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository),
[funding options](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/displaying-a-sponsor-button-in-your-repository),
[citation file](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files),
[Open Graph image](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview),
and [keywords](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics) 
that help users better find the project through various
[search](https://docs.github.com/en/search-github/searching-on-github/searching-for-repositories)
and [filtering](https://docs.github.com/en/search-github/searching-on-github/searching-topics) options.
GitHub repositories also support advanced management [tools and features](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository)
that must be configured, as described in the rest of this section.


(bg-gha)=
## GitHub Actions

In November 2019, GitHub introduced
[GitHub Actions](https://github.com/features/actions) (GHA)—an
event-driven cloud computing platform
for execution of automated software 
[workflows](https://docs.github.com/en/actions/using-workflows/about-workflows)
on configurable virtual machines, in response to specific
[events](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows) 
{cite}`GitHubDevWorkflowAutoEcoBook, HandsOnGHA`. 

Shortly after its release, GHA became the most popular {term}`CI/CD` service on GitHub,
due to its generous free tier for public repositories, 
full integration with other GitHub features, 
and better hardware and software support compared to other services
{cite}`RiseAndFallOfCIinGH, OnUsageAndMigrationOfCITools, OnUseOfGHA`.
GHA supports matrix builds, allowing projects to be tested across multiple environments in parallel, 
ensuring greater reliability and compatibility.
Moreover, GitHub's comprehensive [REST](https://docs.github.com/en/rest)
and [GraphQL](https://docs.github.com/en/graphql) {term}`API`s
grant workflows full control of all repository components, 
enabling automation well beyond conventional CI/CD practices 
{cite}`DevPerceptionOfGHA, GitHubDevWorkflowAutoEcoBook`.
By automating repetitive tasks, GHA streamlines development workflows, 
reduces human error, and speeds up release cycles.

(bg-gha-workflow)=
### Workflows

[GHA workflows](https://docs.github.com/en/actions/using-workflows/about-workflows) 
are the backbone of the automation process. 
Defined using YAML configuration files and
stored in the repository at `.github/workflows`,
workflows outline the specific tasks and steps 
required to build, test, and deploy projects. 
These workflows are event-driven and can be triggered by various activities 
such as code pushes, pull requests, issue comments, or even scheduled cron jobs. 
This flexibility allows teams to automate 
virtually any aspect of their software development lifecycle.

Workflows are composed of one or more jobs, 
and each job consists of a series of steps. 
Jobs can run sequentially or in parallel, 
depending on how the workflow is configured. 
For example, a typical CI workflow might include 
jobs for code linting, running tests, and building deployment artifacts. 
With matrix builds, developers can test their applications 
across multiple environments, operating systems, 
or software versions, ensuring robust and reliable code.


(bg-gha-action)=
### Actions

An [Action](https://docs.github.com/en/actions/sharing-automations/creating-actions/about-custom-actions)
is a reusable application for the [GHA](#bg-gha) platform,
used to encapsulate arbitrary functionality such as running tests,
deploying code, or managing infrastructure.
By combining multiple actions as building blocks,
developers can easily define complex automation workflows.
[GitHub Marketplace](https://github.com/marketplace)
is an indexing service where thousands of pre-built actions 
from GitHub and other third-party vendors are freely available.
Users can also create and publish their own custom actions, using either
[Docker container](https://docs.github.com/en/actions/sharing-automations/creating-actions/creating-a-docker-container-action),
[JavaScript](https://docs.github.com/en/actions/sharing-automations/creating-actions/creating-a-javascript-action),
or [composite actions](https://docs.github.com/en/actions/sharing-automations/creating-actions/creating-a-composite-action)
that can use any programming language under the hood.


(bg-ghcs)=
## GitHub Codespaces

[GitHub Codespaces](https://github.com/features/codespaces) is a cloud-based development environment 
that allows developers to instantly start coding in a fully configured, containerized workspace. 
Integrated directly into GitHub, Codespaces eliminates the need for complex local setups 
by providing on-demand development environments that mirror production configurations.

A codespace is a development environment that's hosted on the cloud,
and is customizable through configuration files 
in a practice called Configuration-as-Code (cf. [Infrastructure-as-Code](#bg-iac)).
Codespaces leverages Visual Studio Code (VS Code), 
offering a familiar interface and support for 
extensions, themes, and custom settings. 
Developers can launch Codespaces directly from a repository, 
enabling them to begin contributing without needing 
to install dependencies or configure environments. 
This is particularly beneficial for onboarding new team members 
and open-source contributors, as it drastically reduces setup time.

Customization is a key feature of Codespaces. 
Teams can define [development container](https://containers.dev) configurations using `devcontainer.json` files, 
specifying the runtime environment, tools, and extensions required for the project. 
This ensures consistency across all development environments, 
preventing configuration drift and improving collaboration across teams.

GitHub Codespaces also integrates with GitHub Actions, 
enabling seamless automation of development workflows. 
Developers can switch between local and cloud-based environments without losing context, 
making it easier to contribute, review code, and run tests. 
While Codespaces offers free usage for public repositories, 
private repositories and larger resource allocations may require a paid subscription, 
with pricing based on compute and storage consumption.


(bg-ghi)=
## GitHub Issues

[GitHub Issues](https://github.com/features/issues) (GHI)
is a built-in {term}`ITS` within GitHub
serving as the core collaboration tool 
for user feedbacks and tracking progress.
It is used to report, document, and managing bugs, feature requests,
and all other development tasks for the project.
Each issue serves as a discussion thread and can include labels,
milestones, assignees, comments, and references to pull requests or commits 
(cf. [GitHub docs](https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues)).
GHI supports project management workflows 
with features like Kanban-style project boards,
customizable submission forms, and automation through [GHA](#bg-gha).
It integrates seamlessly with GitHub’s version control system,
making it a key tool for tracking and coordinating work in software development projects.

GHI and can be [configured](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository)
to provide a comprehensive ITS for the project
with customizable [issue forms](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms)
that enable the collection of machine-readable user inputs.
Developers can also define a set of [labels](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels)
to categorize issues, pull requests, and discussions.


(bg-gh-pull)=
## GitHub Pull Requests

Pull Requests (PRs) are a fundamental aspect of collaborative development on GitHub. 
They provide a structured way for developers to propose changes,
collaborate through feedback, and merge contributions into the main codebase. 
A pull request creates a dedicated discussion space for each proposed change, 
where team members can review the code, suggest improvements, 
and approve or request revisions.

GitHub Pull Requests also integrate with CI/CD pipelines, 
enabling automated checks to run before changes are merged. 
Status checks, such as automated tests and security scans, 
ensure that new code meets quality standards. 
The platform offers various merge strategies, including merge commits, 
squashing, and rebasing, giving teams flexibility in managing their project history. 
Draft pull requests allow developers to share work-in-progress code early, 
fostering early feedback and collaboration.


(bg-ghd)=
## GitHub Discussions

GitHub Discussions offers an organized space for community engagement 
and team collaboration beyond code-centric tasks. 
It provides a platform for asking questions, brainstorming ideas, 
and sharing knowledge in a threaded, forum-like format. 
Unlike issues, which are meant for actionable tasks, 
Discussions encourages open-ended conversations 
that build stronger project communities.

Discussion categories help organize discussions, 
making it easier for participants to find relevant threads.
The ability create polls and mark answers in Q&A threads 
improves knowledge sharing 
by highlighting the most helpful responses. 
GitHub Discussions can also convert discussions into issues 
when conversations evolve into actionable items, 
creating a seamless bridge between ideation and execution.


(bg-ghrt)=
## GitHub Repository Template

[GitHub repository templates](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository)
simplify setting up new projects 
by providing standardized, reusable starting points.
They enable users to easily [create new repositories](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template) 
based on pre-configured project skeletons
to reduce setup time and ensure that best practices 
are consistently followed.
Repositories created from a template inherit
the same branches, directory structure, 
and files from the template repository, 
while providing a clean slate to start a new project 
by excluding the entire git history.
Creating a repository from a template is thus similar to forking,
but with key differences:

- A new fork includes all tags and the entire commit history of the parent repository, 
  while a repository created from a template starts with a single commit.
- Commits to a fork don't appear in users' contributions graph, 
  while commits to a repository created from a template do.
- A fork can be a temporary way to contribute code to an existing project, 
  while creating a repository from a template starts an entirely new project.


(bg-ghp)=
## GitHub Pages

[GitHub Pages](https://pages.github.com/) is a free static website hosting service 
that allows users to deploy websites directly from a GitHub repository. 
Providing each repository with a free URL on GitHub's `github.io` domain
with the flexibility to configure custom domains,
GitHub Pages is an ideal platform for hosting project documentation websites. 
Integration with GHA enables automated website builds and deployments, 
making content updates seamless.


## GitHub Sponsors

[GitHub Sponsors](https://github.com/sponsors) is a program 
that allows developers and organizations to financially support 
open-source contributors and maintainers. 
It provides a seamless way for contributors 
to receive recurring or one-time funding directly through GitHub.

Contributors can create a [sponsorship profile](https://docs.github.com/en/sponsors) 
to highlight their work and funding needs. 
Sponsors can choose tiers offering benefits 
such as public recognition or exclusive updates. 
To make sponsoring easier, repositories can include a 
[`FUNDING.yml`](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/displaying-a-sponsor-button-in-your-repository) file, 
which adds a "Sponsor" button directly to the repository’s interface, 
linking to sponsorship platforms including GitHub Sponsors, [Tidelift](https://tidelift.com/), [Patreon](https://www.patreon.com/),
or any other platform of choice.

GitHub does not take a fee for sponsorships, 
ensuring that all contributions go to the intended recipient. 
While this program strengthens the open-source ecosystem, 
its focus on transparency and simplicity makes it a vital tool 
for sustaining widely used yet underfunded projects.


(bg-gh-writing)=
## Writing on GitHub

[GitHub-Flavored Markdown](#bg-gfmd) (GFM) 
is an extended version of Markdown 
designed specifically for [writing rich documents on GitHub](https://docs.github.com/en/get-started/writing-on-github), 
including [README files](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes),
[community health files](#bg-gh-health-files), 
issue tickets, pull requests, discussions, and project wikis.
GFM enhances standard Markdown by supporting features like tables, 
task lists, and syntax highlighting for code blocks.

Markdown content in GitHub is rendered to HTML, 
making it visually accessible in web browsers.
While HTML elements can be embedded 
within Markdown files for additional customization, 
not all HTML tags and features are supported.
GitHub performs additional post-processing and sanitization 
after rendering the contents to HTML,
removing unsupported elements (e.g., `<svg>`, `<inline>`)
and attributes (e.g., `class`, `style`).
JavaScript and CSS are explicitly excluded, 
which limits the creation of highly interactive or responsive documents. 
This restriction ensures security and uniformity across GitHub-hosted content 
but may make it challenging to achieve visually appealing designs.


(bg-gh-health-files)=
## Community Health Files

To help build and maintain a healthy and collaborative environment for open-source projects,
GitHub allows users to add certain 
[community health files](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file)
to their repositories.
When properly configured, links to these files are automatically displayed on the repository's homepage
and various other related pages, making them easily accessible to the community.
They include:
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
