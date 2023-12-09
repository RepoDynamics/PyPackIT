# Credits


## Authors
::::{grid} 2 3 3 4
:gutter: 3
{% for author in pp_meta.author.entries %}
:::{grid-item-card} {{author.name}}
:class-title: sd-text-center
:class-footer: centered
:img-top: {{author.avatar_url}}
+++
{% if author.url.website -%}[{fas}`globe;margin-sides`]({{author.url.website}}){% endif %}
{%- if author.email -%}[{fas}`envelope;margin-sides`](mailto:{{author.email}}){% endif %}
{%- if author.url.github -%}[{fab}`github;margin-sides`]({{author.url.github}}){% endif %}
{%- if author.url.linkedin -%}[{fab}`linkedin;margin-sides`]({{author.url.linkedin}}){% endif %}
{%- if author.url.orcid -%}[{fab}`orcid;margin-sides`]({{author.url.orcid}}){% endif %}
{%- if author.url.researchgate -%}[{fab}`researchgate;margin-sides`]({{author.url.researchgate}}){% endif %}
{%- if author.url.twitter %}[{fab}`twitter;margin-sides`]({{author.url.twitter}}){% endif %}
:::
{% endfor %}
::::


## Maintainers
::::{grid} 2 3 3 4
:gutter: 3
{% for maintainer in pp_meta.maintainer.list %}
:::{grid-item-card} {{maintainer.name}}
:class-title: sd-text-center
:class-footer: centered
:img-top: {{maintainer.avatar_url}}
+++
{% if maintainer.url.website -%}[{fas}`globe;margin-sides`]({{maintainer.url.website}}){% endif %}
{%- if maintainer.email -%}[{fas}`envelope;margin-sides`](mailto:{{maintainer.email}}){% endif %}
{%- if maintainer.url.github -%}[{fab}`github;margin-sides`]({{maintainer.url.github}}){% endif %}
{%- if maintainer.url.linkedin -%}[{fab}`linkedin;margin-sides`]({{maintainer.url.linkedin}}){% endif %}
{%- if maintainer.url.orcid -%}[{fab}`orcid;margin-sides`]({{maintainer.url.orcid}}){% endif %}
{%- if maintainer.url.researchgate -%}[{fab}`researchgate;margin-sides`]({{maintainer.url.researchgate}}){% endif %}
{%- if maintainer.url.twitter %}[{fab}`twitter;margin-sides`]({{maintainer.url.twitter}}){% endif %}
:::
{% endfor %}
::::


## Collaborators
