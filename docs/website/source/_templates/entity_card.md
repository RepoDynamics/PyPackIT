<!-- Jinja macro to create a card for a person. -->

|{% macro make_entity(entity, ccc) %}|
:::::::::{grid-item-card}

::::::::{grid} 1 1 2 2
:margin: 0
:padding: 2
:gutter: 3

:::::::{grid-item}
:columns: 12 12 4 4

::::::{grid} 1
:margin: 0
:padding: 0
:gutter: 1

:::::{grid-item}
:padding: 0 2 0 0
:class: centered
![](|{{ entity.avatar }}|)
:::::

:::::{grid-item}
:class: font-h6 centered
|{{ entity.name.full }}| |{% if entity.alias %}|(|{{ entity.alias }}|)|{% endif %}| 
:::::

:::::{grid-item}
:padding: 2 2 0 0
:class: centered
|{% if entity.website -%}|[{fas}`globe;margin-sides`](|{{entity.website.url}}|)|{% endif %}|
|{%- if entity.email -%}|[{fas}`envelope;margin-sides`](|{{entity.email.url}}|)|{% endif %}|
|{%- if entity.github -%}|[{fab}`github;margin-sides`](|{{entity.github.url}}|)|{% endif %}|
|{%- if entity.linkedin -%}|[{fab}`linkedin;margin-sides`](|{{entity.linkedin.url}}|)|{% endif %}|
|{%- if entity.orcid -%}|[{fab}`orcid;margin-sides`](|{{entity.orcid.url}}|)|{% endif %}|
|{%- if entity.researchgate -%}|[{fab}`researchgate;margin-sides`](|{{entity.researchgate.url}}|)|{% endif %}|
|{%- if entity.twitter %}|[{fab}`twitter;margin-sides`](|{{entity.twitter.url}}|)|{% endif %}|
:::::

|{% if entity.affiliation %}|
:::::{grid-item}

<div class="iconed-text">
<span class="icon">

{octicon}`organization;1rem;pst-color-primary`

</span>
<span class="text">

|{{ entity.affiliation }}|

</span>
</div>

:::::
|{% endif %}|

|{% if entity.address or entity["post-code"] or entity.city or entity.region or entity.country %}|
:::::{grid-item}

<div class="iconed-text">
<span class="icon">

{octicon}`location;1rem;pst-color-primary`

</span>
<span class="text">

|{{- [entity.address, entity["post-code"], entity.city, entity.region, entity.country] | select | join(", ") }}|

</span>
</div>

:::::
|{% endif %}|

::::::

:::::::


:::::::{grid-item}
:columns: 12 12 8 8

::::::{grid} 1
:margin: 0
:padding: 0
:gutter: 3

|{% if entity.bio %}|
:::::{grid-item}
Bio
---
|{{ entity.bio }}|
:::::
|{% endif %}|

|{% if entity.role %}|
:::::{grid-item}
Roles
---
|{% for role_id in entity.role.keys() -%}|
{bdg-ref-secondary}`|{{ ccc.role[role_id].abbreviation }}| <role-|{{ role_id }}|>`
|{% endfor %}|
:::::
|{% endif %}|

|{% if entity.ownership %}|
:::::{grid-item}
Code Ownership
---
|{% for ownership in entity.ownership -%}|
`|{{ ownership.glob }}|`
|{% endfor %}|
:::::
|{% endif %}|

::::::

:::::::

::::::::

:::::::::
|{% endmacro %}|
