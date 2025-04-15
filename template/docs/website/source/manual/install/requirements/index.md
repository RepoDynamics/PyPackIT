(manual-reqs)=
# Requirements

|{% import 'dependency_card.md' as dependency_card %}|

:::::{grid} 1
:margin: 4 2 0 0
:padding: 0
:gutter: 2

::::{grid-item}

[Hardware and OS](#manual-reqs-os)
- **Platform independent**: |{{ 'Yes' if ccc.pkg.python.pure else 'No' }}|
- **Supported operating systems**: |{{ ccc.pkg.os.values() | map(attribute='name') | join(', ') }}|
::::

::::{grid-item}
[Python Version](#manual-reqs-py)
- **Implementation**: |{{ ccc.pkg.python.implementation if not ccc.pkg.python.pure else "Any (pure Python)" }}|
- **Version specifier**: `|{{ ccc.pkg.python.version.spec }}|`
- **Supported versions**: |{{ ccc.pkg.python.version.minors | join(', ') }}|
::::

::::{grid-item}
[Dependencies](#manual-reqs-deps)
- **Required runtime dependencies**: |{{ manager.doc.comma_list_of_dependencies(pkg="pkg", dep="core") }}|
- **Optional runtime dependencies**: |{{ manager.doc.comma_list_of_dependencies(pkg="pkg", dep="optional") }}|

|{% set dep_count = manager.doc.dependency_availability() %}|
|{% if ccc.pkg.dependency.core or ccc.pkg.dependency.optional %}|
:::{table} Total number of |{{
   'required and optional' if ccc.pkg.dependency.core and ccc.pkg.dependency.optional
   else ('required' if ccc.pkg.dependency.core else 'optional')
   }}| runtime dependencies and their availability in PyPI, Anaconda, and APT indexing repositories. A green checkmark means all dependencies are available in the respective repository, while a red cross indicates zero availability. For partial cases, the number of available dependencies are given as a fraction of the total number.


| Dependency Type | Total | [PyPI](https://pypi.org/) | [Anaconda](https://anaconda.org/) | [APT](https://www.debian.org/distrib/packages) |
| --------------- | ----- | ---- | -------- | --- |
|{% if ccc.pkg.dependency.core -%}|
| [Required](#manual-reqs-dep-pkg-required) | |{{ dep_count.core.total }}| | |{{ dep_count.core.pip }}| | |{{ dep_count.core.conda }}| | |{{ dep_count.core.apt }}| |
|{% endif -%}|
|{% if ccc.pkg.dependency.optional -%}|
| [Optional](#manual-reqs-dep-pkg-optional) | |{{ dep_count.optional.total }}| | |{{ dep_count.optional.pip }}| | |{{ dep_count.optional.conda }}| | |{{ dep_count.optional.apt }}| |
|{% endif %}|
:::
|{% endif %}|
::::

:::::



(manual-reqs-os)=
## Hardware and OS

|{{ ccc.name }}| can be installed on any of the operating systems
listed in {numref}`tab-pkg-os-reqs`.
Note that |{{ ccc.name }}| is |{% if not ccc.pkg.python.pure -%}| not |{%- endif %}| a
[pure-Python](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#pure-python-wheels)
(a.k.a. [Noarch](https://docs.conda.io/projects/conda/en/stable/user-guide/concepts/packages.html#noarch-packages)) package,
meaning that it |{% if ccc.pkg.python.pure -%}| does not implement any |{%- else -%}| implements |{%- endif %}|
[binary extensions](https://packaging.python.org/en/latest/guides/packaging-binary-extensions/).
Therefore,
|{% if ccc.pkg.python.pure -%}|
|{{ ccc.name }}| can be built and installed the same on any platform from a single
[source or binary distribution](https://packaging.python.org/en/latest/discussions/package-formats/).
|{%- else -%}|
installations from [source and binary distributions](https://packaging.python.org/en/latest/discussions/package-formats/)
are platform-specific.
{numref}`tab-pkg-os-reqs` contains a list of supported platforms for which |{{ ccc.name }}| provides
[wheels](https://packaging.python.org/en/latest/specifications/binary-distribution-format/)
|{% endif %}|


:::{table} Operating systems supported by |{{ ccc.name }}|. The **Runner** column indicates the name of the corresponding [GitHub Actions runner](https://docs.github.com/en/actions/using-github-hosted-runners/using-github-hosted-runners/about-github-hosted-runners#standard-github-hosted-runners-for-public-repositories) used to build and test |{{ ccc.name }}|. |{% if not ccc.pkg.python.pure -%}| [**Platform Compatibility Tags**](https://packaging.python.org/en/latest/specifications/platform-compatibility-tags/) describe compatible platforms for the operating system. Each [tag](https://cibuildwheel.pypa.io/en/stable/options/#build-skip) specifies the Python implementation and version, as well as OS type and CPU architecture of a compatible platform. |{% endif %}|
:name: tab-pkg-os-reqs

| Name | Runner | |{% if not ccc.pkg.python.pure %}| Platform Compatibility Tags | |{% endif %}|
|------|--------| |{% if not ccc.pkg.python.pure %}| --- | |{% endif %}|
|{% for os in ccc.pkg.os.values() -%}|
| |{{ os.name }}| | `|{{ os.runner }}|` | |{% if not ccc.pkg.python.pure %}| |{{ (os.builds | map('wrap', '`') | join(', ')) }}| | |{% endif %}|
|{% endfor %}|
:::



(manual-reqs-py)=
## Python Version

|{{ ccc.name }}| |{% if ccc.pkg.python.pure -%}| does not implement any |{%- else -%}| implements |{%- endif %}|
[binary extensions](https://packaging.python.org/en/latest/guides/packaging-binary-extensions/)
|{% if ccc.pkg.python.pure -%}|
and is therefore compatible with all
[Python implementations](https://www.python.org/download/alternatives/). However,
|{% else -%}|
that require the `|{{ ccc.pkg.python.implementation }}|`
[Python implementation](https://www.python.org/download/alternatives/). Moreover,
|{% endif -%}|
|{{ ccc.name }}| requires a Python version matching the
[version specifier](https://packaging.python.org/en/latest/specifications/version-specifiers/#id5)
`|{{ ccc.pkg.python.version.spec }}|`.
In general, |{{ ccc.name }}| tries to follow the Numpy Enhancement Proposal
[NEP 29](https://numpy.org/neps/nep-0029-deprecation_policy.html)
as closely as possible, meaning that each |{{ ccc.name }}| release supports
all minor versions of Python released up to 42 months prior to the release,
and at minimum the two latest minor versions.
Currently supported Python versions are:
|{% for minor_version in ccc.pkg.python.version.minors -%}|
- `|{{ minor_version }}|`
|{% endfor %}|



(manual-reqs-deps)=
## Dependencies

A full list of |{{ ccc.name }}|'s dependencies
are provided in {numref}`tab-pkg-deps`.
They are categorized into build and runtime dependencies:

- **Build dependencies** are only required when building |{{ ccc.name }}| from source,
  but not when installing from a built distribution, and not during runtime.
  They are temporarily installed in an isolated environment during the build process,
  and are discarded afterwards.
- **Runtime dependencies** are required during execution
  and must therefore be available in the environment where the software runs.
  They are categorized into required and optional groups:
  - **Required** dependencies are always needed during runtime.
  - **Optional** dependencies are only required to perform specific additional tasks.
    For each optional task, the required dependencies thus form an optional dependency group.



|{{ ccc.name }}|
|{% if not (ccc.pkg.dependency.core or ccc.pkg.dependency.optional) -%}|
does not have any required or optional runtime dependencies, i.e.,
everything needed to run |{{ ccc.name }}| is contained within the package itself.
However,
|{%- elif ccc.pkg.dependency.core and ccc.pkg.dependency.optional -%}|
has [**|{{ dep_count.core.total }}| required**](#manual-reqs-dep-pkg-required) and
[**|{{ dep_count.optional.total }}| optional dependencies**](#manual-reqs-dep-pkg-optional).
Moreover,
|{%- elif ccc.pkg.dependency.core -%}|
does not define any optional dependencies, but
has [**|{{ dep_count.core.total }}| required dependenc|{{ 'y' if dep_count.core.total == 1 else 'ies' }}|**](#manual-reqs-dep-pkg-required).
Moreover,
|{%- else -%}|
does not have any required dependencies,
but defines [**|{{ dep_count.optional.total }}| optional dependenc|{{ 'y' if dep_count.optional.total == 1 else 'ies' }}|**](#manual-reqs-dep-pkg-optional).
Moreover,
|{% endif -%}|
|{% set count_build_deps = ccc.pkg.dependency.build | length -%}|
|{{ ccc.name }}| has [**|{{ count_build_deps }}| build dependenc|{{ 'y' if count_build_deps == 1 else 'ies' }}|**](#manual-reqs-dep-pkg-build).

In addition to the main application, |{{ ccc.name }}| also provides |{{ ccc.test.name }}|---a
separate application for testing and benchmarking |{{ ccc.pkg.name }}|---with
its own set of dependencies.
These are listed separately in {numref}`tab-test-deps`.


|{% macro make_row(dep_id, dep, type, optional, pkg_type) -%}|
    | [|{{ dep.name }}|](#dep-|{{ pkg_type }}|-|{{ dep_id }}|) | |{{ type }}| | |{{ optional or '❌' }}| | |{{ '✅' if dep.get("pip", {}).get("selector") or dep.get("conda", {}).get("selector") else '❌' }}| | |{{ '✅' if dep.pip else '❌' }}| | |{{ '✅' if dep.conda else '❌' }}| | |{{ '✅' if dep.apt else '❌' }}| |
|{%- endmacro %}|

|{% for pkg_type in ("pkg", "test") %}|
|{% set pkg = ccc.get(pkg_type, {}) %}|
|{% set deps = pkg.dependency %}|
|{% if deps %}|
(manual-reqs-dep-|{{ pkg_type }}|)=
### |{{ pkg.name }}|

:::{table} |{{ ccc.pkg.name }}|'s dependencies. For optional dependencies, the name of the optional dependency group is specified, otherwise a red cross indicates a required dependency. Platform-specific dependencies are marked with a green checkmark. PyPI, Anaconda, and APT columns indicate whether the dependency is available in the respective repository.
:name: tab-|{{ pkg_type }}|-deps

| Name | Type | Optional | Platform Specific | PyPI | Anaconda | APT |
|------|------|----------|-------------------|------|----------|-----|
|{% for dep_id, dep in deps.get("core", {}) | dictsort -%}|
  |{{ make_row(dep_id, dep, "Runtime", "", pkg_type) }}|
|{% endfor -%}|
|{% for _, dep_group in deps.get("optional", {}) | dictsort -%}|
  |{% for dep_id, dep in dep_group.package | dictsort -%}|
    |{{ make_row(dep_id, dep, "Runtime", dep_group.name, pkg_type) }}|
  |{% endfor -%}|
|{% endfor -%}|
|{% for dep_id, dep in deps.get("build", {}) | dictsort -%}|
  |{{ make_row(dep_id, dep, "Build", "", pkg_type) }}|
|{% endfor -%}|
:::

|{% if deps.core or deps.optional %}|
(manual-reqs-dep-|{{ pkg_type }}|-runtime)=
#### Runtime
|{% endif %}|

|{% if deps.core %}|
(manual-reqs-dep-|{{ pkg_type }}|-required)=
##### Required

:::::{grid} 1
:margin: 0
:padding: 4 4 0 0
:gutter: 3

|{% for dep_id, dep in deps.core | dictsort -%}|
    |{{ dependency_card.make(dep_id, dep, pkg_type) }}|
|{% endfor %}|

:::::
|{%- endif %}|


|{% if deps.optional -%}|
(manual-reqs-dep-|{{ pkg_type }}|-optional)=
##### Optional

|{% for group_id, dep_group in deps.optional | dictsort -%}|
(manual-reqs-dep-|{{ pkg_type }}|-optional-|{{ group_id }}|)=
###### |{{ dep_group.name }}|

|{{ dep_group.description }}|

:::::{grid} 1
:margin: 0
:padding: 4 4 0 0
:gutter: 3

|{% for dep_id, dep in dep_group.package | dictsort -%}|
    |{{ dependency_card.make(dep_id, dep, pkg_type) }}|
|{% endfor -%}|
:::::

|{% endfor -%}|

|{%- endif %}|


|{% if deps.build -%}|
(manual-reqs-dep-|{{ pkg_type }}|-build)=
#### Build

:::::{grid} 1
:margin: 0
:padding: 4 4 0 0
:gutter: 3

|{% for dep_id, dep in ccc.pkg.dependency.build | dictsort -%}|
    |{{ dependency_card.make(dep_id, dep, pkg_type) }}|
|{% endfor %}|
:::::
|{% endif %}|


|{% endif %}|
|{% endfor %}|
