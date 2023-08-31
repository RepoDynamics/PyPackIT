# Security Measures

{{pp_meta.name}} uses GitHub's [repository security advisories](https://docs.github.com/en/code-security/security-advisories/repository-security-advisories/about-repository-security-advisories)
feature to privately report, discuss, manage, and fix potential security vulnerabilities in the project.
These include vulnerabilities in our published software and deployed websites and applications,
as well as the repository itself (i.e. GitHub Actions, CI/CD workflows, repository settings etc.).

Since the [private vulnerability reporting is enabled](https://docs.github.com/en/code-security/security-advisories/repository-security-advisories/configuring-private-vulnerability-reporting-for-a-repository#enabling-or-disabling-private-vulnerability-reporting-for-a-repository)
for the repository, anyone can [report a vulnerability](../../feedback/report/security.md).

Everyone is encouraged to conduct vulnerability discovery research
and report potential security vulnerabilities, following our [vulnerability disclosure policy](../../feedback/report/security.md#vulnerability-disclosure-policy)).

Maintainers, especially the vulnerability management team, must make sure that they have [enabled notifications for private vulnerability reporting](https://docs.github.com/en/code-security/security-advisories/repository-security-advisories/configuring-private-vulnerability-reporting-for-a-repository#configuring-notifications-for-private-vulnerability-reporting).

:::{admonition} Our Policy
:class: important
{{pp_meta.name}} has a clear response policy and disclosure policy;
when a report has been submitted by a third party, the vulnerability management team must
acknowledge receiving the report within one week,
and maintain a transparent and open dialogue with the reporter, until the issue is resolved.
We also follow a 120-day disclosure timeline, meaning that the reporting researcher is allowed to
publicly disclose the vulnerability after 120 days. Since most of this time is required to provide users
enough time to update their applications and protect themselves, the vulnerability issue should be resolved
as soon as possible, ideally within the first 30 days.
:::

After a vulnerability report has been submitted, a private discussion and assessment must take place
by the vulnerability management team to [process the reported vulnerability](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing/managing-privately-reported-security-vulnerabilities).

If the reported vulnerability is verified, a [temporary private fork](https://docs.github.com/en/code-security/security-advisories/repository-security-advisories/collaborating-in-a-temporary-private-fork-to-resolve-a-repository-security-vulnerability)
must be created to work on the issue.

When the [issue is resolved](https://docs.github.com/en/code-security/security-advisories/repository-security-advisories/collaborating-in-a-temporary-private-fork-to-resolve-a-repository-security-vulnerability#adding-changes-to-a-temporary-private-fork)
and the [fix is reviewed](https://docs.github.com/en/code-security/security-advisories/repository-security-advisories/collaborating-in-a-temporary-private-fork-to-resolve-a-repository-security-vulnerability#creating-a-pull-request-from-a-temporary-private-fork)
, the [fork is merged](https://docs.github.com/en/code-security/security-advisories/repository-security-advisories/publishing-a-repository-security-advisory)
into the repository's main branch. This must be immediately followed by publishing a new patch release
(in case a published application was affected) and/or deploying the fix to the production environment
(in case an online service was affected), and publishing a security advisory to notify all users.
Publish the security advisory both on our [GitHub repository](https://docs.github.com/en/code-security/security-advisories/repository-security-advisories/publishing-a-repository-security-advisory)
and our website (Create a new blog post in the News section, under the "Security Advisory" category).
Don't forget to [add all collaborators](https://docs.github.com/en/code-security/security-advisories/repository-security-advisories/adding-a-collaborator-to-a-repository-security-advisory) to the advisory.
