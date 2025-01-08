(intro-jinja)=
# Jinja

[Jinja](https://jinja.palletsprojects.com/) is a fast and flexible templating engine for Python, 
commonly used to dynamically generate HTML, configuration files, or other text-based formats. 
It allows embedding Python-like expressions and control structures within templates 
using a concise syntax, such as `{{ }}` for variable interpolation
and `{% %}` for logic statements like loops and conditionals. 
Jinja supports features like template inheritance, macros, filters, and extensions, 
enabling reusable and modular templates. 
Widely adopted in web frameworks like Flask and for tools like Ansible, 
Jinja simplifies rendering dynamic content in various contexts.


## Variables

Jinja templates can access variables passed into the template and render them dynamically.
For example, a template `Hello, {{ name }}!` with the variable
`name` set to `"Alice"` will render as `Hello, Alice!`.


## Filters

Filters are used to transform data in templates.
Common Filters include:
- `upper`: Converts a string to uppercase.
- `lower`: Converts a string to lowercase.
- `length`: Returns the length of a collection.
- `default`: Sets a default value if the variable is undefined.

Filters are applied using a pipe (`|`). For example,
a template `{{ name|upper }}` with the variable `name` set to `"Alice"`
will render as `ALICE`.


## Loops

Use `{% for %}` to iterate over items:

```jinja
{% for item in items %}
- {{ item }}
{% endfor %}
```

**Output:**
```
- apple
- banana
- cherry
```

## Conditionals
Use `{% if %}`, `{% elif %}`, and `{% else %}` for conditional logic.

```jinja
{% if user.is_admin %}
Welcome, admin!
{% else %}
Welcome, user!
{% endif %}
```


## Macros
Macros are reusable blocks of code within templates.

```jinja
{% macro greet(name) %}
Hello, {{ name }}!
{% endmacro %}

{{ greet("Alice") }}
```


## Resources
- [Jinja Documentation](https://jinja.palletsprojects.com/)
- [Jinja GitHub Repository](https://github.com/pallets/jinja)
