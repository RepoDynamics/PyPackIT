# Credits

|{% import 'entity_card.md' as entity_card %}|
{% set emeriti = [] %}



## Team
::::::::::{grid} 1
:gutter: 3

|{% for author in ccc.team.values() %}|
    |{% if author.active %}|
        |{{- entity_card.make_entity(author, ccc) }}|
    |{% else %}|
        {% set _ = emeriti.append(author) %}
    |{% endif %}|
|{% endfor %}|
::::::::::



|{% if emeriti %}|
## Emeriti
::::::::::{grid} 1
:gutter: 3

|{% for emeritus in emeriti %}|
    |{{- entity_card.make_entity(emeritus, ccc) }}|
|{% endfor %}|
::::::::::
|{% endif %}|



|{% if ccc.contributor %}|
## Contributors
::::::::::{grid} 1
:gutter: 3

|{% for contributor in ccc.contributor.values() %}|
    |{{- entity_card.make_entity(contributor, ccc) }}|
|{% endfor %}|
::::::::::
|{% endif %}|



|{% if ccc.role %}|
## Roles
::::::::::{grid} 1
:gutter: 3
|{% for role_id, role in ccc.role.items() %}|
:::::::::{grid-item-card}

[|{{ role.title }}|]{.pst-color-primary .sd-font-weight-bold #role-|{{ role_id }}|} (|{{ role.abbreviation }}|)
^^^
|{{ role.description }}|
|{% if role.assignment %}|
Tasks
-----

|{% if role.assignment.issue %}|
{.sd-text-left}
**Issues**:
|{% for issue_form in manager.issue.forms_from_id_regex(role.assignment.issue) -%}|
{bdg-ref-secondary}`|{{ issue_form.name }}| <issue-form-|{{ issue_form.id }}|>`
|{% endfor %}|
|{% endif %}|

|{% if role.assignment.pull %}|
{.sd-text-left}
**Pull Requests**:
|{% for issue_form in manager.issue.forms_from_id_regex(role.assignment.pull) -%}|
{bdg-ref-secondary}`|{{ issue_form.name }}| <issue-form-|{{ issue_form.id }}|>`
|{% endfor %}|
|{% endif %}|

|{% if role.assignment.review %}|
{.sd-text-left}
**Pull Request Reviews**:
|{% for issue_form in manager.issue.forms_from_id_regex(role.assignment.review) -%}|
{bdg-ref-secondary}`|{{ issue_form.name }}| <issue-form-|{{ issue_form.id }}|>`
|{% endfor %}|
|{% endif %}|

|{% if role.assignment.discussion %}|
{.sd-text-left}
**Discussions**:
|{% for discussion_category in manager.issue.forms_from_id_regex(role.assignment.discussion, "discussion") -%}|
{bdg-ref-secondary}`|{{ discussion_category.emoji }}| |{{ discussion_category.name }}| <discussion-category-|{{ discussion_category.id }}|>`
|{% endfor %}|
|{% endif %}|

|{% endif %}|
+++
DataCite Contribution Type: [|{{ role.type }}|]{.pst-color-primary .sd-font-weight-bold}

:::::::::
|{% endfor %}|
::::::::::
|{% endif %}|
