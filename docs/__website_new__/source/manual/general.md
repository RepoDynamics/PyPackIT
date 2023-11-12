# General Information

## Development Life Cycle
{{pp_meta.name}} follows a triphasic development life cycle:
- **Development Phase**: This phase starts with the planning step, followed by pre-alpha, alpha
https://en.wikipedia.org/wiki/Software_release_life_cycle

### Versioning
* {{pp_meta.name}} follows the [Semantic Versioning (SemVer) 2.0.0](../intro/fundamentals/versioning.md#semantic-versioning)
version scheme, with a **strict Major.Minor.Patch** format and no added segments.
* During the initial development phase, releases with major version zero, i.e. `0.Y.Z`, are published.
These are pre-releases with potentially unstable API, meaning that backward-incompatible breaking changes
may be introduced in new minor releases without an earlier deprecation warning.
* before
defining a stable API in version `1.0.0`.
* Our ideal goal is to never have to release a version `3.0.0`; we use `0.Y.Z` releases to
rapidly reach a complete and stable API that is well-structured and sufficiently tested. This is then followed
by a long period of `1.Y.Z` releases, during which {{pp_meta.name}} evolves with feedback from its users,
and adopts itself to their needs.

### Changelog
Each new release is accompanied by comprehensive release notes, describing all changes applied to
the public API since the former release. Changes are categorized into following groups, according to SemVer:
- Major updates:
  - **Removed**: API components and features that are removed.
  - **Changed**: API components and features that are changed.
- Minor updates:
  - **Deprecated**: API components and features that are announced deprecated.
  - **Added**: New API components and features that are added.
- Patch updates:
  - **Improved**: API components and features that are improved in terms of functionality and performance.
  - **Fixed**: Issues and bugs that are resolved.
  - **Security**: Security vulnerabilities that are resolved.

:::{admonition} Other Changes
:class: note
To learn more about how we keep record of changes to other parts of the project, such as documentations,
test-suites, and maintenance, please refer to the maintenance guide.
:::

### Continuous Delivery
* {{pp_meta.name}} practices continuous delivery with a one-change-per-release policy.
* Each new release contains either only patch updates, minor updates, or major updates, where all changes
are related to a single feature, or a closely-related family of features.
* For example, new major versions only consist of updates that remove or change
a formerly deprecated feature, whereas new features are only introduced in new minor versions
that do not contain any patch updates.


### Backward Compatibility
* Backward-incompatible (breaking) changes are always announced before being released.
These so-called deprecation warnings are declared in both inside the application and in the documentation,
in at least one earlier minor release.
* **In pre-releases**, i.e. major version zero, these breaking changes are applied in the minor release
directly following the minor release where the deprecation was announced. That is, an API component that
exists in version `0.Y.Z` may be announced deprecated in version `0.(Y+1).0`,
and the corresponding change/removal is subsequently applied in version `0.(Y+2).0`.
* **After the first final release**, breaking changes are applied in the next major version
relative to the version that announced the deprecation.
That is, when a deprecation is announced in version `X.Y.Z`, the corresponding breaking change
will always be applied exactly in version `(X+1).0.0`.


### Supported Versions
{{pp_meta.name}} always supports its **two latest major versions**, with one distinction:
> ⚠️ New features will only be added to the latest major version.

That is, while the second-latest major version continues receiving patch updates
to fix problems that are discovered later, it will not receive any new minor updates.

> 🚫 Major version zero will not receive any updates after the release of version `1.0.0`.

Since our plan is to


### {{pp_meta.name}} as Dependency
Managing {{pp_meta.name}} as a dependency in your project is super easy. Simply apply a version constraint
to only allow minor and patch updates. That is, when you are using version `X.Y.Z` (`X` != 0)
in your development and tests, define a constraint in your dependency as `< (X+1).0.0`. For example, if the
{{pp_meta.name}} version used is `1.Y.Z`, then the constraint should be "{{pp_meta.name}} < 2.0.0".
This will make sure that you will receive all bug fixes, improvements and other patch updates
