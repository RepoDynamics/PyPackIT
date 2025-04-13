# PyPackIT © 2023–2024 RepoDynamics
# SPDX-License-Identifier: AGPL-3.0-or-later

"""PyPackIT: Cloud-Native Continuous Software Engineering Automation for Python Packages on GitHub.

PyPackIT [ˈpaɪˌpækɪt] is a comprehensive <strong>cloud-based automation tool</strong> for production
of <abbr title="Findable, Accessible, Interoperable, and Reusable">FAIR</abbr> and professional
applications on <strong>GitHub</strong>, in accordance with the latest software engineering best
practices and standards. PyPackIT is a ready-to-use software suite that streamlines the initiation,
configuration, development, publication, management, and maintenance of high-quality <strong>Python
applications</strong>. By taking charge of repetitive tasks and automatically enforcing best
practices throughout the software development life cycle, PyPackIT enables users to solely focus on
the creative aspects of their projects, while improving quality and lowering production costs. Using
latest tools and methodologies, PyPackIT offers a robust project infrastructure, including a build-
ready Python <strong>package skeleton</strong>, a fully operational <strong>test suite</strong>, an
automated <strong>documentation website</strong>, and a comprehensive <strong>control
center</strong> according to <strong>Infrastructure-as-Code</strong> and <strong>Continuous
Configuration Automation</strong> practices to enable dynamic project management and customization.
PyPackIT establishes a complete <strong>cloud development</strong> environment on GitHub,
integrating with its version control system, issue tracker,and pull-based model to provide a fully
<strong>automated software development workflow</strong> with <strong>issue management</strong>,
<strong>branching model</strong>, and <strong>versioning scheme</strong>. Leveraging <strong>GitHub
Actions</strong>, PyPackIT implements a cloud-native Agile development process using
<strong>Continuous software engineering</strong>, <strong>containerization</strong>, and
<strong>DevOps</strong> methodologies, with a full set of <strong>Continuous Integration</strong>,
Deployment, Testing, Refactoring, and Maintenance pipelines. PyPackIT is a <strong>free</strong> and
<strong>open-source</strong> software suite that readily integrates with both new and existing
projects to ensure their long-term sustainability and high quality, enabling software projects to
rapidly implement their ideas and easily maintain their products.
"""  # noqa: RUF002

__all__ = ["__version__", "__version_info__"]

__version_info__: dict[str, str] = {"version": "0.0.0"}
"""Details of the currently installed version of the package,
including version number, date, branch, and commit hash."""

__version__: str = __version_info__["version"]
"""Version number of the currently installed package."""
