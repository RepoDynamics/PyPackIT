# Contributing Guidelines

Welcome to the {{project_name}} community!
We are excited to have you here, 
and grateful that you are considering contributing to this project! ❤️
{{project_name}} is a free and open-source software that evolves with the needs of its community,
and can only grow through the help of great users like you. 
So, thank you for your support and involvement; we appreciate everything you do!

Note:
> This project follows the [***All Contributors***](https://allcontributors.org/docs/en/specification) specifications; 
all contributors are acknowledged in the public documentation website and release notes. 

{{project_name}} can use your experience, feedback, and expertise in many different areas, 





We appreciate all contributions, from reporting bugs to implementing new features. 
If you're unclear on how to proceed after reading this guide, please contact us on Discord.

We welcome contributions from external contributors, and this document
describes how to merge code changes into this {{cookiecutter.repo_name}}. 


We love your input! We want to make contributing to this project as easy and transparent as possible, whether it's:

Reporting a bug
Discussing the current state of the code
Submitting a fix
Proposing new features
Becoming a maintainer


[GitHub Quickstart](https://docs.github.com/en/get-started)


## Reporting a Problem




## Getting Started

* Make sure you have a [GitHub account](https://github.com/signup/free).
* [Fork](https://help.github.com/articles/fork-a-repo/) this repository on GitHub.
* On your local machine,
  [clone](https://help.github.com/articles/cloning-a-repository/) your fork of
  the repository.

## Making Changes

* Add some really awesome code to your local fork.  It's usually a [good
  idea](http://blog.jasonmeridth.com/posts/do-not-issue-pull-requests-from-your-master-branch/)
  to make changes on a
  [branch](https://help.github.com/articles/creating-and-deleting-branches-within-your-repository/)
  with the branch name relating to the feature you are going to add.
* When you are ready for others to examine and comment on your new feature,
  navigate to your fork of {{cookiecutter.repo_name}} on GitHub and open a [pull
  request](https://help.github.com/articles/using-pull-requests/) (PR). Note that
  after you launch a PR from one of your fork's branches, all
  subsequent commits to that branch will be added to the open pull request
  automatically.  Each commit added to the PR will be validated for
  mergability, compilation and test suite compliance; the results of these tests
  will be visible on the PR page.
* If you're providing a new feature, you must add test cases and documentation.
* When the code is ready to go, make sure you run the test suite using pytest.
* When you're ready to be considered for merging, check the "Ready to go"
  box on the PR page to let the {{cookiecutter.repo_name}} devs know that the changes are complete.
  The code will not be merged until this box is checked, the continuous
  integration returns checkmarks,
  and multiple core developers give "Approved" reviews.

## How to contribute changes
- Clone the repository if you have write access to the main repo, fork the repository if you are a collaborator.
- Make a new branch with `git checkout -b {your branch name}`
- Make changes and test your code
- Ensure that the test environment dependencies (`conda-envs`) line up with the build and deploy dependencies (`conda-recipe/meta.yaml`)
- Push the branch to the repo (either the main or your fork) with `git push -u origin {your branch name}`
  * Note that `origin` is the default name assigned to the remote, yours may be different
- Make a PR on GitHub with your changes
- We'll review the changes and get your code into the repo after lively discussion!


## Checklist for updates
- [ ] Make sure there is an/are issue(s) opened for your specific update
- [ ] Create the PR, referencing the issue
- [ ] Debug the PR as needed until tests pass
- [ ] Tag the final, debugged version 
   *  `git tag -a X.Y.Z [latest pushed commit] && git push --follow-tags`
- [ ] Get the PR merged in


## Additional Resources
