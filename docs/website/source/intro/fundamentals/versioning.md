# Software Versioning
[Software versioning](https://en.wikipedia.org/wiki/Software_versioning)
is the process of assigning a unique and meaningful identifier to each unique state of a computer software.

A standardized version scheme for identifying Python software distributions
was introduced in [PEP 440](https://peps.python.org/pep-0440/).
According to PEP 440, canonical [public version identifiers](https://peps.python.org/pep-0440/#public-version-identifiers)
must be unique within a given distribution, and must comply with the following scheme (each `N` must be a non-negative integer):
:::{code-block} none
[N!]N(.N)*[{a|b|rc}N][.postN][.devN]
:::
The identifier is separated into five segments:
* [Epoch segment](https://peps.python.org/pep-0440/#version-epochs) `N!` (optional)
* [Release segment](https://peps.python.org/pep-0440/#final-releases) `N(.N)*`
* [Pre-release segment](https://peps.python.org/pep-0440/#pre-releases) `{a|b|rc}N` (optional)
* [Post-release segment](https://peps.python.org/pep-0440/#post-releases) `.postN` (optional)
* [Development release segment](https://peps.python.org/pep-0440/#developmental-releases) `.devN` (optional)

Any given release is considered either a “final release”, “pre-release”, “post-release”
or “developmental release”, depending on which segments are present:
  * A version identifier that consists solely of a release segment and optionally an epoch identifier
    is termed a “final release”.
  *  A version identifier that consists solely of a release segment and a pre-release segment is
     termed a “pre-release”.
  * A version identifier that includes a post-release segment without a developmental release segment
    is termed a “post-release”.
  * A version identifier that includes a developmental release segment is termed a “developmental release”.

Some other key takeaways from PEP 440 are:
* Final releases within a project MUST be numbered in a consistently increasing fashion.
* Comparison and ordering of release segments considers the numeric value of each component
of the release segment in turn. When comparing release segments with different numbers of components,
the shorter segment is padded out with additional zeros as necessary.


## Semantic Versioning
[Semantic Versioning (SemVer) 2.0.0](https://semver.org/spec/v2.0.0.html)
to track and communicate changes to its public API, i.e. the part of the application that
users interact with.

Any change to {{pp_meta.name}} public API is categorized into one of three groups,
according to SemVer:
* **Patch**: Backward-compatible changes that only fix a problem or improve a feature.
* **Minor**: Backward-compatible changes that add new features or deprecate existing features.
* **Major**: Backward-incompatible changes, i.e. removal of deprecated features, or breaking changes to a feature.

On the other hand, each release of {{pp_meta.name}} is identified with a unique version number,
consisting of three non-negative integers X, Y, and Z, formatted as `X.Y.Z` (e.g. `1.0.2`).
These correspond to the three groups described above,
and are called major-, minor-, and patch version, respectively (details coming up).

The first release is assigned the version number `1.0.0`, and defines a complete and stable public API
(see below to learn more about pre-releases during the initial development phase).
Subsequently, the version of any new releases is determined from the version number of
the current latest release, according to the types of changes being made:
* If all applied changes since the latest release are patch updates, the patch version is incremented by 1.
That is, the successor of version `X.Y.Z` will be `X.Y.(Z+1)`. For example, the successor of version
`1.0.0` in this case will be version `1.0.1`.
* If any one of the applied changes is a minor update while no major changes are done, the minor version is
incremented by 1, and the patch version is reset to 0.
That is, the successor of version `X.Y.Z` will be `X.(Y+1).0`. This is regardless of whether patch updates also
exist. For example, applying a minor update to either version `1.0.0` or `1.0.1`
results in version `1.1.0` as the next version.
* If any major update exists, the major version is incremented by 1, and the minor and patch versions are reset
to 0. Again, this is regardless of whether lower priority updates have also been made. For example, a major update
to either version `1.0.0`, `1.0.1` or `1.1.0` results in version `2.0.0` as the next version.

The public API is defined in version `1.0.0` (first release).
During the initial development phase, pre-releases with major version zero, i.e. `0.Y.Z`, are published;
these are unstable pre-releases, where breaking changes only increment the minor version.
