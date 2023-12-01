# Custom 404 Page

Both GitHub Pages and ReadTheDocs allow you to customize your website's 404 error page,
i.e., the page that is displayed when a user tries to access a page that does not exist.
This is already implemented in the documentation website
provided to you by the {{ pp_meta.name }} template repository.


## Customization
To change the customized 404 error page of your website,
simply edit the `404.md` file in the `source` subdirectory of your website directory
(default: `./docs/website/source/404.md`).


## Implementation Details
[ReadTheDocs](https://docs.readthedocs.io/en/stable/reference/404-not-found.html)
looks for an HTML file either at `/404.html` or `/404/index.html`,
relative to the root of your documentation website, while
[GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-custom-404-page-for-your-github-pages-site)
only looks for `/404.html`.
Since your documentation website is by default built using Sphinx's `dirhtml` builder,
the `404.md` file is automatically converted to `404/index.html` by Sphinx,
and is therefore not recognized by GitHub Pages.
To solve this issue, a `404.html` file is also provided next to the `404.md` file,
which only contains a redirect to the `404/index.html` file.
Since Sphinx doesn't automatically include non-source files (i.e., files that are not `.md` or `.rst` files)
in the built website, the `404.html` file is added to the `html_extra_path` list in the `conf.py` file,
which tells Sphinx to include it in the built website as is.
This way, both ReadTheDocs and GitHub Pages will be able to find the `404.html` file,
which will then redirect them to the actual customized 404 error page at `404/index.html`.
