# Issue Tracking System

Issue and discussion forms of your repository (defined in the control center) are completely dynamic.
For example, they contain dropdown menus for the user to select the package version, Python version,
operating system, and other specifications relevant to the issue.
Instead of hard coding these specifications in the forms, which would require you to manually
update them every time there is a change (e.g. when a new package version is released, or when support
for a specific Python version or operating system is added or removed),
${{ name }} uses its templating mechanism to dynamically reference the corresponding specifications.


The following is a simplified example of one of ${{ name }}'s main workflows:

Every time a new issue is opened in your repository, ${{ name }} automatically
processes the issue and reformats the text into a pre-defined style,
to ensure consistency and readability across all issues in your repository.
It also adds a comment to the issue, which tracks its status,
and is automatically updated whenever there is a progress.
Moreover, based on the contents of the issue, it is automatically assigned to a defined maintainer,
and tagged with various labels that indicate the type and status of the issue,
along with its target branches and package versions.
The assigned maintainer can then triage the issue and change its status label accordingly.

For example, if the issue is labeled as accepted,
${{ name }} automatically creates a new development branch from each of the issue's target branches,
and transforms the issue into draft pull requests for each of the development branches.
Subsequently, every time changes are applied to one of the development branches,
${{ name }} automatically detects the type of changes, and runs the appropriate linting,
formatting, and testing workflows, applying the necessary fixes and updates to the branch,
while generating comprehensive reports that can be easily tracked through the draft pull request.
Furthermore, depending on the type of changes,
${{ name }} automatically publishes developmental versions of your package on TestPyPI,
and generates previews of your documentation website throughout the development process.

Finally, when a development branch is marked as complete, ${{ name }} automatically
removes the draft status from the corresponding pull request,
adds a summary of all applied changes, and requests reviews from the assigned maintainers.
Once the pull request is approved, the reviewers can label the pull request as final,
or as a pre-release (alpha, beta, or release candidate)
in case of pull requests that correspond to a new package version.
For example, if the pull request is for a new package version and is labeled as final,
${{ name }} automatically merges the pull request into the corresponding release branch,
updates all relevant changelogs, calculates the new version and adds a version tag to the release branch,
builds the package and publishes it on PyPI, creates a new release on GitHub,
and generates a new version of the documentation website and deploys it on GitHub Pages,
with added release notes and an announcement of the new release.
