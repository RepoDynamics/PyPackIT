(intro-jsonpath)=
# JSONPath

[JSONPath](https://datatracker.ietf.org/doc/html/rfc9535)
is a query language for extracting a subset of a serializable data structure.
It was originally designed for JSON data,
but can also be used with other data serialization formats like YAML.

In JSONPath, the root of the data structure
is represented by the `$` symbol,
sequences are accessed by their index using square brackets (`[]`),
and mapping values are accessed using either square brackets or dot (`.`) notation.
For example, the path expression `$.l1-key.l2-key[0]`
means that the top-level data structure is a mapping,
it has a key named `l1-key` whose value is also a mapping,
with a key named `l2-key` whose value is a sequence,
and we are referring to the first element (index 0) of that sequence.

Wildcards can also be used in path expressions using the `*` symbol,
to match any key or index at a specific level.
For example, `$[*].l2-key` means that the root data structure is a sequence
of mappings, and we are referring to the value of the key `l2-key` in each mapping.
Similarly, `$.*[1]` means that the root data is a mapping of sequences,
and we are extracting the second element (index 1) of each sequence in the mapping.
