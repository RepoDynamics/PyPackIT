(manual-cc-templating)=
# Templating

The control center YAML files are equipped with
advanced templating capabilities for
dynamic generation and synchronization of configurations at runtime.
This enables Continuous Configuration Automation, eliminates data redundancy,
and ensures consistency across all project resources.
These features are similar to [Jinja](#intro-jinja) templating used by other tools
(e.g. in [conda build recipes](https://docs.conda.io/projects/conda-build/en/latest/resources/define-metadata.html#templating-with-jinja))
and have some overlaps with [YAML anchors and references](#yaml).
However, |{{ ccc.name }}| implements its own templating engine,
which offers much more features and flexibility for this use case.
For example, |{{ ccc.name }}| templates have access to all other
control center configuration values, and can recursively reference
and use other templates. They can use JSONPath expressions
for complex queries, and allow for the execution of arbitrary Python code to generate values.
Moreover, Jinja-templated YAML files are generally not valid YAML before rendering,
since template elements may break the YAML data structure.
Consequently, these files cannot be viewed, modified, or processed
as normal YAML files, complicating their maintenance.
In contrast, |{{ ccc.name }}|'s templating syntax is designed to maintain
a **valid YAML data structure**.


## Syntax and Behaviour

Templates can be used in place of any key, value,
or sequence element in a YAML file.
Similar to Jinja, templates are surrounded by delimiters
that denote the beginning and the end of the template.
There are four kinds of templates, each with its own start and end delimiters:

1. [Reference templates](#manual-cc-templating-ref) use `${{` and `}}$` delimiters.
2. [Query templates](#manual-cc-templating-query) use `$[[` and `]]$` delimiters.
3. [Code templates](#manual-cc-templating-code) use `#{{` and `}}#` delimiters.
4. [Unpacking templates](#manual-cc-templating-unpack) use `*{{` and `}}*` delimiters.

There must always be at least one space between the
template content and each of the delimiters.
For example, let `...` be a placeholder for the template content.
Then, `${{ ...}}$` is not valid and will be treated as a string,
whereas `${{ ...   }}$` is a valid template. Any other extra whitespace
characters (i.e., newlines and tabs) between the content and delimiters
are allowed as well.


::::{admonition} Example
:class: tip dropdown

Consider a template `${{ ... }}$` (where `...` is some arbitrary content)
that generates the string `"generated_value"`:

1. Usage as a key in a mapping:
   :::{code-block} yaml
   :caption: Input YAML
  
   ${{ ... }}$: some_value
   :::
  
  
   :::{code-block} yaml
   :caption: Output YAML
  
   generated_value: some_value
   :::
2. Usage as a value in a mapping:
   :::{code-block} yaml
   :caption: Input YAML
  
   some_key: ${{ ... }}$
   :::
  

   :::{code-block} yaml
   :caption: Output YAML

   some_key: generated_value
   :::
3. Usage as an element in a sequence:
   :::{code-block} yaml
   :caption: Input YAML
  
   - ${{ ... }}$
   :::
  

   :::{code-block} yaml
   :caption: Output YAML

   - generated_value
   :::

::::

Templates can also generate any valid YAML data structure, not just strings.

::::{admonition} Example
:class: tip dropdown

For example, the template may return the sequence `[1, 2, 3]`,
in which case the above examples will generate the following outputs, respectively:

1. Usage as a key in a mapping:
   :::{code-block} yaml
   :caption: Output YAML
  
   [1, 2, 3]: some_value
   :::
2. Usage as a value in a mapping:
   :::{code-block} yaml
   :caption: Output YAML

   some_key: [1, 2, 3]
   :::
3. Usage as an element in a sequence:
   :::{code-block} yaml
   :caption: Output YAML

   - [1, 2, 3]
   :::

::::

Templates are evaluated recursively,
so that they can depend on other templates.
Before resolving any template, |{{ ccc.name }}| first
resolves all templates that are referenced in the current template.
You only need to make sure not to create circular references,
otherwise you will get an error informing you of the circular path.


(manual-cc-templating-ref)=
## Reference Templates

Reference templates are used to reuse configurations.
They use the syntax `${{ <JSONPath> }}$` where `<JSONPath>`
is a [JSONPath expression](manual-cc-configpaths) (without the leading `$.`)
pointing to a value in the control center configurations.
to extract values from anywhere in the control center configurations.


::::{admonition} Example
:class: tip dropdown

Reference templates are already heavily used as default values for many
configurations in the control center files.
For example, the URL of your documentation website's homepage
is defined at [`$.web.url.home`](#ccc-web-url-home)
and then reused in several other places,
such as the About section of your GitHub repository,
which can be set at [`$.repo.homepage`](#ccc-repo-homepage).
Looking at the default configuration file [`.control/vcs.yaml`](){.user-link-repo-cc-vcs},
you can see the following segment,
which sets the value of `$.repo.homepage` to the value of `$.web.url.home`:

:::{code-block} yaml
:caption: `.control/vcs.yaml`

repo:
  homepage: ${{ web.url.home }}$
:::

::::


(manual-cc-templating-nesting)=
### Nesting

Sometimes, the JSONPath you wish to query may itself contain variable parts
defined elsewhere in your configurations. Such parts can be replaced with
another reference template.
|{{ ccc.name }}| will then first resolve these nested templates to build
the final JSONPath of the parent template.
For each nesting level, you must add an extra `{` and `}`
to the start and end delimiters, respectively.

::::{admonition} Example
:class: tip dropdown

Assume you want to get the full name of a team member
whose ID is stored under a custom key at `$.__data__.target_member_id`:

:::{code-block} yaml

__data__:
  target_member_id: member_1 
:::

Your template must then be:

```text
${{ team.${{{ __data__.target_member_id }}}$.name.full }}$
```

This is first resolved to `${{ team.member_1.name.full }}$`,
which will then return the full name of the member.

Further nesting levels are also allowed.
For example, assume the following configurations:

:::{code-block} yaml
:caption: `.control/vcs.yaml`

__data__:
  first_member_id: member_1
  second_member_id: member_2
  target_member_key: first_member_id 
:::

Here, `first_member_id` and `second_member_id` contain two different member IDs,
and `target_member_key` tells you which one to choose.
To get the corresponding member's full name, you can use the following template:

```text
${{ team.${{{ __data__.${{{{ __data__.target_member_key }}}} }}}$.name.full }}$
```

This will first resolve to:

```text
${{ team.${{{ __data__.first_member_id }}}$.name.full }}$
```

then to `${{ team.member_1.name.full }}$`,
and finally it returns the full name of the member.
::::


(manual-cc-templating-query)=
## Query Templates

JSONPath expressions are queries designed to return a sequence of
zero or more nodes that match the specified expression,
regardless of whether or not that expression specifically points to a single node.
In other words, even simple JSONPath expressions like `$.path.to.some.node`
always return a sequence of values.
When using [reference templates](manual-cc-templating-ref),
|{{ ccc.name }}| checks the length of the returned sequence; if it contains only one node,
then that node is returned, otherwise the entire sequence is returned.
This fails in cases where your query is meant to return a sequence,
but it ends up matching only a single node. In such cases,
the reference template will incorrectly resolve to the node value,
whereas a sequence of node values was expected.
Query templates solve this issue by always 
returning a sequence, regardless of the number of matched nodes.
They can be used in place of reference templates where the query
must return a sequence, but may end up matching only one node.


:::{admonition} Example
:class: tip dropdown

Assume you need a list of your project members' full names for some configuration.
You can generate this list using the JSONPath expression `$.team.*.name.full`.
However, if use a reference template `${{ team.*.name.full }}$`
and your team has only one member, then you will get a string
(i.e. the full name of the only member) instead of a list.
Replacing the reference template with the
corresponding query template `$[[ team.*.name.full ]]$`
ensures that the template always resolves to a sequence,
even when there is only one member.
:::

You can also use [nested reference templates](#manual-cc-templating-nesting)
inside query templates the same way they are used inside reference templates.


(manual-cc-templating-code)=
## Code Templates

Code templates are the most powerful type of template,
allowing you to execute Python code to generate a value.
They use the syntax `#{{ <CODE> }}#` where `<CODE>`
corresponds to a Python function body, i.e.,
any valid Python code ending with a return statement.
For example, `#{{ return 1 + 1 }}#` resolves to the integer `2`.


### JSONPath Queries

Code templates are a superset of reference and query templates,
meaning they can also use JSONPath expressions to query other parts
of the control center configurations.
For this, a function named `get` is provided to the local environment
in which the code is executed. 


::::{admonition} JSONPath Resolver Function
:class: note

:::{py:function} get(path: str, default: typing.Any = None, search: bool = False) -> typing.Any
:single-line-type-parameter-list:
:single-line-parameter-list:

Resolve a JSONPath expression in control center configurations.

:param path: JSONPath expression to resolve.
    The JSONPath syntax is the same as described in reference and query templates.
:param default: Default value to return if no matches are found.
    By default, `None` is returned when `search` is set to `False`,
    otherwise, an empty list is returned.
:param search: Always return a list.
    Setting this to `True` will make the resolution
    work in the same way as query references.
:::
::::


Therefore, any reference template `${{ <JSONPath> }}$` can be
expressed as an equivalent code template `#{{ return get("<JSONPath>") }}#`,
and any query template `$[[ <JSONPath> ]]$` can be
expressed as `#{{ return get("<JSONPath>", search=True) }}#`.


### Helper Variables

Several variables are made available to code templates:

:::{py:data} repo_path
:type: pathlib.Path

Current absolute path to the repository directory on the local machine.
This can be used for example to access files in the repository.
:::

:::{py:data} ccc
:type: dict

Current content (i.e., before synchronization) of the `metadata.json` file.
This can be used for example to check whether a configuration has changed.
:::

::::{py:data} changelog
:type: controlman.changelog_manager.ChangelogManager

A changelog manager with three properties:

:::{py:property} contributor
:type: dict

The `contributor.json` data structure containing
information about the project's external contributors.
:::

:::{py:property} current_public
:type: dict

A [changelog](#cc-changelog) mapping corresponding to the latest
entry in the `changelog.json` file with a `type` other than `local`.
:::

:::{py:property} last_public
:type: dict

A [changelog](#cc-changelog) mapping corresponding to the second-latest
entry in the `changelog.json` file with a `type` other than `local`.
:::

::::

:::{py:data} hook

An `InlineHooks` instance, if defined (see [Using a Python File](#manual-cc-templating-code-hook) below).
:::


### Helper Functions

In addition to the `get` function, several helper functions are also made
available to code templates:


:::{py:function} team_members_with_role_ids(role_ids: str | typing.Sequence[str], active_only: bool = True) -> list[dict]
:single-line-type-parameter-list:
:single-line-parameter-list:

Get team members with specific role IDs.

:param role_ids: Role ID(s) to filter for, as defined in [`$.role`].
    This can be either a single role ID (as a string) or a sequence of role IDs.
:param active_only: Only return team members who are [active](#ccc-team---active). Default is `True`.
:return: A list of dictionaries (i.e., [entity](#https://controlman.repodynamics.com/schema/entity-def) mappings)
    corresponding to selected team members.
    Members are sorted according to their [priority](#ccc-team---role--) (highest first)
    in the given role. If multiple `role_ids` are provided, the highest priority between
    all roles is selected for each member.
    Members with the same priority are sorted alphabetically
    by their last and first names, in that order.
:::


:::{py:function} team_members_with_role_types(role_types: str | typing.Sequence[str], active_only: bool = True) -> list[dict]
:single-line-type-parameter-list:
:single-line-parameter-list:

Get team members with specific role types.

:param role_types: Role type(s) to filter for, as defined in [`$.role.*.type`].
    This can be either a single role type (as a string) or a sequence of role types.
:param active_only: Only return team members who are [active](#ccc-team---active). Default is `True`.
:return: A list of dictionaries (i.e., [entity](#https://controlman.repodynamics.com/schema/entity-def) mappings)
    corresponding to selected team members.
    Members are sorted according to their [priority](#ccc-team---role--) (highest first)
    in the given role. If multiple `role_types` are provided, the highest priority between
    all roles is selected for each member.
    Members with the same priority are sorted alphabetically
    by their last and first names, in that order.
:::


:::{py:function} team_members_without_role_types(role_types: str | typing.Sequence[str], include_other_roles: bool = True, active_only: bool = True) -> list[dict]
:single-line-type-parameter-list:
:single-line-parameter-list:

Get team members without specific role types.

:param role_types: Role type(s) to filter out, as defined in [`$.role.*.type`].
    This can be either a single role type (as a string) or a sequence of role types.
:param include_other_roles: Whether to include team members that have roles other than the excluded role types
:param active_only: Only return team members who are [active](#ccc-team---active). Default is `True`.
:return: A list of dictionaries (i.e., [entity](#https://controlman.repodynamics.com/schema/entity-def) mappings)
    corresponding to selected team members.
:::


:::{py:function} fill_entity(entity: dict) -> tuple[dict, dict | None]:
:single-line-type-parameter-list:
:single-line-parameter-list:

Fill all missing information for a person, using GitHub API.

:param entity: The [entity](#https://controlman.repodynamics.com/schema/entity-def) mapping
    representing the person. It must at least contain a [GitHub ID](#https://controlman.repodynamics.com/schema/entity-def-github-id).
:return: A 2-tuple where the first element is the same `entity` input dictionary
    with all available information filled in-place. Note that already defined values will not be replaced.
    The second tuple element is the raw GitHub user API response.
:::


:::{py:function} slugify(string: str, reduce: bool = True) -> str:
:single-line-type-parameter-list:
:single-line-parameter-list:

Convert a string to a URL-friendly slug.
This performs unicode-normalization on the string,
converts it to lowercase,
and replaces any non-alphanumeric characters with hyphens.

:param string: The string to slugify.
:param reduce: If set to `True` (default), consecutive sequences of hyphens (after replacing non-alphanumeric characters)
    are reduced to a single hyphen, and any leading and trailing hyphens are stripped.
:::


### Dependencies

If your code templates depend on modules
not included in the standard library,
you can declare them in the `requirements.txt` file
of your control center's [`hooks` directory](#manual-cc-hooks).
|{{ ccc.name }}| will `pip install -r` the requirements file
during each synchronization event, so that you can import
those dependencies in your code templates.


(manual-cc-templating-code-hook)=
### Using a Python File

Maintaining long code templates in YAML files is cumbersome,
as they are not processed by IDEs and cannot be easily tested, refactored, or formatted.
|{{ ccc.name }}| allows you to write your template codes in a separate Python file,
which can then be used in any code template inside YAML files.
These reusable code components must be added to a class named `Hooks` inside
a file named `cca_inline.py` located in the control center's [`hooks` directory](#manual-cc-hooks).
By default, this class is added to your repository at
[`.control/hooks/cca_inline.py`](){.user-link-repo-cc-hooks-cca-inline},
where it already contains several methods that are used in your
default configuration files.
You can thus simply add new methods to this class,
to be used within your code templates.
During synchronization, if this class exists, |{{ ccc.name }}|
will automatically instantiate it and make it available to code templates
as a variable named `hook`.


(manual-cc-templating-unpack)=
## Unpacking Templates

Sometimes, instead of templating an entire sequence,
you may want to insert elements at a certain position,
or concatenate the sequence with another.
For example, assume you have the following project keywords:

:::{code-block} yaml

keywords:
  - first main keyword
  - second main keyword
:::

You also have another sequence,
containing some extended keywords:

:::{code-block} yaml

__data__:
  extended_keywords:
    - first extended keyword
    - second extended keyword
:::

If you wish to add your main keywords to the extended list,
you cannot simply use a reference or code template like:

:::{code-block} yaml

__data__:
  extended_keywords:
    - ${{ keywords }}$
    - first extended keyword
    - second extended keyword
:::

as that will incorrectly resolve to:

:::{code-block} yaml

__data__:
  extended_keywords:
    - - first main keyword
      - second main keyword
    - first extended keyword
    - second extended keyword
:::

Instead, you must wrap the reference template inside an unpacking template:

:::{code-block} yaml

__data__:
  extended_keywords:
    - *{{ ${{ keywords }}$ }}*
    - first extended keyword
    - second extended keyword
:::

which will correctly resolve to:

:::{code-block} yaml

__data__:
  extended_keywords:
    - first main keyword
    - second main keyword
    - first extended keyword
    - second extended keyword
:::

Similarly, you can also wrap query and code templates inside unpacking templates.
How this works is that |{{ ccc.name }}| first resolves the nested template
that is wrapped by the unpacking template, and will then iterate over the
resolved value and insert elements one after another at the template's index.
Note that if the nested template returns an empty sequence, nothing will be added.
This can also be useful if want to add a single element conditionally.


## String Formatting

Templates can also be used as a part of any string,
similar to how Python f-strings work.
In this case, the returned values of the templates
are always first cast to a string.
For unpacking templates, |{{ ccc.name }}| first iterates over
the returned value, casts each element to a string,
and joins them via ", " delimiters.


::::{admonition} Example
:class: tip dropdown

Assume the following configurations:

:::{code-block} yaml

name: MyProject
team:
  member_1:
    name:
      first: Jane
      last: Doe
  member_2:
    name:
      first: John
      last: Doe
:::

The template defined at `$.__data__.project_info`: 

:::{code-block} yaml

__data__:
  project_info: >-
    The project ${{ name }}$ 
    has #{{ return len(get("team")) }}# members;
    their names are: *{{ $[[ team.*.name.full ]]$ }}*
:::

will then resolve to:

:::{code-block} yaml

__data__:
  project_info: >-
    The project MyProject 
    has 2 members;
    their names are: Jane Doe, John Doe
:::

::::

For more complex string compositions,
you can instead use a code template that returns the entire string.


## Relative Paths

There may be cases where the absolute JSONPath of a configuration
you want to use in a template is unknown or unstable.
For example, assume you have a sequence of mappings
where some value in each mapping needs to be templated against other values in the same mapping.
You can of course use absolute paths and reference each mapping by its sequence index:

```yaml
__data__:
  dependent_mappings:
    - a: 1
      b: true
      c: >-
        This value depends on
        ${{ __data__.dependent_mappings[0].a }}$ and
        ${{ __data__.dependent_mappings[0].b }}$.
    - a: 2
      b: false
      c: >-
        This value depends on
        ${{ __data__.dependent_mappings[1].a }}$ and
        ${{ __data__.dependent_mappings[1].b }}$.
```

However, you would then need to
update all templates when you insert or remove an element,
since indices would change.
To simplify such cases, |{{ ccc.name }}| extends the JSONPath syntax
to enable using relative paths.
These are resolved relative to the path of the value where the template is defined, as follows:

- When a JSONPath starts with one or more periods (`.`),
  it is considered a relative path.
- One period refers to the path of the **complex data structure** (i.e., mapping or sequence)
  containing the value with the template.
  That is, if the template is used in the value of a key in a mapping,
  `.` refers to the JSONPath of that mapping.
  Similarly, if the template is used in the value of an element in a sequence,
  `.` refers to the JSONPath of that sequence.
- Each additional period refers to the JSONPath of the parent complex data structure
  of the previous JSONPath, following the same logic.

Therefore, the above example can be rewritten as:

```yaml
__data__:
  dependent_mappings:
    - a: 1
      b: true
      c: >-
        This value depends on
        ${{ .a }}$ and
        ${{ .b }}$.
    - a: 2
      b: false
      c: >-
        This value depends on
        ${{ .a }}$ and
        ${{ .b }}$.
```

Now, the templates will always resolve to the values within the same mapping,
regardless of the indices. However, there still remains the problem of redundancy,
as all elements now have the exact same template.
This is where the `__temp__` key comes in play.
As [mentioned earlier](#manual-cc-options-custom),
relative paths in templates defined under `__temp__`
are resolved against the path where that template is referenced, not where it is defined.
This means you can further simplify the above example to:

```yaml
__temp__:
  c: >-
    This value depends on
    ${{ .a }}$ and
    ${{ .b }}$.
__data__:
  dependent_mappings:
    - a: 1
      b: true
      c: ${{ __temp__.c }}$
    - a: 2
      b: false
      c: ${{ __temp__.c }}$
```

### Referencing Keys and Indices

Relative paths can also access the key names of parent mappings
or the index values of parent sequences.
This is done by adding the `__key__` field to end of a relative path.
For example, the following template:

```yaml
__temp__:
  location: >-
    This template is located in
    a mapping named ${{ .__key__ }}$,
    which is at index ${{ ..__key__ }}$
    of a sequence under ${{ ...__key__ }}$
__data__:
  grandparent_sequence:
    - parent_mapping:
        template: ${{ __temp__.location }}$
```

will resolve to:

```yaml
__temp__:
  location: >-
    This template is located in
    a mapping named '${{ .__key__ }}$',
    which is at index ${{ ..__key__ }}$
    of a sequence under '${{ ...__key__ }}$'.
__data__:
  grandparent_sequence:
    - parent_mapping:
        template: >-
          This template is located in
          a mapping named 'parent_mapping',
          which is at index 0
          of a sequence under 'grandparent_seqeunce'.
```
