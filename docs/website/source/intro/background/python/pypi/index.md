(bg-pypi)=
# PyPI

The [Python Package Index](https://pypi.org/) (PyPI)
is the official software repository for Python packages.
It provides a centralized public platform
to publish and share Python libraries and applications,
streamlining the process of integrating third-party dependencies into projects. 
This promotes ease of access to community-contributed packages, 
facilitating rapid development and encouraging code reuse.
Hosting more than six hundred thousand projects, 
PyPI is one of the largest and most diverse ecosystems for open-source software.

PyPI works in conjunction with Python's packaging tools like [`pip`](#bg-pip)
to ensure that software can be easily installed, upgraded, and managed. 
By serving as the backbone of Python's package distribution, 
PyPI plays a crucial role in the language's scalability and accessibility.

Run by the [Python Software Foundation](#bg-psf) 
with an open-source backend named [Warehouse](https://github.com/pypi/warehouse),
PyPI is built using modern technologies and incorporates security practices 
like two-factor authentication (2FA), verified email requirements, 
and the use of the PEP 503 normalized URLs standard.
It provides features such as [API endpoints and public datasets](https://docs.pypi.org/api/),
[digital attestations](https://docs.pypi.org/attestations/),
and [organization accounts](https://docs.pypi.org/organization-accounts/).


## Project Metadata

PyPI can read the metadata of uploaded packages
and display them on the project's webpage.
While all available metadata fields are supported,
some fields such as project URLs and README
have additional [guidelines](https://docs.pypi.org/project_metadata/) 
for correct processing on PyPI.

### URLs

[Project URLs](https://packaging.python.org/en/latest/specifications/well-known-project-urls/) 
that can be [verified](https://docs.pypi.org/project_metadata/#project-urls) are
displayed with a green checkmark,
attesting that the URL is under control of the PyPI package owner at the time of verification.
For example, URLs to the package's source repository can be verified
by enabling [Trusted Publishing](#bg-pypi-trusted-pub)
for that repository. 
Moreover, PyPI recognizes a number of [patterns](https://docs.pypi.org/project_metadata/#icons) 
in URL labels and addresses to add a custom icon to the link 
(cf. [Warehouse source code](https://github.com/pypi/warehouse/blob/cd4cd6505989cf6139078d0d958b4ded2b95fa3c/warehouse/templates/packaging/detail.html#L16-L66)).
For example, following URL labels (i.e., keys of the [`project.url`] table in `pyproject.toml`)
are automatically recognized by PyPI (case-insensitive) and displayed with a custom icon:

- `home`, `homepage`, `home page`
- `download`
- `changelog`, `change log`, `changes`, `release notes`, `news`, `what's new`, `history`

Keys starting with the following terms are recognized as well:

- `documentation`, `docs`
- `issue`, `bug`, `tracker`, `report`
- `sponsor`, `funding`, `donate`, `donation`


(bg-pypi-readme)=
### README

PyPI renders the full description of the package to HTML
and displays it on the project's webpage.
In addition to plain text and HTML inputs,
it also supports [GitHub-Flavored Markdown](#bg-ghfm)
and reStructuredText.
However, like [GitHub](#bg-gh-writing), PyPI also imposes several restrictions on the supported features,
and perform additional post-processing and sanitization after rendering the contents to HTML.
This is done by PyPA's [Readme Renderer](https://github.com/pypa/readme_renderer) library,
which only allows a limited subset of HTML
[tags](https://github.com/pypa/readme_renderer/blob/04d5cfe76850192364eff344be7fe27730af8484/readme_renderer/clean.py#L20-L31)
and [attributes](https://github.com/pypa/readme_renderer/blob/04d5cfe76850192364eff344be7fe27730af8484/readme_renderer/clean.py#L33-L65).
Since these do not completely overlap with the features supported by GitHub
(e.g., GitHub [supports](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/quickstart-for-writing-on-github#adding-an-image-to-suit-your-visitors) `<picture>` elements but PyPI does not),
a separate [PyPI-friendly README](https://packaging.python.org/en/latest/guides/making-a-pypi-friendly-readme/)
is usually required for PyPI, 
to ensure that the contents are correctly rendered.

The [Twine](https://twine.readthedocs.io/) Python package---PyPI's 
recommended tool for uploading packages---has the 
[`twine check`](https://twine.readthedocs.io/en/stable/#twine-check) 
command to check the README file for PyPI compatibility.
This uses Readme Renderer under the hood,
which it only checks whether the file can be rendered by PyPI.
However, if there are unsupported HTML tags or other minor problems in the file,
`twine check` will pass, but those tags will be rendered as plain text on PyPI 
(cf. [Twine's source code](https://github.com/pypa/twine/blob/main/twine/commands/check.py)). 
Therefore, a manual investigation is usually required 
to visually investigate the rendered README file.

