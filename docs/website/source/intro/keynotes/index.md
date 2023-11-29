# Keynotes

::::{grid} 1
:gutter: 3
{% for point in pp_meta.keynotes %}
:::{grid-item-card} {{point.title}}
:class-title: sd-text-center
{{point.description}}
:::
{% endfor %}
::::
