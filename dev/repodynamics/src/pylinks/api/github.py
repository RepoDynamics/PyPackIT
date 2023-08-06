# Standard libraries
from typing import Optional
import re

# Non-standard libraries
from pylinks import request, url


BASE_URL = url("https://api.github.com")


def _response(url_segment):
    return request(url=BASE_URL / url_segment, response_type="json")


class GraphQL:
    def __init__(self, token):
        self.token = token
        return

    def query(self, query):
        return request(
            "https://api.github.com/graphql",
            verb="POST",
            json={"query": f"{{{query}}}"},
            headers={"Authorization": f"Bearer {self.token}"},
            response_type="json",
        )


class User:
    def __init__(self, username: str):
        self.username = username
        return

    def _response(self, url: str = ""):
        return _response(f"users/{self.username}/{url}")

    @property
    def info(self) -> dict:
        return self._response()

    @property
    def social_accounts(self) -> dict:
        return self._response(f"social_accounts")

    def repo(self, repo_name) -> "Repo":
        return Repo(username=self.username, repo_name=repo_name)


def user(username) -> User:
    return User(username=username)


class Repo:
    def __init__(self, username, repo_name):
        self.username = username
        self.repo_name = repo_name
        return

    def _response(self, url: str = ""):
        return _response(f"repos/{self.username}/{self.repo_name}/{url}")

    @property
    def info(self) -> dict:
        return self._response()

    @property
    def tags(self) -> list[dict]:
        return self._response(f"git/refs/tags")

    def tag_names(self, pattern: Optional[str] = None) -> list[str | tuple[str, ...]]:
        tags = [tag['ref'].removeprefix("refs/tags") for tag in self.tags]
        if not pattern:
            return tags
        pattern = re.compile(pattern)
        hits = []
        for tag in tags:
            match = pattern.match(tag)
            if match:
                hits.append(match.groups() or tag)
        return hits

    def semantic_versions(self, tag_prefix: str = "v") -> list[tuple[int, int, int]]:
        """
        Get a list of all tags from a GitHub repository that represent SemVer version numbers,
        i.e. 'X.Y.Z' where X, Y, and Z are integers.

        Parameters
        ----------
        tag_prefix : str, default: 'v'
            Prefix of tags to match.

        Returns
        -------
        A sorted list of SemVer version numbers as tuples of integers. For example:
            `[(0, 1, 0), (0, 1, 1), (0, 2, 0), (1, 0, 0), (1, 1, 0)]`
        """
        tags = self.tag_names(pattern=rf"^{tag_prefix}(\d+\.\d+\.\d+)$")
        return sorted([tuple(map(int, tag[0].split("."))) for tag in tags])


    def discussion_categories(self, access_token: str) -> list[dict[str, str]]:
        """Get discussion categories for a repository.

        Parameters
        ----------
        access_token : str
            GitHub access token.

        Returns
        -------
            A list of discussion categories as dictionaries with keys "name", "slug", and "id".

        References
        ----------
        - [GitHub Docs](https://docs.github.com/en/graphql/guides/using-the-graphql-api-for-discussions)
        -
        """
        query = f"""
            repository(name: "{self.repo_name}", owner: "{self.username}") {{
              discussionCategories(first: 25) {{
                edges {{
                  node {{
                    name
                    slug
                    id
                  }}
                }}
              }}
            }}
        """
        response: dict = GraphQL(access_token).query(query)
        discussions = [
            entry["node"]
            for entry in response["data"]["repository"]["discussionCategories"]["edges"]
        ]
        return discussions


def repo(username, repo_name) -> Repo:
    return Repo(username=username, repo_name=repo_name)
