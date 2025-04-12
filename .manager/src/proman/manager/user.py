from __future__ import annotations as _annotations

import re
from typing import TYPE_CHECKING as _TYPE_CHECKING

from loggerman import logger
import pylinks
import pyserials

import controlman.data_validator as _validator
from proman.dstruct import User
from proman.manager.contributor import ContributorManager

if _TYPE_CHECKING:
    from typing import Literal

    from github_contexts.github.payload.object.issue import Issue
    from github_contexts.github.payload.object.pull_request import PullRequest

    from proman.manager import Manager


class UserManager:
    def __init__(self, manager: Manager):
        self._manager = manager
        self._contributors = ContributorManager(manager=self._manager)
        return

    @property
    def contributors(self) -> ContributorManager:
        return self._contributors

    def from_id(self, entity_id: str | dict):
        """Get a user (member or contributor) from their ID.

        The ID can either be a string, or a dictionary with keys 'id' and 'member'.
        If it's a string, both member IDs and contributor IDs are searched,
        otherwise, the boolean value 'member' defines the search group.
        """
        if isinstance(entity_id, str):
            entity = self._manager.data["team"].get(entity_id) or self._contributors.get(entity_id)
            if not entity:
                raise ValueError(f"Person '{entity_id}' not found in team or contributor data.")
            return User(
                id=entity_id,
                member=bool(self._manager.data["team"].get(entity_id)),
                data=entity,
            )
        if entity_id["member"]:
            return self.from_member_id(entity_id["id"])
        return self.from_contributor_id(entity_id["id"])

    def from_member_id(self, member_id: str) -> User:
        member = self._manager.data["team"].get(member_id)
        if not member:
            raise ValueError(
                f"No member data found in the data branch or main data for member ID {member_id}."
            )
        return User(
            id=member_id,
            member=True,
            data=member,
        )

    def from_contributor_id(self, contributor_id: str) -> User:
        contributor = self._contributors.get(contributor_id)
        if not contributor:
            raise ValueError(
                f"No member data found in the data branch or main data for contributor ID {contributor_id}."
            )
        return User(
            id=contributor_id,
            member=False,
            data=contributor,
        )

    def from_issue_form_id(
        self, issue_form_id: str, assignment: Literal["issue", "pull", "review"]
    ) -> list[User]:
        out = []
        for member_id, member in self._manager.data["team"].items():
            member_roles = {}
            for member_role_id, member_role_priority in member.get("role", {}).items():
                role = self._manager.data["role"][member_role_id]
                issue_id_regex = role.get("assignment", {}).get(assignment)
                if issue_id_regex and re.match(issue_id_regex, issue_form_id):
                    member_roles[member_role_id] = member_role_priority
            if member_roles:
                user = User(
                    id=member_id,
                    member=True,
                    data=member,
                    current_role=member_roles,
                )
                out.append(user)
        return out

    def get_from_github_rest_id(
        self,
        github_id: int,
        add_to_contributors: bool = False,
    ) -> User:
        for member_id, member_data in self._manager.data["team"].items():
            if member_data.get("github", {}).get("rest_id") == github_id:
                return User(id=member_id, member=True, data=member_data)
        if github_id in self._contributors:
            return User(id=github_id, member=False, data=self._contributors[github_id])
        data = self.fill_entity(
            entity={"github": {"rest_id": github_id}},
        )[0]
        user = User(id=github_id, member=False, data=data)
        if add_to_contributors:
            self._contributors.add(user=user)
        return user

    def from_github_username(
        self,
        username: str,
        add_to_contributors: bool = False,
    ):
        for member_id, member_data in self._manager.data["team"].items():
            if member_data.get("github", {}).get("id") == username:
                return User(id=member_id, member=True, data=member_data)
        for contributor_id, contributor_data in self._contributors.items():
            if contributor_data.get("github", {}).get("id") == username:
                return User(id=contributor_id, member=False, data=contributor_data)
        data = self.fill_entity(
            entity={"github": {"id": username}},
        )[0]
        user = User(id=data["github"]["rest_id"], member=False, data=data)
        if add_to_contributors:
            self._contributors.add(user=user)
        return user

    def from_name_and_email(
        self,
        name: str,
        email: str,
        add_to_contributors: bool = False,
    ):
        for member_id, member_data in self._manager.data["team"].items():
            if (
                member_data["name"]["full"] == name
                and member_data.get("email", {}).get("id") == email
            ):
                return User(id=member_id, member=True, data=member_data)
        for contributor_id, contributor_data in self._contributors.items():
            if (
                contributor_data["name"]["full"] == name
                and contributor_data.get("email", {}).get("id") == email
            ):
                return User(id=contributor_id, member=False, data=contributor_data)
        user = User(
            id=f"{name}_{email}",
            member=False,
            data={"name": {"full": name}, "email": {"id": email, "url": f"mailto:{email}"}},
        )
        if add_to_contributors:
            self._contributors.add(user=user)
        return user

    def from_issue_author(
        self,
        issue: Issue | PullRequest | dict,
        add_to_contributors: bool = False,
    ) -> User:
        user = self.get_from_github_rest_id(
            issue["user"]["id"],
            add_to_contributors=add_to_contributors,
        )
        return User(
            id=user.id,
            member=user.member,
            data=user.as_dict,
            github_association=issue.get("author_association"),
        )

    def from_payload_sender(self) -> User | None:
        return (
            self.get_from_github_rest_id(self._manager.gh_context.event.sender.id)
            if self._manager.gh_context.event.sender
            else None
        )

    def fill_entity(
        self,
        entity: dict,
    ) -> tuple[dict, dict | None]:
        """Fill all missing information in an `entity` object."""

        def _get_github_user(username: str | None = None, user_id: str | None = None) -> dict:
            def add_social(name, user, url):
                socials[name] = {"id": user, "url": url}
                return

            user_info = {}
            if user_id and self._manager.cache:
                user_info = self._manager.cache.get("user", user_id)
            if user_info:
                return user_info
            user = self._manager.gh_api_bare.user_from_id(user_id) if user_id else self._manager.gh_api_bare.user(username)
            user_info = user.info
            if user_info["blog"] and "://" not in user_info["blog"]:
                user_info["blog"] = f"https://{user_info['blog']}"
            social_accounts_info = user.social_accounts
            socials = {}
            user_info["socials"] = socials
            for account in social_accounts_info:
                for provider, base_pattern, id_pattern in (
                    ("orcid", r"orcid.org/", r"([0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{3}[0-9X]{1})(.*)"),
                    ("researchgate", r"researchgate.net/profile/", r"([a-zA-Z0-9_-]+)(.*)"),
                    ("linkedin", r"linkedin.com/in/", r"([a-zA-Z0-9_-]+)(.*)"),
                    ("twitter", r"twitter.com/", r"([a-zA-Z0-9_-]+)(.*)"),
                    ("twitter", r"x.com/", r"([a-zA-Z0-9_-]+)(.*)"),
                ):
                    match = re.search(rf"{base_pattern}{id_pattern}", account["url"])
                    if match:
                        add_social(
                            provider,
                            match.group(1),
                            f"https://{base_pattern}{match.group(1)}{match.group(2)}",
                        )
                        break
                else:
                    if account["provider"] != "generic":
                        add_social(account["provider"], None, account["url"])
                    else:
                        generics = socials.setdefault("generics", [])
                        generics.append(account["url"])
                        logger.info("Unknown account", account["url"])
            if self._manager.cache:
                self._manager.cache.set("user", user_info["id"], user_info)
            return user_info

        def get_orcid_publications(orcid_id: str) -> list[dict]:
            dois = []
            if self._manager.cache:
                dois = self._manager.cache.get("orcid", orcid_id)
            if not dois:
                dois = pylinks.api.orcid(orcid_id=orcid_id).doi
                if self._manager.cache:
                    self._manager.cache.set("orcid", orcid_id, dois)
            publications = []
            for doi in dois:
                publication_data = {}
                if self._manager.cache:
                    publication_data = self._manager.cache.get("doi", doi)
                if not publication_data:
                    publication_data = pylinks.api.doi(doi=doi).curated
                    if self._manager.cache:
                        self._manager.cache.set("doi", doi, publication_data)
                publications.append(publication_data)
            return sorted(publications, key=lambda i: i["date_tuple"], reverse=True)

        def make_name(user: dict):
            username = user["login"]
            if not user.get("name"):
                logger.warning(
                    f"GitHub user {username} has no name",
                    "Setting entity to legal person",
                )
                return {"legal": username}
            if user["type"] != "User":
                return {"legal": user["name"]}
            name_parts = user["name"].split(" ")
            if len(name_parts) != 2:
                logger.warning(
                    f"GitHub user {user} has a non-standard name",
                    f"Setting entity to legal person with name '{user['name']}'.",
                )
                return {"legal": user["name"]}
            return {"first": name_parts[0], "last": name_parts[1]}

        gh_id = entity.get("github", {}).get("rest_id")
        gh_username = entity.get("github", {}).get("id")
        github_user_info = None
        if gh_id or gh_username:
            github_user_info = _get_github_user(username=gh_username, user_id=gh_id)
            for key_self, key_gh in (
                ("id", "login"),
                ("rest_id", "id"),
                ("node_id", "node_id"),
                ("url", "html_url"),
            ):
                entity["github"][key_self] = github_user_info[key_gh]
            if "name" not in entity:
                entity["name"] = make_name(github_user_info)
            for key_self, key_gh in (
                ("affiliation", "company"),
                ("bio", "bio"),
                ("avatar", "avatar_url"),
                ("website", "blog"),
                ("city", "location"),
            ):
                if not entity.get(key_self) and github_user_info.get(key_gh):
                    entity[key_self] = github_user_info[key_gh]
            if not entity.get("email", {}).get("id") and github_user_info.get("email"):
                email = entity.setdefault("email", {})
                email["id"] = github_user_info["email"]
            for social_name, social_data in github_user_info["socials"].items():
                if (
                    social_name in ("orcid", "researchgate", "linkedin", "twitter")
                    and social_name not in entity
                ):
                    entity[social_name] = social_data
        if "orcid" in entity and entity["orcid"].get("get_pubs"):
            entity["orcid"]["pubs"] = get_orcid_publications(orcid_id=entity["orcid"]["user"])
        _validator.validate(data=entity, schema="entity", before_substitution=True)
        entity_ = pyserials.NestedDict(entity)
        entity_.fill()
        return entity_(), github_user_info
