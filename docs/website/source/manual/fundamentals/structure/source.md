# Source Directory

The `source` directory is where all source code of your package is stored.
This directory is named `src` by default, and is located at the root of the repository.
However, you can change its name and location via the `meta` content.
{{pp_meta.name}} follows the
[Setuptools's src-layout](https://setuptools.pypa.io/en/latest/userguide/package_discovery.html#src-layout)
for package discovery.
This means that your `source` directory must contain a single top-level package directory,
which must at least contain a `__init__.py` file. The name of this top-level package directory
defines the import name of your package. You must never rename the top-level package directory directly;
instead, {{pp_meta.name}} will automatically rename it for you
when you change the package name in the `meta` content. {{pp_meta.name}} will also automatically
update all import statements in your source code to reflect the new package name.

When the repository is first initialized, {{pp_meta.name}} will automatically create the `source` directory
and the top-level package directory, along with the top-level `__init__.py` file.
Note that the docstring of the top-level `__init__.py` file is also dynamic. Therefore, while you can
change the content of the `__init__.py` file, you must never change the docstring directly, but always
through the `meta` content.
