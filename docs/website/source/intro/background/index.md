# Background


## Python

[Python](https://www.python.org/) is a general-purpose, multi-paradigm programming language,
created by Guido van Rossum and first released in 1991.[^python-timeline]
It has since evolved into one of the most popular programming languages in the world,
consistently ranking among the top five languages in the [TIOBE Index](https://www.tiobe.com/tiobe-index/)
throughout the last decade, and topping the list since 2021.

[^python-timeline]: [G. van Rossum (2009). A Brief Timeline of Python. The History of Python](https://python-history.blogspot.com/2009/01/brief-timeline-of-python.html)

Python was designed with an emphasis on code readability and simplicity;
its high-level abstractions and straightforward syntax
have made software development accessible to a wider range of users,
while still being powerful and robust enough to support advanced applications.
Python is a dynamically typed, interpreted language, with automatic memory management,
which allows for rapid prototyping and implementation of complex concepts,
enabling users to readily develop their ideas and share them with others.

Owing to an active community of open-source developers, Python's rich ecosystem of libraries
and frameworks has grown exponentially over the years,
making it a powerful and versatile tool for a wide range of applications,
from web development, to data science, artificial intelligence, and machine learning.
Not only do large organizations like Google, NASA, and CERN use Python in many of their projects,
but it has also become the language of choice for many startups,
small businesses, and academic research groups.
For example, the majority of scientific software across various disciplines of computational sciences
are now being published as Python packages.


## GitHub

The growth of the Python ecosystem and its open-source libraries has been further accelerated
by the emergence of cloud-based platforms for version control systems (VCSs),
such as [GitHub](https://github.com),
which marked a significant shift in how software is developed, shared, and maintained.
Their purpose is to facilitate collaborative software development,
by providing a centralized location for storing code, tracking changes,
and managing contributions from multiple developers.
They are especially crucial for open-source projects,
where developers from various backgrounds contribute to a shared codebase,
and feedback from the community is an integral part of the development process.

GitHub, launched in 2008, has quickly risen to prominence
as the world's largest host of source code,
with more than 100 million developers working on over 372 million repositories,
as of November 2023 .[^github-stats]
In addition to its user-friendly interface, GitHub offers an extensive set of features
that have solidified its position in the software development landscape, including:
- **Version Control**: At its core, GitHub provides git-based version control,
  enabling developers to track changes, revert to previous states, 
  and manage different versions of their code efficiently.
- **Issue Tracking**: GitHub includes an issue tracking system that allows developers
  to report bugs, request features, and discuss improvements within the platform.
- **Collaboration Tools**: Features such as pull requests, code reviews, and branch management
  facilitate collaboration among developers, making it easier to contribute to and maintain projects.
- **Automation Tools**: GitHub allows for building continuous integration, deployment, and
  testing (CI/CD/CT) pipelines, enabling automatic testing, building, and deployment of software projects,
  directly from GitHub repositories and without the need for third-party platforms.
- **Web Hosting**: GitHub provides free web hosting for static websites stored in GitHub repositories,
  making it easier to publish documentation and other project-related content.
- **Integration**: GitHub can be readily integrated with various development tools and services,
  enhancing its utility in different stages of software development.

[^github-stats]: [GitHub (2023). Octoverse: The state of open source and rise of AI in 2023.](https://github.blog/2023-11-08-the-state-of-open-source-and-ai/)


## State of the Art

The Python programming language and its vibrant ecosystem have made software development
more accessible and efficient than ever before, enabling a diverse community of users,
from professional developers and researchers, to amateur programmers and enthusiasts,
to promptly implement their novel ideas and share their valuable work with the world.
In addition, the rise of comprehensive cloud-based services like GitHub has undeniably revolutionized
the software development process, making it easier to collaborate on projects and share code,
and streamlining the process of building, testing, documenting, deploying, and maintaining software.
However, despite these significant advancements, the current landscape of Python software development
is still not without its challenges; these render the goal of rapid development, publishing,
and maintenance of professional and effective Python software a non-trivial task,
particularly for smaller teams or projects that lack dedicated developers for each step of the process.
The following sections discuss several challenges in the current landscape of Python software development,
which often act as significant barriers to smaller development teams,
inadvertently hampering innovation and growth within the Python community.


### Setup and Configuration

The first step in developing a Python package is setting up the project directory,
which involves creating the necessary files and directories, and configuring the project structure.
This process can be tedious and time-consuming, especially for new users,
who may not be familiar with the required files and their contents.
While there are several tools available to automate this process,
they often require additional configuration and customization to suit the specific needs of the project.
Moreover, the process of setting up a project directory is only the first step;
it is often followed by a series of additional steps, such as installing dependencies,
configuring the development environment, and setting up a CI/CD pipeline,
which can be equally challenging and time-consuming.


## Code Quality and Testing


### Documentation

Documentation is an essential aspect of software development,
weaving together the intricacies of code with the clarity of language,
and contributing significantly to the usability, maintenance, and longevity of projects.
Comprehensive documentation acts as a guide, explaining functionalities, providing examples,
and clarifying complex concepts, to ensure that users, regardless of their experience level,
can fully understand and effectively utilize the software.
Moreover, in a collaborative environment, clear documentation aids new contributors in maintaining the code; 
it provides a reference to the current design and functionalities of the software,
making it easier to identify and fix issues, thereby speeding up the development process.

Historically, Python project documentation began with simple README files,
but as software complexity grew, so did the need for more structured and detailed documentation.
This gave rise to documentation generation tools like Sphinx, originally created for Python's documentation.
Sphinx revolutionized Python documentation with features like automatic API documentation generation,
support for various output formats, and extensive customization through themes and extensions.
Its ability to integrate with hosting services like Read the Docs further streamlined
the documentation process, automating deployment and versioning.

Parallel to Sphinx's evolution, MkDocs emerged, offering a lighter, Markdown-based alternative.
It catered to projects requiring quick, easy-to-write documentation,
with a focus on simplicity and user-friendliness.
The development of themes and plugins for MkDocs enhanced its functionality,
making it a popular choice for smaller-scale projects.

The landscape of documentation tools further expanded with
the introduction of Jekyll, GitHub Pages, and Docusaurus.
Each brought unique features, such as easy integration with
version control systems, blogging capabilities, and support for internationalization,
broadening the choices available to developers for their documentation needs.

Despite the advancements in tools and platforms,
the creation and maintenance of documentation present ongoing challenges.
Setting up and customizing a documentation site, particularly with Sphinx, can be daunting.
The initial configuration, designing a user-friendly layout, and structuring content require
careful consideration and sometimes, a deeper understanding of web development concepts.
Solutions like the Sphinx Quickstart tool and pre-built themes simplify this process,
but the challenge remains in tailoring the documentation to the specific needs of the project.

Deployment and hosting are other critical aspects. Integrating documentation with version control
and setting up continuous integration and delivery pipelines ensure that the documentation is 
onsistently updated alongside code changes. Tools like Read the Docs automate much of this process
for Sphinx and MkDocs, while CI/CD tools like Jenkins or GitHub Actions offer further automation possibilities.

However, the most significant ongoing challenge is ensuring that documentation
stays current with the evolving codebase. This requires a documentation-as-code approach,
where documentation is treated with the same rigor as the code itself,
undergoing regular updates and revisions. Balancing the detail and clarity of information is also crucial,
as is making the documentation accessible to a diverse audience.

Looking forward, the field of documentation for Python projects is poised for continued evolution.
As tools like Sphinx and MkDocs become more sophisticated,
integrating more seamlessly with development workflows and expanding their capabilities,
the process of creating and maintaining documentation will become more streamlined.
The focus will likely shift towards enhancing user experience,
improving accessibility, and leveraging community feedback for continuous improvement.

In conclusion, the art of documenting Python projects is an ever-evolving landscape,
with tools and practices adapting to meet the growing demands of software development.
Effective documentation remains a cornerstone of successful software projects,
bridging the gap between code and comprehension, and ensuring that software remains usable,
maintainable, and sustainable over time.


### Publishing


The popularity of Python has also led to the development of several package managers,
such as [pip](https://pip.pypa.io/en/stable/), [conda](https://docs.conda.io/en/latest/),
and [poetry](https://python-poetry.org/), which have made it easier to install and manage Python packages.
These package managers have also enabled the creation of package indexes,
such as [PyPI](https://pypi.org/), [Anaconda Cloud](https://anaconda.org/), and [TestPyPI](https://test.pypi.org/),
which provide a centralized location for publishing and sharing Python packages.



### Maintenance


### Evolving Standards


## Summary