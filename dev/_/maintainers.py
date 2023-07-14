

# from typing import NamedTuple
#
#
# class Person(NamedTuple):
#     name: str
#     username: str
#     email: str
#     website: str
#     orcid: str
#     google_scholar: str
#     researchgate: str
#     linkedin: str
#     twitter: str
#
#
#
#
#
# people = {
#
#   "owner": {
#     "name": "Armin Ariamajd",
#   },
#
#   "maintainers": [
#     {
#       "job": "",
#       "files": [],
#       "name": "Armin Ariamajd",
#       "website": "",
#       "email": "armin.ariam@fu-berlin.de",
#       "orcid": "https://orcid.org/0000-0003-1563-6987",
#       "google_scholar": "",
#       "researchgate": "https://www.researchgate.net/profile/Armin-Ariamajd",
#       "linkedin": "https://www.linkedin.com/in/armin-ariamajd/",
#       "twitter": "https://twitter.com/al___chemist"
#     }
#   ],
#
#   "authors": [
#     {
#         "is_corresponding": True,
#         "name": "Armin Ariamajd",
#         "username": "Armin-Ariamajd",
#         "email": "armin.ariam@fu-berlin.de",
#         "website": "",
#         "orcid": "https://orcid.org/0000-0003-1563-6987",
#         "google_scholar": "",
#         "researchgate": "https://www.researchgate.net/profile/Armin-Ariamajd",
#         "linkedin": "https://www.linkedin.com/in/armin-ariamajd/",
#         "twitter": "https://twitter.com/al___chemist"
#     }
#   ],
#
#   "acknowledgments": [
#   ]
#
# }

from dev._ import project

EMAIL_SECURITY: str = "armin.ariam@fu-berlin.de"


ISSUES: dict[str, list[str]] = {
    'default': [project.AUTHORS[0]],
    'bug_api': [project.AUTHORS[0]],
}
"""
Maintainers that are automatically assigned to each opened issue.

Each key is the name of an issue template form (YAML file) under './github/ISSUE_TEMPLATE/', with the leading
integer and underscore stripped; e.g. for '1_bug_api.yaml', the key is 'bug_api'.
The 'default' key is used for all other issue forms that are not explicitly named here.
The values are lists of GitHub usernames.
"""


PRS: dict[str, list[str]] = {

    '*': [project.AUTHORS[0]],

    '/*': [project.AUTHORS[0]],
    # All files and directories under the '.github' directory.
    # These are workflows (sensitive; can be exploited) and other GitHub related configs.
    '/.github/': [project.AUTHORS[0]]
}
"""
Code owners that will be automatically requested to review pull requests before merging.

Each key is a glob pattern (with slightly modified rules; see reference) to match files and directories that
a list of GitHub usernames (the value) own.  

Notes
-----
* Code owners must have write permissions for the repository.
* For code owners to be automatically requested for reviews, the option must be enabled:
https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches#require-pull-request-reviews-before-merging
* Order is important; the last matching pattern takes the most precedence.

References
----------
* GitHub documentation about code owners:
https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
"""


