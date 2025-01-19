(bg-py)=
# Python

[Python](https://www.python.org/) is a general-purpose, multi-paradigm programming language,
created by Guido van Rossum and first released in 1991 {cite}`PythonHistory`.
It has since evolved into one of the most popular programming languages in the world,
consistently ranking among the top five throughout the last decade and topping the list since 2021,
according to the [TIOBE Index](https://www.tiobe.com/tiobe-index/).
In 2024, Python became the top language in GitHub {cite}`GitHubOctoverse2024`,
tied to its dominance in artificial intelligence and machine learning applications.
Moreover, Python is the leading programming language for scientific software development
{cite}`SurveySEPracticesInScience2, AnalyzingGitHubRepoOfPapers, DevOpsInSciSysDev`, 
widely adopted by major organizations such as CERN
{cite}`IntroducingPythonAtCERN, PythonAtCERN` and NASA {cite}`PythonAtNASA`, 
and instrumental in key scientific achievements {cite}`PythonScientificSuccessStories` 
like the discovery of gravitational waves {cite}`GravWaveDiscovery`
and black hole imaging {cite}`BlackHoleImage`.

Python is now the most recommended language for various applications 
due to its simplicity, versatility, and extensive ecosystem
{cite}`PythonBatteriesIncluded, PythonForSciComp, PythonForSciAndEng, PythonJupyterEcosystem, SciCompWithPythonOnHPC, PythonEcosystemSciComp, WhatMakesPythonFirstChoice`, 
which provides performance-optimized libraries for
array programming {cite}`NumPy`, 
fundamental algorithms {cite}`SciPy`, 
data analysis {cite}`pandas`, 
machine learning {cite}`PyTorch, Top5MLLibPython, ScikitLearn`, 
image processing {cite}`scikitImage`, 
visualization {cite}`Matplotlib, Mayavi`, 
interactive distributed computing {cite}`IPython, Jupyter, Jupyter2`, 
parallel programming {cite}`DaskAndNumba, DaskApplications`, 
and domain-specific scientific applications {cite}`Astropy, SunPy, Pangeo, MDAnalysis, Biopython, NIPY`. 

Python can readily handle complex tasks such as web integration and visualization 
that are hard to address in low-level languages {cite}`PythonEcosystemSciComp`, 
while bridging the performance gap via
optimized compilers {cite}`Cython, Numba, Pythran`, 
GPU run-time code generators {cite}`PyCUDA`, 
nd APIs for integrating low-level languages {cite}`PythonForSciComp, PythonEcosystemSciComp`. 
This adaptability enables rapid prototyping of complex applications, 
allowing developers to quickly evaluate various ideas and 
efficiently optimize the best solution {cite}`BestPracticesForSciComp`. 
The recent advancements in parallel distributed computing with Python
{cite}`SciCompWithPythonOnHPC, ParallelDistCompUsingPython, ScientistsGuideToCloudComputing, DemystPythonPackageWithCondaEnvMod, PythonAcceleratorsForHPC` 
and Jupyter {cite}`DistWorkflowsWithJupyter` 
has even motivated large high-performance computing (HPC) communities 
to shift toward Python {cite}`SoftEngForCompSci, InteractiveSupercomputingWithJupyter`. 

## Pip

[Pip](https://pip.pypa.io) is Python's official package manager maintained by [PyPA](#bg-pypa), 
used to install and manage Python packages. 
As a command-line tool often included with Python distributions, 
pip automates the installation of Python packages and their dependencies, 
significantly simplifying the setup and deployment of Python environments.

Pip can be used to download and install packages
from source distributions and binary wheels available locally or
in online repositories such as [PyPI](#bg-pypi)
and version control systems like Git.
It integrates seamlessly with Python virtual environments, 
ensuring project-specific dependency isolation.
Functionalities include version control with 
[requirement specifiers](https://pip.pypa.io/en/stable/reference/requirement-specifiers/),
bulk installation via [`requirements.txt`](https://pip.pypa.io/en/stable/reference/requirements-file-format/)
and [constraints](https://pip.pypa.io/en/stable/user_guide/#constraints-files) files,
and [editable installations](https://pip.pypa.io/en/stable/topics/local-project-installs/#editable-installs).


(bg-pypi)=
## PyPI

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


### Project Metadata

PyPI can read the metadata of uploaded packages
and display them on the project's webpage.
While all available metadata fields are supported,
some fields such as project URLs and README
have additional [guidelines](https://docs.pypi.org/project_metadata/) 
for correct processing on PyPI.

#### URLs

[Project URLs]() that can be [verified](https://docs.pypi.org/project_metadata/#project-urls) are
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
#### README

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


## Governance

Python's governance model ensures that the language continues to evolve 
in a stable, transparent, and community-driven manner. 
Initially, Python's development was overseen solely by its creator, Guido van Rossum, 
who served as the Benevolent Dictator for Life (BDFL). 
In 2018, van Rossum stepped down from this role, 
prompting the transition to a more democratic 
and structured governance model to guide Python's future development.

Python now operates under a formalized Steering Council model, 
introduced by [PEP 8016](https://peps.python.org/pep-8016/). 
The Steering Council is composed of five members elected annually by the Python core development team. 
This council has the authority to make decisions about Python's direction, 
resolve disputes, and manage contributions. 
Its decentralized structure ensures broad representation 
and encourages open discussion within the community.

Python's governance also relies on collaborative working groups, 
such as the Python Packaging Authority (PyPA) 
and the Security Response Team, 
which manage specific areas of the language's ecosystem. 
These groups are tasked with maintaining Python's core tools,
security, packaging standards, and community outreach initiatives.

Governance is further supported by Python Enhancement Proposals (PEPs), 
which serve as the formal process for introducing new features, 
improving existing functionality, and evolving Python's ecosystem. 
This process ensures that changes are well-documented, thoroughly discussed, 
and aligned with the community's needs.


(bg-psf)=
### Python Software Foundation

The [Python Software Foundation](https://www.python.org/psf-landing/) (PSF) 
is a non-profit organization responsible for advancing the Python programming language. 
The PSF manages the intellectual property rights of Python, 
organizes community events such as PyCon, 
and provides financial support for Python-related projects and initiatives. 
It fosters an inclusive, diverse community and promotes Python's global adoption
through grants, sponsorships, and outreach programs.


(bg-pypa)=
### Python Packaging Authority

The [Python Packaging Authority](https://www.pypa.io/) (PyPA) 
is a working group that develops and maintains tools and standards 
related to Python packaging and distribution. 
PyPA oversees key tools like pip, setuptools, and twine, 
and manages packaging specifications like the
[Python Packaging User Guide](https://packaging.python.org/en/latest/)
and standards such as [PEP 517](https://peps.python.org/pep-0517/)
and [PEP 621](https://peps.python.org/pep-0621/).

PyPA plays a crucial role in ensuring the reliability, 
security, and ease of Python package management, 
continually improving the Python packaging ecosystem 
to meet the needs of modern software development.


(bg-pep)=
### Python Enhancement Proposals

[Python Enhancement Proposals](https://peps.python.org/) (PEPs) 
are the primary mechanism for proposing changes, new features, improvements, 
and processes within the Python language and its ecosystem. 
PEPs serve as formal reference documents for Python's development,
providing a framework for discussion and decision-making.
They are reviewed and approved by Python’s core developers
and form a cornerstone of Python's open development model.
PEPs are categorized as:

- **Standards Track**: Propose new features or implementation details for Python.
- **Informational**: Provide general guidelines and information.
- **Process**: Suggest changes to Python's development processes or governance.

Notable examples include [PEP 8](https://peps.python.org/pep-0008/) (style guide for Python code),
[PEP 20](https://peps.python.org/pep-0020/) (The Zen of Python), and
[PEP 440](https://peps.python.org/pep-0440/) (Version Identification and Dependency Specification).
