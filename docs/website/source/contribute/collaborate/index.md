---
sd_hide_title: true
---
# Collaborate
:::{toctree}
:hidden:

docs/index
dev/index
maintain/index
:::

You can {{pp_meta.name}} can use your help in many different ways; a few examples of
how {{pp_meta.name}} can appreciate from your experience, support, knowledge and expertise are:

So, thank you for your support and involvement; we appreciate all your work! 🙏❤️


Our community aspires to treat everyone equally and to value all contributions.
We have a Code of Conduct to foster an open and welcoming environment.


:::{admonition} Why should I read the contributing guidelines?
:class: tip
As most of us have surely experienced,
maintaining a free and open-source project is not a trivial task,
and the need for coordination between different contributors who
are not all in contact with each other adds another layer of complexity to the job.
To value every volunteer's time and efforts, we have devised detailed instructions
for how to join the conversation and become a part of the community.
These guidelines aim to standardize the development and maintenance process,
so that a large portion of the pipeline can be automated.
By following these instructions, you ensure that you and every other member
is making the most out of their time and efforts.
:::



If you are new to contributing to open-source projects,
we also recommend reading the [Open Source Guides](https://opensource.guide),
particularly: [How to Contribute to Open Source](https://opensource.guide/how-to-contribute/).


## Become a Collaborator
* writing code; fixing bugs, improving performance and quality, and adding new features
* adding examples and tutorials to the documentation
* proofreading, editing and writing documentation


It starts by describing the general development cycle of the project,
followed by detailed instructions for different types of contributions.
If you are interested in becoming an active member or a maintainer of the project,
we strongly advise you to read all sections chronologically. Otherwise,
you can read the general notes and then
head down to the section addressing the type of contribution you want to make
(see left sidebar), for example reporting a problem or contributing code.


## License and Copyright
{{pp_meta.name}} is licensed under the {{pp_meta.project.license.fullname}}.
In essence, this means that any contribution you make, such as code, media, and documents,
will also be under the same copyleft license, and free to use, modify and distribute to everyone.
You are thus responsible to make sure that you own the rights to your contribution,
or that the material you are contributing is under a license that allows this.
If you have any doubts or concerns, please feel free to [contact us](../../help/contact/index.md).

:::{button-ref} /about/license
:color: danger
:expand:

Read our full license
:::

## Development Cycle
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
With a standardized workflow, almost all activities in {project_name} follow the same steps.

Also have a look at GitHub documentation on [planning and tracking tools](https://docs.github.com/en/issues/tracking-your-work-with-issues/planning-and-tracking-work-for-your-team-or-project)
.

Also have a look at GitHub documentations on [communicating](https://docs.github.com/en/get-started/quickstart/communicating-on-github)
and [socializing](https://docs.github.com/en/get-started/quickstart/be-social) on GitHub.


Fork repo ABC
Clone it locally (git clone git@github.com:jmeridth/jekyll.git)
Add upstream repo (git remote add upstream git@github.com:mojombo/jekyll.git)
Create a feature/topic branch (git checkout -b awesome_feature)
Code fix/feature
don’t forget to add tests/specs and make sure they pass
Commit code on feature/topic branch (git add . && git commit -m “awesome”)
Checkout master (git checkout master)
Pull latest from upstream (git pull upstream master)
Checkout feature/topic branch (git checkout awesome_feature)
Rebase your changes onto the latest changes in master (git rebase master)
Push your fix/feature branch to your fork (git push origin awesome_feature)


### Create a Discussion
Regardless of whether we are a member of the core development team
or a first-time contributor, when we think something should be fixed, changed, added, or removed,
or simply have a question, idea, announcement, or anything else we want to share with the community,
we start by creating a new discussion topic in the relevant category;
for example, a discussion titled 'Graphical user interface (GUI)' in the
[New Features](https://github.com/{github_user}/{github_repo}/discussions/categories/new-features) category,
to discuss the idea of adding a GUI to the application.

### Create an Issue

Before creating an issue, you have to make sure the issue
### Bug

First, there are two thing you have to make sure of:
1. What you are experiencing is actually a bug in the application, and not the intended behavior,
or the result of not following the instructions.
2. The bug has not yet been fixed or reported by anyone else.

Additionally,

1. Create a new virtual environment on your machine. This provides an isolated environment to
ensure that the bug is indeed caused by our application.
2. [Download and install] the latest development version directly from our repository into the new environment.
3.

#### Verify the bug

#### Make sure the bug still exists
After verifying the bug, you have to make sure that it has not yet been fixed or reported.
To do so, we highly recommend the following steps:

[Search in Discussions](https://docs.github.com/en/issues/tracking-your-work-with-issues/filtering-and-searching-issues-and-pull-requests)
and [in issues and pull requests](https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests)
with several different keywords to make sure the issue has not already been reported.


[creating an issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/creating-an-issue).
After the community discusses the topic, if the consensus is that some
action is required, an [issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/quickstart) is
[created from the corresponding discussion topic](https://docs.github.com/en/issues/tracking-your-work-with-issues/creating-an-issue#creating-an-issue-from-discussion).
A maintainer is [automatically assigned](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms#top-level-syntax)
to each opened issue, which can then also [assign other volunteering contributors](https://docs.github.com/en/issues/tracking-your-work-with-issues/assigning-issues-and-pull-requests-to-other-github-users).



### Create a Branch
Clone the repository if you have write access to the main repo, fork the repository if you are a collaborator.
Make a new branch with `git checkout -b <your branch name>`

When you are assigned to an issue create a development branch
1. If you are not a core developer of the project (and thus don't have write access to this repository),
[fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo) this repository first.
2. On your fork (or on this repository when you are a core developer),
create a new branch from the **main** branch

[Clone](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)
the repository.


If you have write access, you can also
[directly create a branch from the issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/creating-a-branch-for-an-issue#creating-a-branch-for-an-issue)


Naming rules for branches:

Other than the 'main' branch, we have the following types of branch names:
* `release/v[0-9]+`: Release branches for each past major version, e.g. `release/v1` is created when
version `2.0.0` is released.
* `dev/(app|docs|test|ops)/[0-9]+`: Development branches for applying changes, e.g. `dev/app/11`.




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

The branch must be named: dev-{issue number} (for example: dev-11)

:::{admonition} About Branches
:class: tip
Learn more about branches on [GitHub Documentation](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-branches)
:::

### Commit Changes

After [cloning](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)
the repository (or your fork of the repository) on your local machine, .

We use [conventional commits](https://www.conventionalcommits.org/).

Use pre-commit hooks.

Run tests. When the code is ready to go, make sure you run the test suite using pytest.

If you're providing a new feature, you must add test cases and documentation.

Ensure that the test environment dependencies (`conda-envs`) line up with the build and deploy dependencies (`conda-recipe/meta.yaml`)

Ensure the code style and formatting by running black and isort.

Push the branch to the repo (either the main or your fork) with `git push -u origin <your branch name>`
* Note that `origin` is the default name assigned to the remote, yours may be different

### Create a Pull Request

When you are ready for others to examine and comment on your new feature,
  navigate to your fork of {{pp_meta.repo.name}} on GitHub and open a [pull
  request](https://help.github.com/articles/using-pull-requests/) (PR).

There are many ways to [create pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request)
.

Pull requests from forks can be created on the [GitHub web UI](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork)
but we use URls with [query parameters](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/using-query-parameters-to-create-a-pull-request)
to directly load the correct template:

We advise you to regularly [sync your fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/syncing-a-fork)
with the main repository.

For core developers: [sync your branch](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/keeping-your-pull-request-in-sync-with-the-base-branch)

Note that after you launch a PR from one of your fork's branches, all
subsequent commits to that branch will be added to the open pull request
automatically.  Each commit added to the PR will be validated for
mergability, compilation and test suite compliance; the results of these tests
will be visible on the PR page.

Don't forget to [link the pull request to the corresponding issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue).
If you are a maintainer, you can do this either from the
[pull request sidebar](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue#manually-linking-a-pull-request-to-an-issue-using-the-pull-request-sidebar)
or the corresponding [issue sidebar](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue#manually-linking-a-pull-request-or-branch-to-an-issue-using-the-issue-sidebar).
Otherwise, [use a keyword](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue#linking-a-pull-request-to-an-issue-using-a-keyword)
in your pull request (e.g. Resolves #11).

When you're ready to be considered for merging, check the "Ready to go"
box on the PR page to let the {{pp_meta.repo.name}} devs know that the changes are complete.
The code will not be merged until this box is checked, the continuous
integration returns checkmarks,
and multiple core developers give "Approved" reviews.


### Review and Merge Pull Request

### Publish New Release
*  `git tag -a X.Y.Z [latest pushed commit] && git push --follow-tags`
