"""PyPackIT Test-Suite

Copyright (C) 2023 RepoDynamics

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""  # noqa: D400


import subprocess


def run(path_root: str = ".", path_config: str = "pyproject.toml"):
    """Run the test-suite."""
    process = subprocess.run(
        ["pytest", f"--rootdir={path_root}", f"--config-file={path_config}"],
        text=True,
        cwd=path_root,
        capture_output=False,
        check=True
    )
    return
