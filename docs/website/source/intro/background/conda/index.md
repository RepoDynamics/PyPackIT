# Anaconda

The Anaconda ecosystem is a comprehensive suite of tools, platforms, 
and services designed to simplify package management, environment configuration, 
and deployment in data science, machine learning, and scientific computing workflows. 
Developed and maintained by [Anaconda, Inc.](https://www.anaconda.com),
the ecosystem includes the [Anaconda.org](#bg-anaconda-org) indexing repository,
the [Conda](#bg-conda) package manager, the [Anaconda and Miniconda distributions](#bg-anaconda-dist),
community-driven resources like [conda-forge](#bg-conda-forge) and [miniforge](#bg-miniforge),
and other tools such as [mamba](#bg-mamba) and [micromamba](#bg-mamba).
This diverse ecosystem provides a powerful and flexible infrastructure 
to efficiently manage complex projects with varied dependency requirements 
across multiple platforms.
Originally designed for Python and R development,
Anaconda has since grew into a language-agnostic platform
with support for many programming languages.


(bg-anaconda-org)=
## Anaconda.org

[Anaconda.org](http://www.anaconda.org/)
is an indexing repository and cloud service
by [Anaconda Inc.](http://anaconda.com/)
for sharing and managing packages and environments.
Users can collaborate in teams 
to publish custom [conda packages](https://docs.conda.io/projects/conda/en/stable/user-guide/concepts/packages.html)
and [standard Python packages](https://docs.anaconda.com/anacondaorg/user-guide/packages/standard-python-packages/)
in private and public repositories.
Anaconda.org is a popular choice
for publishing Python packages with non-Python dependencies,
which are common in high-performance computing applications.
Similar to [PyPI](#bg-pypi) using [pip](#bg-pip),
Anaconda.org integrates with the [conda](#bg-conda) package manager, 
allowing users to easily download and install packages 
hosted on the platform using command-line tools.


(bg-conda-forge)=
## Conda-forge

[Conda-forge](https://conda-forge.org/) is a community-driven collection of recipes,
build infrastructure, and packages for the [Conda](#bg-conda) package manager.
It provides a vast [public repository](https://github.com/conda-forge/feedstocks) 
of high-quality, up-to-date packages,
many of which are not available in the [default Anaconda repository](https://repo.anaconda.com/pkgs/).
Packages on conda-forge are automatically built
and tested across multiple operating systems and architectures
using Continuous Integration (CI) systems,
and uploaded to the [conda-forge Anaconda channel](https://anaconda.org/conda-forge).
It is a widely used source for Python and non-Python packages,
especially in scientific computing and data science communities.


(bg-conda)=
## Conda

[Conda](https://docs.conda.io) 
is the core package and environment manager used across the Anaconda ecosystem.
Unlike Python's native package manager [pip](#bg-pip), 
Conda supports packages written in any language, 
including Python, R, C, and C++. 
Compared to [pip](#bg-pip), it can install any system-level binaries,
making it more similar to OS package managers like [APT](https://wiki.debian.org/apt-get).
Conda also supports creating isolated virtual environments,
allowing users to manage multiple projects with different dependencies.

Conda is an open-source software by the [Conda community](https://conda.org/)
included in the [Anaconda and Miniconda distributions](#bg-anaconda-dist).
It works with repositories such as [Anaconda.org](#bg-anaconda-org) and [conda-forge](#bg-conda-forge),
and is designed to simplify the installation and management 
of software packages and their dependencies across platforms,
with support for precompiled binary packages for faster installation. 


(bg-mamba)=
## Mamba

[Mamba](https://mamba.readthedocs.io/) is a high-performance
reimplementation of the [Conda](#bg-conda) package manager in C++,
as part of the [conda-forge](#bg-conda-forge) ecosystem.
It offers improved speed for resolving dependencies and installing packages
while maintaining compatibility with the conda ecosystem.
Mamba supports the same commands and functionality as conda,
including managing environments and installing packages
from repositories like [Anaconda.org](#bg-anaconda-org) and conda-forge.
It also introduces efficient parallel downloads
and optimized dependency resolution,
making it particularly useful for users
working with large or complex package environments.


(bg-micromamba)=
## Micromamba

[Micromamba](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html) 
is a lightweight version of Mamba 
designed for use in containerized environments. 
It requires no Python interpreter 
and is ideal for lightweight deployments and CI/CD workflows.


(bg-anaconda-dist)=
## Anaconda Distribution

[Anaconda Distribution](https://docs.anaconda.com/anaconda/) is a curated collection 
of pre-installed Python and R packages tailored for scientific computing and data science.
It simplifies Python and R development 
by bundling [Conda](#bg-conda)
and other tools like Spyder and Anaconda Navigator
with over 300 popular libraries like 
NumPy, Pandas, Matplotlib, SciPy, and scikit-learn.
Moreover, it provides access to the [Anaconda Public Repository](https://repo.anaconda.com/pkgs/)
with more than eight thousand open-source packages.


(bg-miniconda)=
## Miniconda Distribution

[Miniconda](https://docs.anaconda.com/miniconda/) 
is a lightweight version of Anaconda Distribution, 
including only Python, Conda, and a small number of other useful packages.
This allows users to install only the packages they need using Conda, 
providing greater control over their environment.


(bg-miniforge)=
## Miniforge Distribution

[Miniforge](https://github.com/conda-forge/miniforge) 
is a minimal [conda-forge](#bg-conda-forge) distribution 
maintained by the conda-forge community.
It includes [conda](#bg-conda) and [mamba](#bg-mamba), 
pre-configured to use conda-forge as the default channel.
