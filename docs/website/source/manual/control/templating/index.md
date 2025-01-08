(manual-cc-templating)=
# Templating

The control center YAML files are equipped with
advanced templating capabilities for
dynamic generation and synchronization of configurations at runtime.
This enables Continuous configuration automation, eliminates data redundancy,
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


## General Syntax

Similar to Jinja, templates are surrounded by delimiters
that denote the beginning and the end of the template.
There are four kinds of templates, each with its own start and end delimiters:

1. [Reference templates](#manual-cc-templating-ref) use `${{` and `}}$` delimiters.
2. [Query templates](#manual-cc-templating-query) use `$[[` and `]]$` delimiters.
3. [Code templates](#manual-cc-templating-code) use `#{{` and `}}#` delimiters.
4. [Unpacking templates](#manual-cc-templating-unpack) use `*{{` and `}}*` delimiters.

Templates can be used in place of any key, value, or sequence element in a YAML file.

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


(manual-cc-templating-ref)=
## Reference Templates

Reference templates are used to reuse configurations.
They use the syntax `${{ <JSONPath> }}$` where `<JSONPath>`
is a [JSONPath expression](manual-cc-configpaths) (without the leading `$.`)
to extract values from anywhere in the control center configurations.
Note that there must be **at least one whitespace character**
between `<JSONPath>` and each of the delimiters. For example,
`${{ <JSONPath>}}$` is not valid and will be treated as a string,
whereas `${{ <JSONPath>   }}$` is a valid template.


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


### JSONPath Queries

Substitutions allow the use of JSONPath expressions,
which can be used for complex queries,
e.g., to dynamically build an array of values from different parts of the control center.
For example, if you need a list of all team members' full names,
you can use the following JSONPath expression: `${‎{ team[*].name.full }}`.


### Recursive Referencing

Substitutions are evaluated recursively,
meaning that you can use substitutions to reference a content that itself contains substitutions.
You only need to make sure not to create any circular references,
otherwise you will get an error.
  


## Relative Paths

Substitutions can use relative paths,
which are resolved relative to the path of the value using the substitution.
This is particularly useful when using substitutions at locations
that do not have a fixed path. For example, assume you have a sequence of mappings
where some value in each mapping depends on other values in the same mapping.
You can of course use absolute paths and reference each mapping by its sequence index,
but then you would need to update all references every time you add or remove a mapping,
since indices would change.

To simplify such cases, |{{ ccc.name }}| extends the JSONPath syntax
to enable using relative paths, as follows:
- When a path starts with one or more periods (`.`),
  it is considered a relative path.
- One period refers to the path of the **complex data structure** (i.e., mapping or sequence)
  containing the value using the substitution.
  That is, if the substitution syntax is used in the value of a key in a mapping,
  `.` refers to the path of that mapping.
  Similarly, if the substitution syntax is used in the value of an element in a sequence,
  `.` refers to the path of that sequence.
- Each additional period refers to the path of the parent complex data structure
  of the previous path, following the same logic.


:::{admonition} Example
:class: tip dropdown

This feature is used to dynamically set default values for new pieces of data
that are added to the control center. For example, the control center has configurations
for entering the [`email`](#cccdef-email) and other social accounts of each team member.
Each of these are a mapping including the keys `id` and `url`.
By default, the `url` key of each mapping is built using string substitution with relative paths.
For example, `email.url` is set to `mailto:${‎{ .id }}`,
and `linkedin.url` is set to `https://linkedin.com/in/${‎{ .id }}`.
:::


## Code Templates



## Sequence Unpacking

Sometimes, instead of templating an entire sequence,
you may want to insert elements at a certain position.
For example, assume you have following keywords:

:::{code-block} yaml
:caption: `.control/vcs.yaml`

repo:
  description: ${‎{ title }}
:::


## String Formatting

Templates can also be used as part of a string value

Substitutions can be used within strings,
enabling the dynamic construction of complex values from multiple parts of the control center.
For example, the title used in your project's citation,
configurable at [`$.citation.title`](#ccc-citation-title),
is set to `${‎{ name }}: ${‎{ title }}`,
so, assuming your project's [`$.name`](#ccc-name) and [`$.title`](#ccc-title)
are `MyProject` and `A Great Project`, respectively,
the citation title will be `MyProject: A Great Project`.
Note that if you reference a value that is not a string,
it will be converted to a string before being substituted.
In contrast, when the entire value is being substituted
(i.e., the entire string is only the substitution syntax),
the substituted value will have the same type as the referenced value.