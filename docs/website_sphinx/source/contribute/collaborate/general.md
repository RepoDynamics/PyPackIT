# General Procedure



[Clone](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) 
the repository:

git clone https://github.com/YOUR-USERNAME/Spoon-Knife


## General Development Cycle
Our "headquarters" is our [GitHub repository](https://github.com) 
(always accessible via the {fab}`github` icon on the top-right navigation bar), 
where we host, develop, manage and maintain our project, and communicate with each other.

:::{admonition} Get started with GitHub
:class: tip
If you are unfamiliar with [GitHub](https://github.com), 
please take a look at the [GitHub Documentation](https://docs.github.com/en) 
and read the [GitHub Quickstart](https://docs.github.com/en/get-started/quickstart). 
Don't forget to [create a free account](https://github.com/join).
:::

We have adopted the [GitHub flow](https://docs.github.com/en/get-started/quickstart/github-flow)
to [contribute to the project](https://docs.github.com/en/get-started/quickstart/contributing-to-projects), 
and use [GitHub Discussions](https://docs.github.com/en/discussions/quickstart) 
as the starting point for most of our 
[communications](https://docs.github.com/en/get-started/quickstart/communicating-on-github).
With a standardized workflow, almost all activities in {project_name} follow the same steps:
1. [**Start a new discussion**](): Regardless of whether we are a member of the core development team 
or a first-time contributor, when we think something should be fixed, changed, added, or removed,
or simply have a question, idea, announcement, or anything else we want to share with the community,
we start by creating a new discussion topic in the relevant category; 
for example, a discussion titled 'Graphical user interface (GUI)' in the 
[New Features](https://github.com/{github_user}/{github_repo}/discussions/categories/new-features) category, 
to discuss the idea of adding a GUI to the application.

2. [**Create a new issue**](): 

3. [**Create a development branch**](): 
4. [**Apply changes**](): After [cloning](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) 
the repository (or your fork of the repository) on your local machine, .
5. [**Create a pull request**]()
6. [**Test, review and merge changes**]():
7. [**Release a new version**]():

### Starting a Discussion

### Creating an Issue
After the community discusses the topic, if the consensus is that some
action is required, an [issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/quickstart) is 
[created from the corresponding discussion topic](https://docs.github.com/en/issues/tracking-your-work-with-issues/creating-an-issue#creating-an-issue-from-discussion). 
A maintainer is [automatically assigned](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms#top-level-syntax) 
to each opened issue, which can then also assign other volunteering contributors.

### Creating a Development Branch



The assignees then create a new branch from the repository's main branch,
to work on the issue. If you are a core developer (and thus have write access to the repository), you can
simply [create a new branch](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-and-deleting-branches-within-your-repository) 
in the project's repository. 
Otherwise, you must first [fork the repository](https://docs.github.com/en/get-started/quickstart/fork-a-repo),
and then create a new branch from the fork's main branch.

:::{admonition} For members with write access
:class: tip
If you are a core developer or maintainer of the project and thus have write access to the repository,
instead of forking the repository and creating a branch on your fork, you can instead directly create a 
new branch on the repository.
:::

:::{admonition} About Branches
:class: tip
Learn more about branches on [GitHub Documentation](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-branches)
:::


### Making Changes

We use [conventional commits](https://www.conventionalcommits.org/).

### Creating a Pull Request

Pull requests from forks can be created on the [GitHub web UI](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork)
but we use URls directly to load the correct template:

We advise you to regularly [sync your fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/syncing-a-fork)
with the main repository.

For core developers: [sync your branch](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/keeping-your-pull-request-in-sync-with-the-base-branch)