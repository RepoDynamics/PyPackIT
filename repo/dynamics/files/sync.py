
from pathlib import Path
import argparse
import json

from typing import Optional
from types import ModuleType


class DynamicFileSynchronizer:

    def __init__(
            self,
            metadata: dict,
            path_root: Optional[str | Path] = None,
    ):
        self._metadata: dict = metadata
        self._path_root = path_root or Path(__file__).parent.parent.parent.parent.parent
        self._path
        return

    def update_all(self):
        self.update_contributing()
        self.update_security()
        return

    def update_contributing(self):
        with open(self._metadata.paths.TEMPLATE_CONTRIBUTING) as f:
            text = f.read()
        with open(self._metadata.paths.CONTRIBUTING, "w") as f:
            f.write(
                text.format(
                    project_name=self._metadata.project.NAME,
                    url_contributors=self._metadata.urls.CONTRIBUTORS,
                    url_releases=self._metadata.urls.RELEASES,
                    url_contributing=self._metadata.urls.CONTRIBUTING,
                )
            )
        return

    def update_security(self):
        with open(self._metadata.paths.TEMPLATE_SECURITY) as f:
            text = f.read()
        with open(self._metadata.paths.SECURITY, "w") as f:
            f.write(
                text.format(
                    project_name=self._metadata.project.NAME,
                    url_security_measures=self._metadata.urls.CONTRIBUTORS,
                    url_security_report=self._metadata.urls.RELEASES,
                    email_security="armin.ariam@gmail.com",
                )
            )
        return

    def update_license(self):
        with open(self._metadata.paths.TEMPLATE_LICENSE) as f:
            text = f.read()
        with open(self._metadata.paths.LICENSE, "w") as f:
            f.write(
                text.format(
                    project_name=self._metadata.project.NAME,
                    url_license=self._metadata.urls.LICENSE,
                    license_name=self._metadata.project.LICENSE_NAME_FULL,
                    license_name_short=self._metadata.project.LICENSE_NAME_SHORT,
                    license_year=self._metadata.project.START_YEAR,
                    license_author=self._metadata.project.AUTHORS[0]["name"],
                )
            )
        return

    def create_license_file(self):
        path_licenses = PATH_REPO / 'licenses'
        license_name = {
            "GNU Affero General Public License v3 or later (AGPLv3+)": 'GNU_AGPLv3',
            "GNU Affero General Public License v3": 'GNU_AGPLv3',
            "GNU General Public License v3 or later (GPLv3+)": 'GNU_GPLv3',
            "GNU General Public License v3 (GPLv3)": 'GNU_GPLv3',
            "GNU Lesser General Public License v3 or later (LGPLv3+)": 'GNU_LGPLv3',
            "GNU Lesser General Public License v3 (LGPLv3)": 'GNU_LGPLv3',
            "MIT License": 'MIT',
            "Boost Software License 1.0 (BSL-1.0)": 'BSLv1',
            "BSD License": 'BSD_3_Clause',
            "The Unlicense (Unlicense)": 'Unlicense',
        }
        license = license_name['{{ cookiecutter.license }}']
        if license == 'GNU_LGPLv3':
            (path_licenses / 'GNU_GPLv3').rename(PATH_REPO / "LICENSE")
            (path_licenses / license).rename(PATH_REPO / "LICENSE.LESSER")
        else:
            (path_licenses / license).rename(PATH_REPO / "LICENSE")
        # Remove original licenses directory
        shutil.rmtree(path_licenses)
        return


if __name__ == "__main__":
    updater = DynamicFileSynchronizer(path_repo="/", path_metadata_variables="../../repo/metadata/variables")
    updater.update_all()
