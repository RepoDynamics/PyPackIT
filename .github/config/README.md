# CI/CD Configurations
This directory contains configuration files for other workflows.
The following is a description of each file in this directory.

## [`labeler.yaml`](./github_labeler.yaml)
Configurations for the GitHub Actions workflow [PR Labeler](../workflows/_pr_labeler.yaml).
The workflow labels pull requests based on the paths of the affected files.
This config file contains the defined mapping between the labels and corresponding filepaths.
### References
[GitHub Actions: Labeler](https://github.com/actions/labeler)
