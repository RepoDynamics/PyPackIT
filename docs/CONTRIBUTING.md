# Contributing Guidelines

<p align="justify">
Welcome to the **PyPACKIT** community!
We are excited to have you here, 
and grateful that you are considering contributing.
PyPACKIT is a free and open-source project that evolves with the needs of its users,
and can only survive and grow through the help of great members like you. 
So, thank you for your support and involvement; we appreciate all your work! 🙏❤️
</p>

> We Appreciate All Your Work ❤️🙏 \  
We follow the [***All Contributors***](https://allcontributors.org/docs/en/specification) specifications; 
all types of contributions are encouraged and valued, and 
all contributors are acknowledged on our [public website](https://.rtfd.io/about#contributors) 
and [repository](https://github.com/ArminAriam/PyPACKIT/releases).


To keep all documentation on our project organized and easy to find, 
the complete [contribution guide](docs/CONTRIBUTING.md) 
is hosted on our website. 

Following these guidelines helps to communicate that you respect the time of the developers managing and developing this open source project. In return, they should reciprocate that respect in addressing your issue, assessing changes, and helping you finalize your pull requests.



## Making Changes

* Add some really awesome code to your local fork.  It's usually a [good
  idea](http://blog.jasonmeridth.com/posts/do-not-issue-pull-requests-from-your-master-branch/)
  to make changes on a
  [branch](https://help.github.com/articles/creating-and-deleting-branches-within-your-repository/)
  with the branch name relating to the feature you are going to add.
* When you are ready for others to examine and comment on your new feature,
  navigate to your fork of {cookiecutter.repo_name} on GitHub and open a [pull
  request](https://help.github.com/articles/using-pull-requests/) (PR). Note that
  after you launch a PR from one of your fork's branches, all
  subsequent commits to that branch will be added to the open pull request
  automatically.  Each commit added to the PR will be validated for
  mergability, compilation and test suite compliance; the results of these tests
  will be visible on the PR page.
* If you're providing a new feature, you must add test cases and documentation.
* When the code is ready to go, make sure you run the test suite using pytest.
* When you're ready to be considered for merging, check the "Ready to go"
  box on the PR page to let the {cookiecutter.repo_name} devs know that the changes are complete.
  The code will not be merged until this box is checked, the continuous
  integration returns checkmarks,
  and multiple core developers give "Approved" reviews.

## How to contribute changes
- Clone the repository if you have write access to the main repo, fork the repository if you are a collaborator.
- Make a new branch with `git checkout -b <your branch name>`
- Make changes and test your code
- Ensure that the test environment dependencies (`conda-envs`) line up with the build and deploy dependencies (`conda-recipe/meta.yaml`)
- Push the branch to the repo (either the main or your fork) with `git push -u origin <your branch name>`
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
