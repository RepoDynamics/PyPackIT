from . import project

# The name should be normarlized;
#   see: https://packaging.python.org/en/latest/specifications/name-normalization/
name = project.PACKAGE_NAME

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