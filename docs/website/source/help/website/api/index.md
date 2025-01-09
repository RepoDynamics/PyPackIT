# JSON Schemas

The [API](#api) section of the documentation
contains a full reference of all available options
in your project's configuration and metadata files.
These are automatically generated from [JSON Schema](https://json-schema.org/)
schemas that define the exact data structure of configurations
and are used to validate user settings.
All schemas are written in [Draft 2020-12](https://json-schema.org/draft/2020-12).
If you are unfamiliar with JSON Schema specifications,
we recommend you read the [documentation](https://json-schema.org/understanding-json-schema)
to better understand the API reference documentation. 


## Default Values

JSON Schema allows for an [annotation keyword](https://json-schema.org/understanding-json-schema/reference/annotations)
named [`default`](https://json-schema.org/draft/2020-12/json-schema-validation#name-default),
which can be used to supply a default value for a schema.
|{{ ccc.name }}| uses the [`jsonschema`](https://github.com/python-jsonschema/jsonschema)
package—a Python implementation of the JSON Schema specification—to automatically
set defaults (cf. [jsonschema documentation](https://python-jsonschema.readthedocs.io/en/stable/faq/#why-doesn-t-my-schema-s-default-property-set-the-default-on-my-instance))
for control center configurations during [input validation](#manual-cc-sync).
To correctly understand the API reference,
the way these default values are applied requires some clarification:

The default value of a schema is applied to the corresponding schema's instance,
only if all parent data structures of that instance are instantiated,
and the instance itself is not present in input configurations.
The parent data structures (i.e., mappings or sequences) could be instantiated
either because they are present in input configurations, or because they
also have default values defined in the schema.
For example, consider the following minimal schema:

```yaml

type: object
properties:
  a:
    type: object
    properties:
      b:
        type: object
        default: {}
        properties:
          c:
            type: integer
            default: 0
```

Here, we have a top-level object (mapping) with a single property `a`,
which is another mapping with a single property `b`,
which is another mapping with a single property `c`,
where `c` is an integer with a default value set to `0`.
While `b` defines an empty object as its default, `a` does not have a default value.
Therefore, if the input instance is an empty object (without an `a` key),
then no default value will be added and the instance remains an empty object after validation.
This is because `a` does not define a default value, nor was it present in the input.
However, if the input is `{a: {}}` (i.e., an object with key `a` set to an empty object),
then `a` is instantiated since it is present in the input.
As `a` is the only parent of `b`, this means that all parents of `b` are instantiated,
and so, `b` will also be instantiated with the defined default value (i.e., an empty object).
Now, since both `a` and `b` are instantiated, all parents of `c` are instantiated,
and `c` will thus be instantiated as well, resulting in the final output `{a: {b: {c: 0}}}`.
Note that an input of `{a: {b: {}}` will also produce the same result (
this time `b` is instantiated because it is present in the input, not due to having a default value set 
), while `{a: b: {c: 1}}` will remain as is (`c` is already instantiated in input, so the default is ignored).


:::{admonition} Conclusion
:class: important

Just because a schema has a default value does not mean that default value
will always be applied to configurations. Instead, the default is only applied
if all parents either have a default as well, or are present in the input configurations.
:::


Another thing to consider is that the default value for a schema
may be defined in the default value of one of its parent schemas.
For example, in the above case, we defined an empty object as the default of `b`,
and the default for `c` was defined in its own schema. We could instead have:

```yaml

type: object
properties:
  a:
    type: object
    properties:
      b:
        type: object
        default: {c: 0}
        properties:
          c:
            type: integer
```

Here, the default for `c` is defined as part of the default value for `b`.
Note that in this case, an input of `{a: {b: {}}` will remain unchanged,
since the default value of `b` will not be applied.
Therefore, from reading the API reference alone you cannot deduce whether
or not a default value will be applied to your configurations,
as this is also dependent on your actual configurations. 
