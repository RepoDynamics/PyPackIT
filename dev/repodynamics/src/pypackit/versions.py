# Standard libraries
import re

# Non-standard libraries
import pylinks


def semver_from_github_tags(
    github_username: str, github_repo_name: str, tag_prefix: str = "v"
) -> list[tuple[int, int, int]]:
    """
    Get a list of all tags from a GitHub repository that represent SemVer version numbers,
    i.e. 'X.Y.Z' where X, Y, and Z are integers.

    Parameters
    ----------
    github_username : str
        GitHub username.
    github_repo_name : str
        GitHub repository name.
    tag_prefix : str, default: 'v'
        Prefix of tags to match.

    Returns
    -------
        A sorted list of SemVer version numbers as tuples of integers. For example:
        `[(0, 1, 0), (0, 1, 1), (0, 2, 0), (1, 0, 0), (1, 1, 0)]`
    """
    tags = pylinks.api.github.Repo(username=github_username, repo_name=github_repo_name).tags
    semver_tag_pattern = re.compile(rf"^refs/tags/{tag_prefix}(\d+\.\d+\.\d+)$")
    versions = list()
    for tag in tags:
        # Match tags that represent final versions, i.e. vN.N.N where Ns are integers
        match = semver_tag_pattern.match(tag["ref"])
        if match:
            versions.append(tuple(map(int, match.group(1).split("."))))
    return sorted(versions)
