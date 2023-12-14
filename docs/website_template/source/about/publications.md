# Publications

{% for publication in pp_meta.owner.publications %}
{% if publication.type == "journal-article" %}
* {{ publication.title }} {{ publication.year }}
{% else %}
* (Emeritus)
{% endif %}
{% endfor %}
