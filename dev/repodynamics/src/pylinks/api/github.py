# Standard libraries
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
