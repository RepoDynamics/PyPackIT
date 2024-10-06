# Publications

{% for publication in ccc.owner.publications %}
{% if publication.type == "journal-article" %}
* {{ publication.title }} {{ publication.year }}
{% else %}
* (Emeritus)
{% endif %}
{% endfor %}
