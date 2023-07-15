
from pathlib import Path
import argparse
import json

from typing import Optional
from types import ModuleType
import importlib.util
import sys


class DynamicFileSynchronizer:

    def __init__(
            self,
            path_repo: Optional[str | Path] = "./",
            path_metadata_variables: Optional[str] = "./metadata/variables",
    ):
        # Load metadata variables as package
        spec = importlib.util.spec_from_file_location("metadata", Path(path_metadata_variables)/"__init__.py")
        metadata = importlib.util.module_from_spec(spec)
        sys.modules["metadata"] = metadata
        spec.loader.exec_module(metadata)

        self._metadata: ModuleType = metadata
        self._path_root = Path(path_repo)
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


if __name__ == "__main__":
    updater = DynamicFileSynchronizer(path_repo="/", path_metadata_variables="../../repo/metadata/variables")
    updater.update_all()
