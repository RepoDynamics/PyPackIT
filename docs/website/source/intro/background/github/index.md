(bg-gh)=
# GitHub


(bg-gha)=
## GitHub Actions

In November 2019, GitHub introduced
[GitHub Actions](https://github.com/features/actions) (GHA)—an
event-driven cloud computing platform
for execution of automated software development 
[workflows](https://docs.github.com/en/actions/using-workflows/about-workflows)
on configurable virtual machines, in response to specific
[events](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows) 
{cite}`GitHubDevWorkflowAutoEcoBook, HandsOnGHA`. 

Shortly after its release, GHA became the most popular {term}`CI/CD` service on GitHub,
due to its generous free tier for public repositories, 
full integration with GitHub, 
and better hardware and software support compared to other services
{cite}`RiseAndFallOfCIinGH, OnUsageAndMigrationOfCITools, OnUseOfGHA`.
Moreover, GitHub's comprehensive [REST](https://docs.github.com/en/rest)
and [GraphQL](https://docs.github.com/en/graphql) {term}`API`s
grant workflows full control of all repository components, 
enabling automation well beyond conventional CI/CD practices 
{cite}`DevPerceptionOfGHA, GitHubDevWorkflowAutoEcoBook`.



GHA supports a wide range of tasks through pre-built or custom actions,
including CI/CD pipelines, automated code reviews, and deployment to cloud services.
It integrates tightly with GitHub repositories, providing a scalable and flexible solution
for automating development processes.


(bg-gha-workflow)=
### Workflows


Workflows are defined using YAML files stored in a repository’s `.github/workflows` directory
and can be triggered by events like commits, pull requests, or scheduled intervals.


[GitHub Actions workflows](https://docs.github.com/en/actions/using-workflows/about-workflows)


(bg-gha-actions)=
### Actions

To facilitate GHA workflow development,
GitHub allows reusable components called
[actions](https://docs.github.com/en/actions/creating-actions/about-custom-actions),
which act as building blocks for workflows, similar to software libraries. 
Developers can host actions on public GitHub repositories and publish them on 
[GitHub Marketplace](https://github.com/marketplace),
an indexing service allowing users to search for suitable options.


(bga-ghrt)=
## Repository Template

https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository

