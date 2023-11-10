# GitHub Actions Workflows
This directory contains [workflows](https://docs.github.com/en/actions/using-workflows/about-workflows)
used in the CI/CD operations of the repository.

## [docs_rtd_pr_preview](_docs_rtd-pr-preview.yaml)
https://docs.readthedocs.io/en/latest/pull-requests.html
https://docs.readthedocs.io/en/latest/guides/pull-requests.html

## Releases
GitHub has [built-in functionality](https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes)
to automatically generate release notes.

## Used Actions

### setup-python
https://github.com/marketplace/actions/setup-python

### setup-micromamba
https://github.com/mamba-org/setup-micromamba
replacing [provision-with-micromamba](https://github.com/mamba-org/provision-with-micromamba)

## Syntax

### on: schedule: cron
schedule : https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule
cron tasks: https://pubs.opengroup.org/onlinepubs/9699919799/utilities/crontab.html#tag_20_25_07

## References
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

## Useful Links
- [Workflow security: `pull_request` vs `pull_request_target`](https://securitylab.github.com/research/github-actions-preventing-pwn-requests/)
