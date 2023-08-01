# Website

## Maintenance

### Managing the Table of Contents (TOCtree)
Pages that have a 'toctree' included must only have one top-level heading (h1) and no other headings.
Similarly, pages that have lower-level headings must not have a 'toctree' included,
i.e. they must be the leaf nodes of the tree.

### Managing commenting on pages
The 'News' section of the website uses [ABlog](https://ablog.readthedocs.io/) to allow creating blog posts
with categories, tags, and RSS feeds. ABlog has [integration](https://ablog.readthedocs.io/en/stable/manual/ablog-configuration-options.html#disqus-integration)
for [Disqus](https://disqus.com/) to allow commenting on blog posts.
However, there seems to be an [issue](https://github.com/sunpy/ablog/issues/229),
at least when using the [PyData Sphinx Theme](https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/ablog.html),
which breaks the page layout when Disqus is enabled.
Moreover, using ABlog's Disqus integration would only allow commenting on blog posts, and not on other pages.
Also, the comments would be stored on Disqus servers, and not on the repository, and are thus
only accessible via the Disqus API.

[Giscus](https://giscus.app/) is the alternative we are using. It is a free and open-source commenting system,
integrates with GitHub, and stores comments on GitHub discussions.
Comments can be added to any page, and are stored in the repository.

In order to Giscus to work, the [giscus app](https://github.com/marketplace/giscus)
must be installed for the repository.
With [GitHub Discussions](https://docs.github.com/en/discussions) enabled,
the Giscus app will automatically create a discussion for each page that has Giscus enabled.

To enable giscuss for a page, follow the instructions in the [Giscus documentation](https://giscus.app/).
See [Advanced Usage](https://github.com/giscus/giscus/blob/main/ADVANCED-USAGE.md) for more details.
On GitHub: https://github.com/giscus/giscus
You can also use the [provided CSS themes](https://github.com/giscus/giscus/tree/main/styles/themes)
as a starting point for customizing the look of the comments section.
These are stored in `docs/website/source/_static/css/extensions/giscus.css` on our repo.

Also see https://github.com/mrocklin/mrocklin.github.io/blob/main/_templates/layout.html
for an example of how to add Giscus to pages programmatically.

### Using GitHub to serve files
In some cases, we have to use absolute URLs to link to a file.

An example is in the Giscus script that is added to pages to enable commenting.
There, we can pass a URL to a CSS file to style the comments section.
However, when using the GitHub repository as the source of file, i.e. linking to
`https://raw.githubusercontent.com/{username}/{repo-name}/{path-to-file}`,
GitHub will serve the file with the `text/plain` MIME type, which causes problems in some browsers when
the file is not to be interpreted as plain text, for example in case of CSS and JavaScript scripts. This will
produce an error in the browser (on Chrome, right-click on page and click `inspect`) like:

> Refused to execute script from {URL} because its MIME type (text/plain) is not executable,
and strict MIME type checking is enabled.

and the script will not be executed.

To solve this, the file must be hosted on web hosting system that serves the file with the correct MIME type.
One solution is to use services like [JSDELIVR](https://www.jsdelivr.com/?docs=gh), where you can e.g. input
a GitHub URL of the file, and get a URL to the file hosted on JSDELIVR. However, these services
usually have long caching periods, which means that changes to the file will not be reflected immediately.
A better alternative is to include these files in the GitHub Pages build of the repo, and link accordingly.


### Passing variables to use in source pages
The MyST parser's `Substitutions` extension allows passing variables to use in the source pages,
however it only accepts strings and numeric values.
Fortunately, `Substitutions` also allows access to Sphinx environment variables, such as the config variables.
Therefore we register a new config variable `rd_meta` in `conf.py`, which is a dictionary of all available metadata.
we then use the `env.config` prefix to access the variable in the source pages.


### Adding metadata to pages
We use sphinxext-opengraph to add [Open Graph](https://ogp.me/) meta tags to each HTML page of the site.

PyPI: https://pypi.org/project/sphinxext-opengraph
conda-forge: https://anaconda.org/conda-forge/sphinxext-opengraph
GitHub: https://github.com/wpilibsuite/sphinxext-opengraph
Docs: https://sphinxext-opengraph.readthedocs.io/en/latest/
