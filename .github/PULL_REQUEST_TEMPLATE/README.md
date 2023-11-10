# GitHub Pull Requests Templates
This directory contains additional templates for pull requests.

By default, the template defined at [./github/pull_request_template.md](./github/pull_request_template.md)
is used when opening a pull request. To use the extra templates in this directory,
the `template` [query parameter](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/using-query-parameters-to-create-a-pull-request)
must be added to the URL of the pull request form, defining the name of the template to use.
For example, to use a template file named `my_custom_template.md`, add the following query string at the end of the
URL: `?template=my_custom_template.md`. A full URL may e.g. look like this:
https://github.com/my-username/my-repo/compare/main...my-branch?template=my_custom_template.md

## Notes
- Pull request template filenames are not case-sensitive, and can have an extension such as `.md` or `.txt`.
- The YAML syntax used for issue forms is not supported for pull requests templates.

## References
- [GitHub Documentation](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository)
