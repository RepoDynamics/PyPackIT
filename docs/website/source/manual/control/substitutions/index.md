# Substitutions

To eliminate any redundancy and provide your project with a high degree of flexibility
and customization, {{ pp_meta.name }} allows for complex and recursive templating
within the entire control center, meaning that you can reference and reuse
any part of the control center's contents in all other places within the control center.

:::{admonition} Substitutions in Website Content
:class: seealso
The entire content of the control center is also made available to your documentation website,
and can be used for substitutions in your website's content.
See [Manual > Usage > Website > Substitutions](../../usage/website/substitutions.md) for more information.
:::


## Syntax

Substitutions are defined using the syntax `${‎{ PATH }}`
(the whitespace between `PATH` and the curly braces is optional and ignored),
where `PATH` is the full address to the control center's content you want to substitute,
as described in [Manual > Control Center > Outputs > Metadata File](../outputs/metadata.md).
You can use this syntax to substitute any key or value, or any part of a key or value
in any YAML or TOML file within the control center.
If you use this to substitute an entire value or array element, that value or element
will have the same type as the substituted value or element.
On the other hand, if you use this to substitute a part of a string,
the substituted part will also be converted to a string.
Substitutions are evaluated recursively, meaning that you can use substitutions
to reference a content that itself contains substitutions; you only need to make sure
not to create any circular references.


## Examples
