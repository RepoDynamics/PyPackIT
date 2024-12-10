# PyPackIT © 2023–2024 RepoDynamics
# SPDX-License-Identifier: AGPL-3.0-or-later

"""PyPackIT: Cloud-Native Continuous Software Engineering Automation for Python Packages on GitHub.

PyPackIT [ˈpaɪˌpækɪt] is a comprehensive <strong>cloud-based automation tool</strong> for production
of <abbr title="Findable, Accessible, Interoperable, and Reusable">FAIR</abbr> and professional
software on <strong>GitHub</strong>, in accordance with the latest engineering best practices and
standards. It is a ready-to-use software suite that streamlines the initiation, configuration,
development, publication, management, and maintenance of high-quality software libraries in
<strong>Python</strong>. By taking charge of repetitive tasks and automatically enforcing best
practices throughout the software development life-cycle, PyPackIT enables users to solely focus on
the creative aspects of their projects, while improving quality and lowering production costs. Using
state-of-the-art tools and methodologies, PyPackIT offers a robust project infrastructure, including
a build-ready Python <strong>package skeleton</strong>, a fully operational <strong>test
suite</strong>, a complete <strong>documentation website</strong>, and a comprehensive
<strong>control center</strong> facilitating Continuous Configuration Automation (CCA) and dynamic
project management. PyPackIT establishes a complete <strong>cloud-native development</strong>
environment on GitHub, integrating with its version control system, issue tracker, and pull-based
model to provide a fully automated software development workflow, complete with features like
<strong>issue management</strong>, <strong>branching model</strong>, and <strong>version
scheme</strong>. Leveraging <strong>GitHub Actions</strong> (GHA), PyPackIT implements a cloud-
native development process with specialized Continuous Integration (CI), Deployment (CD), Testing
(CT), Refactoring (CR), and Maintenance (CM) pipelines, using <strong>Agile</strong>,
<strong>Continuous software engineering</strong>, and <strong>DevOps</strong> methodologies.
PyPackIT is a free and open-source software suite that readily integrates with both new and existing
projects to ensure their long-term sustainability and high quality, thus enabling developers to
rapidly implement their ideas and easily maintain their software.
"""  # noqa: RUF002

__all__ = ["__version_details__", "__version__"]

__version_details__: dict[str, str] = {"version": "0.0.0"}
"""Details of the currently installed version of the package,
including version number, date, branch, and commit hash."""

__version__: str = __version_details__["version"]
"""Version number of the currently installed package."""
