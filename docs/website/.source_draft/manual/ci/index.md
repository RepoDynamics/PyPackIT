# Workflows

:::{toctree}
:hidden:

actions/index
events/index
:::


# GitHub Actions Workflows
This directory contains [workflows](https://docs.github.com/en/actions/using-workflows/about-workflows)
used in the CI/CD operations of the repository.


## References
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

## Useful Links
- [Workflow security: `pull_request` vs `pull_request_target`](https://securitylab.github.com/research/github-actions-preventing-pwn-requests/)


More recently, [Ruff](https://github.com/astral-sh/ruff), a high-performance linter written in Rust,
  has gained popularity for its speed and extensive feature set.
  Ruff combines the functionality of several existing tools,
  offering a drop-in replacement for Pylint, Bandit, Flake8, Black, and Isort,
  while supporting advanced linting capabilities.
  Unlike traditional linters, Ruff can also automatically fix
  a range of issues it detects, streamlining the development process further.




\begin{table}[h!]
\centering
\begin{tabular}{|p{0.20\textwidth}|p{0.28\textwidth}|p{0.24\textwidth}|p{0.28\textwidth}|}
\textbf{Repository} & \textbf{Description} & \textbf{Deployment Method} & \textbf{Requirement}\\
\hline

\href{https://pypi.org/}{PyPI} & Python Package Index; Python's official software repository &  \href{https://docs.pypi.org/trusted-publishers/}{Trusted publishing} with \href{https://github.com/pypa/gh-action-pypi-publish}{PyPA's official GHA application} & One-time configuration on PyPI\\

\href{https://anaconda.org/}{Anaconda} & A language-agnostic repository popular in the scientific community & Anaconda client & One-time token addition as repository secret \\

\href{https://zenodo.org/}{Zenodo} & A general-purpose repository by CERN, capable of minting persistent DOIs for each deposition & Zenodo REST API & One-time token addition\\

Docker & Any Docker registry such as \href{https://hub.docker.com/}{Docker Hub} or \href{https://github.blog/news-insights/product-news/introducing-github-container-registry/}{GitHub Container Registry} & Docker client & No requirements for GitHub Container Registry; One-time token addition for other registries\\

\href{https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases}{GitHub Releases} & GitHub's general-purpose repository, similar to Zenodo & GitHub REST API & No requirements \\

\href{https://test.pypi.org/}{TestPyPI} & A separate instance of PyPI for testing purposes & Same as PyPI & One-time configuration on TestPyPI\\

\href{https://sandbox.zenodo.org/}{Zenodo Sandbox} & A separate instance of Zenodo for testing purposes & Zenodo REST API & One-time token addition\\

\end{tabular}
\caption{Indexing repositories supported by PyPackIT for automatic deployment.}
\label{table:indexing-repos}

\end{table}

The deployment is automated using [trusted publishing](https://docs.pypi.org/trusted-publishers/) with
  [PyPA's official GHA application](https://github.com/pypa/gh-action-pypi-publish),
