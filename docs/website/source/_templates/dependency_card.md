<!-- Jinja macro to create a card for a dependency. -->

|{% macro make(dep_id, dep, pkg_type) -%}|

::::{grid-item-card}

[**|{{ dep.name }}|**]{#dep-|{{ pkg_type }}|-|{{ dep_id }}| .pst-color-primary} [`|{{ dep.import_name }}|`]{.float-right}
^^^
|{{ dep.description }}|

Specifiers
---
|{% if dep.pip -%}|
- [**PyPI**](|{{ dep.get("url", {}).get("pip") or "https://pypi.org/project/" ~ dep.name }}|):
  - Specifier: `|{{ dep.pip.spec }}|`
  |{% if dep.pip.selector -%}|
  - Platform selector: `|{{ dep.pip.selector }}|`
  |{%- endif %}|
|{%- endif %}|
|{% if dep.conda -%}|
- [**Anaconda**](|{{ dep.get("url", {}).get("conda") or "https://anaconda.org/" ~ dep.conda.channel ~ "/" ~ dep.name }}|):
  - Channel: `|{{ dep.conda.channel }}|` 
  - Specifier: `|{{ dep.conda.spec }}|`
  |{% if dep.conda.selector -%}|
  - Platform selector: `|{{ dep.conda.selector }}|`
  |{%- endif %}|
|{%- endif %}|
|{% if dep.apt -%}|
- [**APT**](|{{ dep.get("url", {}).get("apt") or "https://packages.debian.org/" ~ dep.name }}|): 
  - Specifier: `|{{ dep.apt.spec }}|`
|{%- endif %}|

|{% set excluded_keys = ['pip', 'conda', 'apt', 'docs', 'source'] %}|
|{% set resources = [] %}|
|{% for key, value in dep.get("url", {}).items() %}|
    |{% if key not in excluded_keys %}|
        |{% set _ = resources.append(value) %}|
    |{% endif %}|
|{% endfor %}|

|{% if resources or (dep.url and (dep.url.docs or dep.url.source)) -%}|
Resources
---
|{% if dep.get("url", {}).get("source") -%}|
- Source code: |{{ dep.url.source }}|
|{%- endif %}|
|{% if dep.get("url", {}).get("docs") -%}|
- Documentation: |{{ dep.url.docs }}|
|{%- endif %}|
|{% for resource in resources -%}|
- |{{ resource.title }}|: |{{ resource.url }}|
|{%- if resource.description %}|
  |{{ resource.description }}|
|{%- endif -%}|
|{% endfor %}|

|{% endif %}|


|{% if dep.notes %}|
Notes
---
|{{ dep.notes }}|
|{%- endif %}|
::::

|{%- endmacro %}|
