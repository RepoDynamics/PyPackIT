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
milestones, assignees, comments, and references to pull requests or commits.
GHI supports project management workflows 
with features like Kanban-style project boards,
customizable submission forms, and automation through [GHA](#bg-gha).
It integrates seamlessly with GitHub’s version control system,
making it a key tool for tracking and coordinating work in software development projects.

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

