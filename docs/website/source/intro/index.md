# Intro
:::{toctree}
:hidden:

background/index
overview/index
fundamentals/index
:::


::::{grid} 1 2 2 2
:gutter: 3
{% for point in pp_meta.keynotes %}
:::{grid-item-card} {{point.title}}
:class-title: sd-text-center
{{point.description}}
:::
{% endfor %}
::::

