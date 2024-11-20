# Credits


## Authors
::::{grid} 2 3 3 4
:gutter: 3
{% for author in ccc.citation.authors %}
:::{grid-item-card} {{author.name.full}}
:class-title: sd-text-center
:class-footer: centered
:img-top: {{author.avatar}}
+++
{% if author.website -%}[{fas}`globe;margin-sides`]({{author.website.url}}){% endif %}
{%- if author.email -%}[{fas}`envelope;margin-sides`](author.email.url){% endif %}
{%- if author.github -%}[{fab}`github;margin-sides`]({{author.github.url}}){% endif %}
{%- if author.linkedin -%}[{fab}`linkedin;margin-sides`]({{author.linkedin.url}}){% endif %}
{%- if author.orcid -%}[{fab}`orcid;margin-sides`]({{author.orcid.url}}){% endif %}
{%- if author.researchgate -%}[{fab}`researchgate;margin-sides`]({{author.researchgate.url}}){% endif %}
{%- if author.twitter %}[{fab}`twitter;margin-sides`]({{author.twitter.url}}){% endif %}
:::
{% endfor %}
::::


## Maintainers
<!--
::::{grid} 2 3 3 4
:gutter: 3
{% for maintainer in ccc.maintainer.list %}
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
-->

## Collaborators
