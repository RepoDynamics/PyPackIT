
import re
from typing import Literal
from dev._ import project


cibuilds = None
operating_systems = ["ubuntu-latest", "macos-latest", "windows-latest"]

description: str = "{{{main.project.short_description}}}"
keywords: str = "{{{main.project.keywords}}}"
urls: str = {
  "Homepage": "",
  "Download": "",
  "News": "",
  "Documentation": "",
  "Bug Tracker": "",
  "Sponsor": "",
  "Source": ""
}

authors: str = "{{{credits.authors}}}"
maintainers: str = "{{{credits.maintainers}}}"

readme: str = {"file": "{{{main.local_path.readme}}}", "content-type": "text/markdown"}
license: str = {"file": "{{{main.local_path.license}}}"}
dynamic: str = None
version: str = None
requires_python: str = ">=3.9"
scripts: str = {}
gui_scripts: str = {}
entry_points: str = {}
dependencies: str = "{{{main.local_path.requirements.main}}}"
optional_dependencies: str = "{{{main.local_path.requirements.optional}}}"
