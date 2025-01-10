# PyPackIT © 2023–2024 RepoDynamics
# SPDX-License-Identifier: AGPL-3.0-or-later

"""PyPackIT: Cloud-Native Continuous Software Engineering Automation for Python Packages on GitHub.

PyPackIT [ˈpaɪˌpækɪt] is a comprehensive <strong>cloud-based automation tool</strong> for production
of <abbr title="Findable, Accessible, Interoperable, and Reusable">FAIR</abbr> and professional
software on <strong>GitHub</strong>, in accordance with the latest engineering best practices and
standards. It is a ready-to-use software suite that streamlines the initiation, configuration,
development, publication, management, and maintenance of high-quality <strong>Python
applications</strong>. By taking charge of repetitive tasks and automatically enforcing best
practices throughout the software development life cycle, PyPackIT enables users to solely focus on
the creative aspects of their projects, while improving quality and lowering production costs. Using
latest tools and methodologies, PyPackIT offers a robust project infrastructure, including a build-
ready Python <strong>package skeleton</strong>, a fully operational <strong>test suite</strong>, an
automated <strong>documentation website</strong>, and a comprehensive <strong>control
center</strong> according to <strong>Infrastructure-as-Code</strong> and <strong>Continuous
Configuration Automation</strong> practices to enable dynamic project management and customization.
PyPackIT establishes a complete <strong>cloud-native development</strong> environment on GitHub,
integrating with its version control system, issue tracker, and pull-based model to provide a fully
<strong>automated software development workflow</strong>, complete with features like <strong>issue
management</strong>, <strong>branching model</strong>, and <strong>version scheme</strong>.
Leveraging <strong>GitHub Actions</strong>, PyPackIT implements a cloud-native development process
with specialized <strong>Continuous Integration</strong>, Deployment, Testing, Refactoring, and
Maintenance pipelines using <strong>Agile</strong>, <strong>Continuous software
engineering</strong>, and <strong>DevOps</strong> methodologies. PyPackIT is a <strong>free</strong>
and <strong>open-source</strong> software suite that readily integrates with both new and existing
projects to ensure their long-term sustainability and high quality, enabling developers to rapidly
implement their ideas and easily maintain their software.
"""  # noqa: RUF002

__all__ = ["__version_details__", "__version__"]

__version_details__: dict[str, str] = {"version": "0.0.0"}
"""Details of the currently installed version of the package,
including version number, date, branch, and commit hash."""

__version__: str = __version_details__["version"]
"""Version number of the currently installed package."""
