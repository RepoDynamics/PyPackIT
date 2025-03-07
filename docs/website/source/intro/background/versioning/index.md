(bg-versioning)=
# Versioning

Software versioning is a systematic method of
assigning unique version numbers to software releases,
allowing developers and users
to track changes, improvements, and fixes over time.
Versioning is crucial for managing software development,
ensuring backward compatibility, and facilitating effective collaboration among teams.
A well-defined versioning strategy enhances transparency,
simplifies dependency management,
and supports Continuous workflows and cloud-native practices.

Historically, software versioning began as simple incremental numbering
but has evolved into more structured and standardized systems.
Today, versioning strategies often reflect the development lifecycle,
stability, and compatibility of software.
Popular methods include Semantic Versioning (SemVer),
date-based versioning, and revision control systems
that embed version history into the software development process.
Selecting the appropriate versioning strategy is vital for managing feature development,
bug fixes, and major architectural changes.


(bg-semver)=
## Semantic Versioning

[Semantic Versioning](https://semver.org/spec/v2.0.0.html) (SemVer) is one of the
most widely adopted versioning systems in software development.
It uses a three-part version number in `X.Y.Z` format (e.g., `1.2.3`),
where `X`, `Y`, and `Z` are non-negative integers
representing the so-called ***major***, ***minor***, and ***patch*** numbers, respectively.
This system promotes clarity, helping developers and users
understand the impact of software updates.
SemVer's structured approach helps communicate
the nature of changes between releases;
for each release, one of the components is incremented by 1,
while the lower-priority components (major > minor > patch) are reset to 0.
Which component is incremented depends on the type of changes in the release ({numref}`fig-semver`):

1. **Major release**:
  If the release contains any backward-incompatible changes,
  then the major number must be incremented.
2. **Minor release**:
   Otherwise, if the release contains new features or
   other important updates, then the minor number is incremented.
3. **Patch release**:
   The patch number is incremented when the release
   only contains backward-compatible bug fixes and improvements.

:::{image} /_media/figure/semver_light.svg
:class: hidden
:::
:::{figure} /_media/figure/semver_dark.svg
:alt: SemVer
:class: dark-light themed
:align: center
:name: fig-semver

Schematic overview of Semantic Versioning.
Depending on the type of new changes,
one of *major*, *minor*, or *patch* numbers are incremented by 1,
while the lower-priority numbers (the ones to its right) are reset to 0.
:::

Note that SemVer necessitates that the application has a clear public API,
enabling distinction between backward-compatible and incompatible changes.
The public API is introduced in version `1.0.0`,
while major version zero (`0.y.z`) is for initial development and signals an unstable API.
Pre-release and build metadata can also be appended to version numbers,
by appending a hyphen or plus sign followed by a series of dot-separated identifiers,
e.g., `2.1.4-alpha`, `2.1.4+build.123`, or `2.1.4-beta.2+build.3`.


(bg-pep440)=
## Python Version Specifiers

Python package versioning must follow the [specifications](https://packaging.python.org/en/latest/specifications/version-specifiers/#version-specifiers)
set by the PyPA. Originally described in [PEP 440](https://peps.python.org/pep-0440/),
this standard defines how Python projects should assign version numbers
to ensure compatibility across the Python ecosystem,
particularly for distribution on PyPI.
According to PyPA's specifications,
canonical [public version identifiers](https://peps.python.org/pep-0440/#public-version-identifiers)
must be unique within a given distribution,
and must comply with the following scheme, where each `N` is a non-negative integer:

:::{code-block} text
[N!]N(.N)*[{a|b|rc}N][.postN][.devN]
:::

The identifier is separated into five segments:
* [Epoch segment](https://peps.python.org/pep-0440/#version-epochs) `N!`
  is optional, and implicitly set to `0!`. An explicit epoch can be set
  to denote a change in the versioning scheme itself.
* [Release segment](https://peps.python.org/pep-0440/#final-releases) `N(.N)*`
  is the only required part, consisting of any number of dot-separated integers, e.g., `1.2.3`.
* [Pre-release segment](https://peps.python.org/pep-0440/#pre-releases) `{a|b|rc}N`
  can be optionally added to indicate an alpha (`a`), beta (`b`), or release candidate (`rc`) prerelease,
  followed by an integer that enumerates different prereleases in the same phase.
* [Post-release segment](https://peps.python.org/pep-0440/#post-releases) `.postN`
  can be added to indicate minor corrections after a release.
* [Development release segment](https://peps.python.org/pep-0440/#developmental-releases) `.devN`
  can be used to indicate a pre-alpha developmental release.

Any given release is considered either a ***final release***, ***pre-release***, ***post-release***,
or ***developmental release***, depending on which segments are present:
- A version identifier that consists solely of a release segment and optionally an epoch identifier
  is termed a “final release”.
-  A version identifier that consists solely of a release segment and a pre-release segment is
   termed a “pre-release”.
- A version identifier that includes a post-release segment without a developmental release segment
  is termed a “post-release”.
- A version identifier that includes a developmental release segment is termed a “developmental release”.

There are both similarities and differences between PyPA's version specifiers and SemVer.
For example, the release segment's format is similar to SemVer,
but PyPA does not specify the number of integers whereas SemVer has exactly three.
Moreover, PyPA defines a clear scheme for developmental, pre, and post-releases,
while SemVer only specifies some general rules for prereleases.
The separators used by PyPA and SemVer are also different,
with SemVer using hyphens to separate the prerelease segment.
Nevertheless, SemVer versioning can be readily adopted by Python projects,
since PyPA's specifications can be seen as a superset of SemVer
with some inconsequential syntactic differences.
