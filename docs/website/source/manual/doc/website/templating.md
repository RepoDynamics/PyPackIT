
## Website Files

During website builds, the top-level configuration mapping is passed
to the Sphinx environment as an object named `ccc` (short for Control Center Configurations),
which is then made available to all website template and source files.
You can thus dynamically use all control center contents in your website
using [Jinja](https://jinja.palletsprojects.com/) syntax,
which is the default templating engine for Sphinx.
For example, to mention your package's name and Python version specification,
which can be respectively found at `$.pkg.name` and `$.pkg.python.version.spec` in the control center,
you can use the following Jinja syntax in your website content:

```md
{‎{ ccc.pkg.name }} requires Python {‎{ ccc.pkg.python.version.spec }}.
```

Assuming that the package name is `MyPackage` and its Python version specification is `>=3.10`,
the above Jinja syntax will be rendered in the built website as:

```md
MyPackage requires Python >=3.10.
```

{{ ccc.name }} also configures Sphinx to enable full Jinja templating
not only in template files but also in all other source files.
Together with the availability of the entire project configuration in the `ccc` object,
this allows you to dynamically create sophisticated contents
that are automatically updated with any changes to the control center.

:::{admonition} Learn More
:class: seealso

To learn more about templating and dynamic content generation in your website,
see the [Documentation Guide](#website).
:::
