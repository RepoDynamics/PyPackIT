These include README files that are displayed to users on landing pages of
project's repositories, such as GitHub, PyPI, and Anaconda, as well as
README files in different directories of the repository providing
technical information to contributors and reviewers, and
[community health files](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file).

:::{admonition} Supported Syntax
:class: dropdown info

[GitHub](https://docs.github.com/en/get-started/writing-on-github),
PyPI, and Anaconda.org all support markup languages such as Markdown and reStructuredText
for defining the contents of files.
That is, when the file extension is in a supported format (e.g., `.md`, `.rst`),
the contents are rendered as HTML on the respective platforms.
However, GitHub only allows [GitHub Flavored Markdown](https://github.github.com/gfm/) syntax,
and performs additional post-processing and sanitization after rendering the contents to HTML,
due to security concerns. This means that only a
[limited subset of HTML features](https://docs.github.com/en/get-started/writing-on-github)
are supported.
Like GitHub, PyPI and Anaconda also impose several restrictions
and perform additional post-processing and sanitization.
PyPI uses the [Readme Renderer](https://github.com/pypa/readme_renderer) library
to render the README file, which only supports a
[limited subset of HTML tags](https://github.com/pypa/readme_renderer/blob/9c2eb81301bc230f2795cf7e6dc2c23f5815ea41/readme_renderer/clean.py#L20-L31)
and [attributes](https://github.com/pypa/readme_renderer/blob/9c2eb81301bc230f2795cf7e6dc2c23f5815ea41/readme_renderer/clean.py#L33-L65).
Since these do not completely overlap with the features supported by GitHub,
a separate [PyPI-friendly README](https://packaging.python.org/en/latest/guides/making-a-pypi-friendly-readme/)
must be provided for PyPI, to ensure that the contents are correctly rendered on the package index.
