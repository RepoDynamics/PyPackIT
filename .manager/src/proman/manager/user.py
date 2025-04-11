from __future__ import annotations as _annotations

import re
from typing import TYPE_CHECKING as _TYPE_CHECKING

from controlman import data_helper
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
        data = data_helper.fill_entity(
            entity={"github": {"rest_id": github_id}},
            github_api=self._manager.gh_api_bare,
            cache_manager=self._manager.cache,
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
        data = data_helper.fill_entity(
            entity={"github": {"id": username}},
            github_api=self._manager.gh_api_bare,
            cache_manager=self._manager.cache,
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
