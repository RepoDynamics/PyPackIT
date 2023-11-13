# CI

## Code scanning
Instead of the [now deprecated](https://github.blog/2022-08-15-the-next-step-for-lgtm-com-github-code-scanning/)
[LGTM](https://github.com/apps/lgtm-com) app, we use [GitHub code scanning](https://docs.github.com/en/code-security/code-scanning),
which uses the same [CodeQL](https://docs.github.com/en/code-security/code-scanning/automatically-scanning-your-code-for-vulnerabilities-and-errors/about-code-scanning-with-codeql)
analysis technology as LGTM.
The code scanning is [integrated](https://docs.github.com/en/code-security/code-scanning/automatically-scanning-your-code-for-vulnerabilities-and-errors/configuring-code-scanning-for-a-repository)
into the CI workflow, and can be easily [customized](https://docs.github.com/en/code-security/code-scanning/automatically-scanning-your-code-for-vulnerabilities-and-errors/customizing-code-scanning).
Action: https://github.com/github/codeql-action/


##
