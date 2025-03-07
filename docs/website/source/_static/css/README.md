# CSS Stylesheets

This directory contains CSS stylesheets for the website.
All `.css` and `.css_t` files are automatically
added to the `html_css_files` list
in Sphinx's `conf.py` configuration file,
and are thus included in the website's stylesheets.
Note that `.css_t` files can contain Jinja templates
that are evaluated during builds.

Stylesheets are categorized into the following files and subdirectories:

- `theme/`: Stylesheets specific to the HTML theme of the website.
- `extensions/`: Stylesheets specific to different extensions used in the website.
  Each file corresponds to an extension.
- `custom/`: Custom stylesheets unrelated to the theme and other extensions.
- `dynamic.css_t`: Applies dynamic stylesheets defined in control center configurations.


## References

For `pydata-sphinx-theme` stylesheets, see:
- [PyData Documentation](https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/styling.html)
- [PyData GitHub Repo](https://github.com/pydata/pydata-sphinx-theme/tree/main/src/pydata_sphinx_theme/assets/styles)
