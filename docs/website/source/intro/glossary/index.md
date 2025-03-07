# Glossary

:::{glossary}
:sorted:

API
  Application Programming Interface.

CI/CD
  Aggregation of Continuous Integration, Delivery, and Deployment,
  as part of [Continuous software engineering](#bg-continuous) practices.
  CI/CD is also often used as an umbrella term for Continuous methodologies in general.

CM
  Continuous Maintenance (CM) is the ongoing process of updating,
  improving, and adapting software or systems to address evolving requirements,
  fix defects, and maintain performance and security.
  Unlike one-time maintenance tasks, CM
  is integrated into the software development life cycle,
  often leveraging automation tools and processes.
  It includes activities like patch management, refactoring,
  dependency updates, performance tuning, and responding to user feedback.
  CM ensures that software remains reliable, secure,
  and aligned with organizational or user needs over time, particularly in dynamic environments.

CR
  Continuous Refactoring (CR) is the practice of regularly and incrementally
  improving the internal structure of code without altering its external behavior.
  This process is integrated into the software development life cycle,
  ensuring that the codebase remains clean, maintainable, and scalable
  as new features are added or changes occur.
  CR focuses on reducing technical debt, improving performance,
  and enhancing readability, often following principles like the
  DRY (Don't Repeat Yourself) and SOLID principles.
  By addressing code quality iteratively, it minimizes the risk of
  large-scale rewrites and facilitates long-term development efficiency.

CT
  Continuous Testing is the practice of executing automated tests
  at every stage of the software development life cycle
  to provide rapid feedback on the health and functionality of the application.
  It integrates testing into CI/CD pipelines,
  ensuring that code changes are validated early and often.
  CT encompasses various types of tests, such as unit,
  integration, functional, performance, and security tests.
  Its goal is to identify defects as soon as they occur,
  reduce the risk of deployment failures,
  and maintain high software quality in agile and DevOps environments.

FOSS
  [Free and Open Source Software](https://en.wikipedia.org/wiki/Free_and_open-source_software) (FOSS)
  refers to software that is both free to use,
  modify, and distribute and whose source code is openly available.
  The "free" aspect emphasizes freedom rather than cost,
  granting users the rights to study, change, and improve the software.
  FOSS promotes collaboration, transparency, and innovation,
  often developed by distributed communities.
  Licenses like GNU General Public License (GPL), MIT, and Apache ensure these freedoms.
  Examples of FOSS include Linux, Python, and Firefox.
  It plays a critical role in software development
  by providing reusable tools and fostering a shared knowledge ecosystem.  

ITS
  An Issue Tracking System (ITS) is a software tool used to document,
  manage, and track issues, bugs, tasks, and feature requests throughout a project's life cycle.
  It enables teams to report problems, prioritize work, assign responsibilities, and monitor progress.
  Common features include categorization, tagging, status updates, comment threads,
  and integration with version control systems.
  Popular ITS tools include Jira, [GitHub Issues](#bg-ghi), GitLab Issues, and Bugzilla.
  ITS platforms are essential for effective project management, fostering collaboration,
  and ensuring accountability in software development and other workflows.

OIDC
  [OpenID Connect](https://openid.net/connect/) (OIDC)
  is an identity layer built on top of the OAuth 2.0 protocol
  that enables secure authentication and authorization for web and mobile applications.
  OIDC allows applications to verify the identity of a user based on authentication
  performed by an identity provider and to obtain basic profile information about the user.
  Key features of OIDC include support for single sign-on (SSO), session management,
  and compatibility with OAuth 2.0 for access delegation, making it a widely adopted standard
  for identity management and user authentication in platforms such as
  [GitHub](https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect)
  and [PyPI](https://docs.pypi.org/trusted-publishers/).

PAT
  A [Personal Access Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) (PAT)
  is a secure, alphanumeric string used to authenticate a user
  to an application or service in place of a password.
  Commonly used in APIs and version control systems like GitHub,
  PATs allow granular access control by defining specific scopes or permissions,
  such as read-only access or write privileges to repositories.
  PATs enhance security by avoiding the direct use of passwords
  and can be easily revoked or regenerated if compromised.
  They are often used in automated workflows, scripts,
  or integrations requiring authenticated access.

PR
  A Pull Request (PR) is a feature in distributed version control systems such as GitHub,
  which allows developers to propose changes to a codebase.
  It is created when a contributor pushes changes to a branch
  and requests their review and integration into the main or another target branch.
  PRs facilitate collaboration by enabling code reviews,
  discussions, and testing before merging.
  They often include a description of the changes, references to related issues,
  and a summary of the intent or impact of the modification.
  PRs are a critical component of modern collaborative software development workflows.

:::
