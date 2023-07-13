
import re
from typing import Literal
from . import project


NAME: str = re.sub(r'[._-]+', '-', project.NAME.lower())
"""Name of the package.

It is derived from the package name `NAME` via normalization:
The name should be lowercased with all runs of the characters period (.), underscore (_) and hyphen (-) 
replaced with a single hyphen.

References
----------
* [Python Packaging User Guide > PyPA specifications > Package name normalization](https://packaging.python.org/en/latest/specifications/name-normalization/)
"""


DEVELOPMENT_STATUS: Literal[1,2,3,4,5,6,7] = 1
python_versions = ["3.9", "3.10", "3.11"]
cibuilds = None
operating_systems = ["ubuntu-latest", "macos-latest", "windows-latest"]




settings = {
  "name": "{{{main.project.slug_name}}}",
  "description": "{{{main.project.short_description}}}",
  "keywords": "{{{main.project.keywords}}}",
  "urls": {
    "Homepage": "",
    "Download": "",
    "News": "",
    "Documentation": "",
    "Bug Tracker": "",
    "Sponsor": "",
    "Source": ""
  },
  "classifiers": [
    "Typing :: Typed"
  ],

  "authors": "{{{credits.authors}}}",
  "maintainers": "{{{credits.maintainers}}}",

  "readme": {"file": "{{{main.local_path.readme}}}", "content-type": "text/markdown"},
  "license": {"file": "{{{main.local_path.license}}}"},
  "dynamic": None,
  "version": None,
  "requires-python": ">=3.9",
  "scripts": {},
  "gui-scripts": {},
  "entry-points": {},
  "dependencies": "{{{main.local_path.requirements.main}}}",
  "optional-dependencies": "{{{main.local_path.requirements.optional}}}"
}