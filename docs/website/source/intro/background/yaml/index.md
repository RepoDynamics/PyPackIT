(yaml)=
# YAML

[YAML Ain't Markup Language](https://yaml.org) (YAML)
is a concise, human-readable data serialization format similar to **JSON** and **TOML**.
It is commonly used for configuration files and data exchange
due to its simplicity and ease of integration with programming languages.

YAML represents data in a structured, hierarchical format
using **indentation** for nesting and **key-value** pairs for defining data.
It provides 3 main data types: mappings, sequences, and scalars.
**Scalars** represent single values and include strings, numbers, booleans, and null values.
Sequences and mappings on the other hand are complex data types that can contain other data types.
**Sequences** (equivalent to JSON and TOML arrays or Python lists) are ordered lists of items,
while **mappings** (equivalent to JSON objects, TOML tables, or Python dictionaries)
represent key-value pairs.

Each YAML file contains a single top-level data structure,
which can be any of the mentioned data types.
For example, a YAML file can contain a single string,
and thus act as a plain text file:

:::{code-block} yaml
:caption: YAML file with a single-line string

'Greetings from within a YAML file!'
:::

:::{code-block} yaml
:caption: YAML file with a multi-line string

|
  Greetings from within a YAML file!
  YAML uses syntactically significant newlines and indentation like Python
  to represent complex data structures in a human-readable format.
  The pipe character (|) is used to denote the start of a multi-line string,
  which can span multiple lines without the need for explicit line breaks
  or quotation marks.
:::

It becomes more interesting when the top-level data type is a mapping or a sequence,
allowing for complex and nested data structures.
Sequences can be created either using dashes (`-`) or square brackets (`[]`).
For example, the following YAML file defines a sequence of mixed data types
using the dash notation (notice the use of `#` for comments):

:::{code-block} yaml
:caption: YAML file with a sequence of mixed data types

- This is the first item in the sequence. It is a string.  # and this is a comment!
- 42             # The second item in the sequence, which is an integer.
- 3.14159265359  # Look, it's π in the third place!
- true           # A boolean value as the fourth item.
- null           # This item is a null (aka None).
- [1, 2, 3]      # A nested sequence using square brackets.
- - One          # A nested sequence using dashes.
  - Two
  - Three
:::

Finally, mappings are created using colon (`:`) or curly braces (`{}`):

:::{code-block} yaml
:caption: YAML file with a mapping as the top-level data structure

key1: value1     # A simple key-value pair; both key and value are strings.
key2: true       # he key is a string and its value is a boolean.
true: 1          # The key is a boolean and the value is an integer.
my-dashed-list:  # A key with a nested sequence as its value.
  - One
  - Two
  - Three
my-inline-list: [1, 2, 3]
my-inline-map: {key1: value1, key2: value2}
my_nested_map:
  key1: value1
  key2: value2
  key3: value3
:::

YAML also provides several advanced features such as anchors and tags
to enhance its flexibility and reusability.
[Anchors](https://yaml.org/spec/1.2.2/#3222-anchors-and-aliases)
allow you to define a value once and reference it later using aliases,
which can significantly reduce duplication and improve maintainability of large configurations.
For example, the following YAML file defines a mapping
named `my-default-settings`, anchors it to the alias `default`,
and uses that alias to reuse the mapping in two different places:

:::{code-block} yaml
:caption: YAML file with anchors and aliases

my-default-settings: &default  # The '&' character is used
  key1: value1                 # to define an anchor named 'default'
  key2: value2                 # for the `my-default-settings` mapping.

my-cases:
  - name: case1
    settings: *default         # The '*' character is used to reference the anchor.
  - name: case2
    settings: *default         # Both cases reference the same settings.
:::

[Tags](https://yaml.org/spec/1.2.2/#tags) allow you to explicitly define the datatype of a node
or apply custom semantics to the content.
For instance, a tag like `!str` can be used to specify
that a value should be treated as a string.
|{{ ccc.name }}| uses this feature to allow for
[referencing values from external sources](#manual-cc-inheritance).


:::{admonition} Learn More
:class: seealso

- [Official YAML Specification Index](https://yaml.org/spec/)
- [Learn YAML in Y minutes](https://learnxinyminutes.com/yaml/)
:::
