---
sd_hide_title: true
---
# Security Vulnerability
{{pp_meta.name}} takes the security and privacy of all its users and members very seriously,
and is committed to ensuring the safety of its products and services.
In case a security vulnerability is detected that may affect users, we take immediate action to:
1. fix the issue as soon as possible,
2. release a new security patch in case a published application was affected,
3. release a security advisory, detailing the vulnerability,
as well as guidelines for end-users to protect themselves.
Security advisories are accessible on our website and repository, as well as via a feed.

:::{admonition} {{pp_meta.name}} Security Measures 🛡
:class: seealso
Learn more about our security measures and procedures to handle vulnerability issues on our
maintenance guide(../collaborate/maintenance/index).
:::

## Vulnerability Disclosure Policy

This policy is intended to give users, contributors, and security researchers clear guidelines for
[reporting potential security vulnerabilities](#reporting-a-potential-vulnerability)
and [conducting vulnerability discovery activities](#testing-for-vulnerabilities).
It describes what systems and types of research are covered under this policy,
how to send us vulnerability reports, what information to include,
and how long we ask security researchers to wait before publicly disclosing vulnerabilities.

<blockquote>
    🛡️**Supported Versions**
    <br><br>
    Questions regarding this policy may be sent to security@agency.gov.
    We also invite you to contact us with suggestions for improving this policy.
</blockquote>


### Reporting a Potential Vulnerability
If you have found a potential vulnerability in our application, website, or repository,
please report it as soon as possible, following the guidelines described here.
Please DO NOT

#### Where to Report
We use [GitHub's security advisories feature](https://docs.github.com/en/code-security/security-advisories/repository-security-advisories/about-repository-security-advisories)
of our repository to securely discuss, fix and publish information about security vulnerabilities
in {{pp_meta.name}}.
To privately report a security vulnerability,
follow the [documentation on Github](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing/privately-reporting-a-security-vulnerability#privately-reporting-a-security-vulnerability)
or {{ '[**click here to directly open a private report form**]({})'.format(pp_meta.url.github.security.new_advisory) }}.

Other ways to open a security advisory:

On the {{ '[Issues]({})'.format(pp_meta.url.github.issues.home) }} tab

On the {{ '[Security]({})'.format(pp_meta.url.github.security.home) }} tab


:::::{admonition} {{pp_meta.name}} Security Measures 🛡
:class: seealso
ergergg
::::{dropdown} Email Body

:::{code-block}default

---Thank you for reporting a security vulnerability. Please provide as much information as you can under the sections listed below. Texts like this that are surrounded by three hyphens are instructions and should be deleted before sending the email.---

1. Summary
---Provide a short summary of the problem. Make the impact and severity as clear as possible. For example: An unsafe deserialization vulnerability allows any unauthenticated user to execute arbitrary code on the server.---

2. Details
---Give all details on the vulnerability. Pointing to the incriminated source code is very helpful for the maintainer.---

3. PoC
---Complete instructions, including specific configuration details, to reproduce the vulnerability.---

4. Impact
---What kind of vulnerability is it? Who is impacted?---

5. Affected Products
---For each affected product, name the ecosystem (e.g. pip, GitHub Actions), package- or filename, and affected versions.---

6. Severity
---Asses the severity of the issue, e.g. using a CVSS vector string (learn more at https://www.first.org/cvss/v3.1/user-guide).---

7. Weaknesses
---Provide Common Weakness Enumerator (CWE; learn more at https://docs.github.com/en/code-security/security-advisories/repository-security-advisories/about-repository-security-advisories#cve-identification-numbers).---

8. Mitigation
---Provide necessary steps to mitigate the problem.---

:::

::::
:::::

<blockquote>
    🥷🏾 <b>Prefer Anonymity?</b>
    <br><br>
    Our vulnerability management team also welcomes anonymous emails sent to
    <a href="mailto:{email_security}
?subject=
%5BSecurity%20Vulnerability%20Report%5D%3A%20---Please%20provide%20a%20consc
ise%20title%20here---
&body=
---Thank%20you%20for%20reporting%20a%20security%20vulnerability.%20Please%20
provide%20as%20much%20information%20as%20you%20can%20under%20the%20sections%
20listed%20below.%20Texts%20like%20this%20that%20are%20surrounded%20by%20thr
ee%20hyphens%20are%20instructions%20and%20should%20be%20deleted%20before%20s
ending%20the%20email.---%20%0D%0A%0D%0A1.%20Summary%0D%0A---Provide%20a%20sh
ort%20summary%20of%20the%20problem.%20Make%20the%20impact%20and%20severity%2
0as%20clear%20as%20possible.%20For%20example%3A%20An%20unsafe%20deserializat
ion%20vulnerability%20allows%20any%20unauthenticated%20user%20to%20execute%2
0arbitrary%20code%20on%20the%20server.---%0D%0A%0D%0A2.%20Details%0D%0A---Gi
ve%20all%20details%20on%20the%20vulnerability.%20Pointing%20to%20the%20incri
minated%20source%20code%20is%20very%20helpful%20for%20the%20maintainer.---%0
D%0A%0D%0A3.%20PoC%0D%0A---Complete%20instructions%2C%20including%20specific
%20configuration%20details%2C%20to%20reproduce%20the%20vulnerability.---%0D%
0A%0D%0A4.%20Impact%0D%0A---What%20kind%20of%20vulnerability%20is%20it%3F%20
Who%20is%20impacted%3F---%0D%0A%0D%0A5.%20Affected%20Products%0D%0A---For%20
each%20affected%20product%2C%20name%20the%20ecosystem%20%28e.g.%20pip%2C%20G
itHub%20Actions%29%2C%20package-%20or%20filename%2C%20and%20affected%20versi
ons.---%0D%0A%0D%0A6.%20Severity%0D%0A---Asses%20the%20severity%20of%20the%2
0issue%2C%20e.g.%20using%20a%20CVSS%20vector%20string%20%28learn%20more%20at
%20https%3A%2F%2Fwww.first.org%2Fcvss%2Fv3.1%2Fuser-guide%29.---%0D%0A%0D%0A
7.%20Weaknesses%0D%0A---Provide%20Common%20Weakness%20Enumerator%20%28CWE%3B
%20learn%20more%20at%20https%3A%2F%2Fdocs.github.com%2Fen%2Fcode-security%2F
security-advisories%2Frepository-security-advisories%2Fabout-repository-secu
rity-advisories%23cve-identification-numbers%29.---%0D%0A%0D%0A8.%20Mitigati
on%0D%0A---Provide%20necessary%20steps%20to%20mitigate%20the%20problem.---%2
">{email_security}</a>.
</blockquote>


#### Information to Include

In order to help us assess and triage submissions,
please provide as much information as you can, under following sections:
1. **Title**: A concise title describing the vulnerability.
2. **Summary**: A short summary of the problem. Make the impact and severity as clear as possible.
For example: An unsafe deserialization vulnerability allows any unauthenticated user to execute
arbitrary code on the server.
3. **Details**: Details on the vulnerability, including the location the vulnerability was discovered.
Pointing to the incriminated source code is very helpful for the maintainer.
4. **PoC**: Complete instructions, including specific configuration details, to reproduce the vulnerability.
Proof of concept scripts or screenshots can be helpful to include.
5. **Impact**: The type of vulnerability in terms of potential impact of exploitation and affected users.
6. **Affected Products**: Name of the ecosystem (e.g. pip, GitHub Actions),
package- or filename, and affected versions, for each affected product.
7. **Severity**: Assessment of the severity of the issue, using the [Common Vulnerability Scoring System](https://www.first.org/cvss/specification-document) (CVSS).
8. **Weaknesses**: A [Common Weakness Enumerator](https://docs.github.com/en/code-security/security-advisories/repository-security-advisories/about-repository-security-advisories#cve-identification-numbers) (CWE), if available.
9. **Mitigation**: If known, necessary steps to mitigate the problem.

For more information, also refer to GitHub documentations on
[creating a repository security advisory](https://docs.github.com/en/code-security/security-advisories/repository-security-advisories/creating-a-repository-security-advisory)
and [best practices for writing repository security advisories](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing/best-practices-for-writing-repository-security-advisories).

#### Response Policy
When you choose to share your contact information with us,
we commit to coordinating with you as openly and as quickly as possible:
* Within a week, our vulnerability management team will acknowledge receiving your report.
* To the best of our ability, we will confirm the existence of the vulnerability to you
and be as transparent as possible about what steps we are taking during the remediation process,
including on issues or challenges that may delay resolution.
* We will maintain an open dialogue to discuss issues.

#### Disclosure Policy
This project follows a 120-day disclosure timeline;
if you are a security researcher and would like to disclose the vulnerability you detected,
we request that you **allow us at least 120 days prior to any public exposure**.
This helps the project contributors to resolve the vulnerability and issue a new release,
and provides our users a chance to update their applications and protect themselves.


### Testing for Vulnerabilities
{{pp_meta.name}} is a free and open-source project.
We encourage security researchers to help us improve our security measures
by conducting vulnerability discovery activities on our application, website, and repository.
Before starting, please read the [guidelines](#testing-for-vulnerabilities) below,
describing what systems and types of research are covered under this policy.

#### Authorization
If you make a good faith effort to comply with this policy during your security research,
we will consider your research to be authorized, will work with you to understand and resolve the issue quickly,
and will not recommend or pursue legal action related to your research.
Should legal action be initiated by a third party against you for activities that were conducted
in accordance with this policy, we will make this authorization known.

#### Guidelines
Under this policy, "research" and "vulnerability discovery" means activities in which you:
* notify us as soon as possible after you discover a real or potential security issue,
* make every effort to avoid privacy violations, degradation of user experience,
disruption to production systems, and destruction or manipulation of data,
* only use exploits to the extent necessary to confirm a vulnerability's presence,
* do not use an exploit to compromise or exfiltrate data, establish persistent command line access,
or use the exploit to pivot to other systems,
* provide us a reasonable amount of time to resolve the issue before you disclose it publicly,
* do not submit a high volume of low-quality reports.

Once you've established that a vulnerability exists or encounter
any sensitive data (including personally identifiable information, financial information,
or proprietary information or secrets of any kind), **you must**:
* stop your test,
* notify us immediately,
* and not disclose this data to anyone else.

#### Test Methods
The following test methods are **not authorized**:
* Network denial of service (DoS or DDoS) tests or other tests that
impair access to or damage a system or data.
* Social engineering (e.g. phishing) or any other non-technical vulnerability testing.

#### Scope
This policy applies to any source code, data, or configuration directly stored in our GitHub repository
at {{pp_meta.url.github.home}}, and any software, package, website, or other digital products and services that are
directly published/deployed from this repository.

**Any service not expressly listed above**, such as any connected services, are **excluded from scope**
and are **not authorized** for testing. Additionally, vulnerabilities found in systems from our vendors
fall outside of this policy's scope and should be reported directly to the vendor according to their
disclosure policy (if any). If you aren't sure whether a system is in scope or not,
or there is a particular system not in scope that you think merits testing,
please contact us at {{pp_meta.email.security}} to discuss it first, before starting your research.
