### Documentation Website

|{{ ccc.name }}| comes with a fully developed, ready to use,
yet highly customizable professional documentation website for your project,
that is automatically generated, deployed, and maintained,
with minimal effort required from your side.

#### Main Features
- The website is built with [Sphinx](https://github.com/sphinx-doc/sphinx),
  a powerful and popular documentation generator.
- It uses the [PyData Sphinx Theme](https://github.com/pydata/pydata-sphinx-theme)–the
  official theme of the [PyData](https://pydata.org/) community,
  used by many popular Python projects such as
  [NumPy](https://numpy.org/doc/stable/),
  [SciPy](https://docs.scipy.org/doc/scipy/),
  [Pandas](https://pandas.pydata.org/docs/),
  [Matplotlib](https://matplotlib.org/stable/),
  and [Jupyter](https://docs.jupyter.org/en/latest/)–to
  provide a professional and modern design.
- Sphinx's powerful templating capabilities (using [Jinja](https://jinja.palletsprojects.com/))
  are directly integrated into all source files,
  rendering most of the website's content dynamic and self-updating.
- The [MyST Parser](https://github.com/executablebooks/MyST-Parser) extension is used
  to add support for the [MyST Markdown](https://mystmd.org/) syntax,
  which provides a variety of rich features for writing technical and scientific documentation,
  such as typography, code blocks, admonitions, figures, tables, cross-references, and mathematical notation.
- The [Sphinx Design](https://github.com/executablebooks/sphinx-design) extension is used
  to include beautiful and responsive web components in the website,
  including grids, cards, dropdowns, tabs, buttons, and icons.
- Using the [sphinx-autodoc2](https://github.com/sphinx-extensions2/sphinx-autodoc2) extension,
  the website automatically generates API documentation for your Python package,
  based on the docstrings in your source code.
- With the help of the [ABlog](https://github.com/sunpy/ablog) extension,
  the website includes a full-fledged blog,
  with support for comments (using [Giscus](https://giscus.app/)),
  web feeds, and various categorization, searching, and archiving options.
- Using the [sphinxext-opengraph](https://github.com/wpilibsuite/sphinxext-opengraph) extension,
  [Open Graph](https://ogp.me/) metadata are automatically added to each page of the website,
  allowing for search engine optimization (SEO) and rich previews when sharing the website on social media.
- The [sphinxcontrib-bibtex](https://github.com/mcmtroffaes/sphinxcontrib-bibtex) extension
  is integrated into the website, enabling you to manage your project's entire bibliography
  and citations in a BibTeX file, automatically add citations to your documentation,
  and generate bibliographies and citation lists in various formats.
- The included [sphinxcontrib-mermaid](https://github.com/mgaitan/sphinxcontrib-mermaid) extension
  allows for adding complex diagrams and charts to your documentation using the
  [Mermaid](https://github.com/mermaid-js/mermaid) syntax.


#### Structure and Content

The website is fully structured according to a standardized and well-organized layout,
with seven main sections:
- [**Introduction**]{.primary-color}: A comprehensive introduction to your project,
  serving as a starting point for new users.
  It is further divided into four subsections:
  - [**Outline**]{.primary-color}: An abstract of the project, outlining its motivations, purpose, and objectives,
    along with a brief description of its main features and capabilities.
  - [**Background**]{.primary-color}: A detailed overview of the background and context of the project,
    including a brief history of the field, and a summary of the current state of the art.
  - [**Overview**]{.primary-color}: An extensive high-level overview of the project and all its functionalites,
    the problems they solve, and the benefits they provide.
  - [**Basics**]{.primary-color}: A summary of the fundamental concepts and principles
    underlying the project, and related background information.
- [**User Manual**]{.primary-color}: An in-depth user guide, providing detailed information
  on how to install, configure, and use your software,
  and explaining all its features and functionalities with examples and use cases.
- [**API Reference**]{.primary-color}: A full API reference for your Python package,
  documenting all its subpackages, modules, classes, methods, and attributes.
- [**News**]{.primary-color}: A blog for your project, where you can post release notes,
  announcements, updates, and other news,
  and share your plans and progress with the community.
- [**Contribute**]{.primary-color}: A guide for contributors, explaining how to get involved and support the project,
  share feedback, report issues, suggest new features,
  and contribute to the development and maintenance of the software.
- [**About**]{.primary-color}: General metadata about the project,
  such as credits (authors, maintainers, sponsors, acknowledgements, etc.),
  roadmap, license information, citation details, and contact information.
- [**Help**]{.primary-color}: A help section with various resources for users and contributors,
  including a FAQ page with comments, a site map with instructions on how to navigate the website,
  and a contact page with information on how to get in touch with the project's maintainers
  for further support and assistance.

Several parts of the website are either pre-filled with content, or automatically populated
using information from your project's metadata and configurations; for example:
- The website's homepage is automatically generated to include the project's logo and description,
  as defined in project's control center.
  It also includes links to the website's main sections,
  along with a brief description of each section.
- The installation guide in the user manual is automatically generated to include
  instructions for installing your package from various sources,
  including GitHub, PyPI, and if applicable, conda.
- The API reference is automatically generated to include documentation for all subpackages,
  modules, classes, methods, and attributes in your package,
  based on the docstrings in your source code.
- The blog is automatically updated with new posts for each release of your package,
  including release notes, changelogs, and links to the corresponding resources.
- The Contribute section is fully populated with information on how to contribute to the project,
  from sharing feedback and reporting issues,
  to contributing to the development and maintenance of the software.
- The About section is automatically populated with general information about the project,
  including a full list of all authors, maintainers, sponsors, and collaborators,
  license information, citation details, and contact information,
  all of which are automatically fetched from the project's metadata and configurations.
- For each new release of your package, an announcement is automatically added to the website,
  and subsequently removed after a specified period of time.

Therefore, the only remaining contents to be added to the website are practically
the introduction of the project,
and a user guide describing the functionalities of your package and how to use them.


#### Configuration and Customization

The website is fully configured and ready to use out of the box,
with all configurations and metadata for Sphinx and its theme and extensions
provided in the Sphinx configuration file, `conf.py`.
Moreover, most of these are set dynamically;
all metadata, such as project's name, authors, version, and copyright, are automatically fetched,
and many important settings can be directly configured in the project's control center, including:
- color schemes and fonts,
- logo and favicon,
- navigation bar icons and links,
- quicklinks,
- web analytics
  (using [Google Analytics](https://analytics.google.com/) and/or [Plausible](https://plausible.io/)), and
- announcement retention period.

This allows for a high degree of customization,
without needing to be familiar with all the complex configurations and settings of Sphinx and its extensions,
and without having to manually edit the Sphinx configuration file.
Nevertheless, the Sphinx configuration file is also annotated with detailed comments and references,
allowing for further advanced customizations, if needed.


#### Build and Deployment

The build and deployment process of the website is automatically carried out on the cloud,
as part of the provided GitHub Actions workflows for the repository.
After |{{ ccc.name }}| is installed in your repository,
it automatically activates and configures the [GitHub Pages](https://pages.github.com/) service
for your repository, and deploys the website.
Subsequently, every time a change that affects the website
(i.e., a change to the website's source files, the package's source code,
or the corresponding settings in the control center)
is made to one of the repository's release branches,
the website is automatically rebuilt and redeployed.
Similarly, when such changes are made to one of the development branches,
a built version of the website is automatically attached to the corresponding workflow run,
and can be downloaded as an artifact from the workflow's page on GitHub, to be viewed locally.
The website is accessible at the default GitHub Pages URL for your repository,
which is `https://<username>.github.io/<repository-name>/`,
where `<username>` is the GitHub username of the person or organization that owns the repository,
and `<repository-name>` is the name of the repository.
However, you can also configure a custom domain
for your website in the repository's control center,
and |{{ ccc.name }}| will automatically set it up for you.
|{{ ccc.name }}| also automatically generates a full configuration file for the
[Read The Docs](https://readthedocs.org/) platform,
so that you can easily build and deploy your website there as well.

