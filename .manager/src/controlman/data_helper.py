"""Helper functions to retrieve and generate data."""

from __future__ import annotations as _annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING
import re as _re

from loggerman import logger as _logger
import pylinks as _pl
import pyserials as _ps

from controlman import data_validator as _validator

if _TYPE_CHECKING:
    from typing import Sequence, Callable
    from controlman.cache_manager import CacheManager


def team_members_with_role_types(
    get: Callable,
    role_types: str | Sequence[str],
    active_only: bool = True,
) -> list[dict]:
    """Get team members with specific role types.

    Parameters
    ----------
    role_types
        The role type(s) to filter for.
    active_only
        Whether to filter for active team members only.

    Returns
    -------
    list[dict]
        A list of dictionaries, each representing a team member.
    """
    team_data = get("team")
    role_data = get("role")
    out = []
    if isinstance(role_types, str):
        role_types = [role_types]
    for member_id, member_data in team_data.items():
        if active_only and not member_data["active"]:
            continue
        max_priority = -1
        for role_type in role_types:
            for member_role_id, member_priority in member_data.get("role", {}).items():
                member_role_type = role_data[member_role_id]["type"]
                if member_role_type == role_type:
                    max_priority = max(max_priority, member_priority)
        if max_priority > 0:
            out.append(
                (member_data | {"id": member_id}, max_priority, member_data["name"]["full_inverted"])
            )
    return [member_data for member_data, _, _ in sorted(out, key=lambda i: (i[1], i[2]), reverse=True)]


def team_members_with_role_ids(
    get: Callable,
    role_ids: str | Sequence[str],
    active_only: bool = True,
) -> list[dict]:
    """Get team members with a specific role ID.

    Parameters
    ----------
    role_ids
        The role ID(s) to filter for.
    active_only
        Whether to filter for active team members only.

    Returns
    -------
    list[dict]
        A list of dictionaries, each representing a team member.
    """
    team_data = get("team")
    out = []
    if isinstance(role_ids, str):
        role_ids = [role_ids]
    for member_id, member_data in team_data.items():
        if active_only and not member_data["active"]:
            continue
        for role_id, member_priority in member_data.get("role", {}).items():
            if role_id in role_ids:
                out.append(
                    (member_data | {"id": member_id}, role_ids.index(role_id), member_priority)
                )
                break
    return [member_data for member_data, _, _ in sorted(out, key=lambda i: (i[1], i[2]), reverse=True)]


def team_members_without_role_types(
    get: Callable,
    role_types: str | Sequence[str],
    include_other_roles: bool = True,
    active_only: bool = True,
) -> list[dict]:
    """Get team members without a specific role type.

    Parameters
    ----------
    role_types
        The role type(s) to filter out.
    include_other_roles
        Whether to include team members that have roles
        other than the excluded role types.
    active_only
        Whether to filter for active team members only.

    Returns
    -------
    list[dict]
        A list of dictionaries, each representing a team member.
    """
    team_data = get("team")
    role_data = get("role")
    out = []
    if isinstance(role_types, str):
        role_types = [role_types]
    excluded_role_types = set(role_types)
    for member_id, member_data in team_data.items():
        if active_only and not member_data["active"]:
            continue
        member_role_types = set(
            role_data[role_id]["type"] for role_id in member_data.get("role", {}).keys()
        )
        if not excluded_role_types.intersection(member_role_types):
            out.append(member_data | {"id": member_id})
            continue
        if not include_other_roles:
            continue
        if member_role_types - excluded_role_types:
            out.append(member_data | {"id": member_id})
    return out


def fill_entity(
    entity: dict,
    github_api: _pl.api.GitHub,
    cache_manager: CacheManager | None = None,
) -> tuple[dict, dict | None]:
    """Fill all missing information in an `entity` object."""

    def _get_github_user(username: str | None = None, user_id: str | None = None) -> dict:

        def add_social(name, user, url):
            socials[name] = {"id": user, "url": url}
            return

        user_info = {}
        if user_id and cache_manager:
            user_info = cache_manager.get("user", user_id)
        if user_info:
            return user_info
        user = github_api.user_from_id(user_id) if user_id else github_api.user(username)
        user_info = user.info
        if user_info["blog"] and "://" not in user_info["blog"]:
            user_info["blog"] = f"https://{user_info['blog']}"
        social_accounts_info = user.social_accounts
        socials = {}
        user_info["socials"] = socials
        for account in social_accounts_info:
            for provider, base_pattern, id_pattern in (
                ("orcid", r'orcid.org/', r'([0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{3}[0-9X]{1})(.*)'),
                ("researchgate", r'researchgate.net/profile/', r'([a-zA-Z0-9_-]+)(.*)'),
                ("linkedin", r'linkedin.com/in/', r'([a-zA-Z0-9_-]+)(.*)'),
                ("twitter", r'twitter.com/', r'([a-zA-Z0-9_-]+)(.*)'),
                ("twitter", r'x.com/', r'([a-zA-Z0-9_-]+)(.*)'),
            ):
                match = _re.search(rf"{base_pattern}{id_pattern}", account["url"])
                if match:
                    add_social(
                        provider,
                        match.group(1),
                        f"https://{base_pattern}{match.group(1)}{match.group(2)}"
                    )
                    break
            else:
                if account["provider"] != "generic":
                    add_social(account["provider"], None, account["url"])
                else:
                    generics = socials.setdefault("generics", [])
                    generics.append(account["url"])
                    _logger.info(f"Unknown account", account['url'])
        if cache_manager:
            cache_manager.set("user", user_info["id"], user_info)
        return user_info

    def get_orcid_publications(orcid_id: str) -> list[dict]:
        dois = []
        if cache_manager:
            dois = cache_manager.get("orcid", orcid_id)
        if not dois:
            dois = _pl.api.orcid(orcid_id=orcid_id).doi
            if cache_manager:
                cache_manager.set("orcid", orcid_id, dois)
        publications = []
        for doi in dois:
            publication_data = {}
            if cache_manager:
                publication_data = cache_manager.get("doi", doi)
            if not publication_data:
                publication_data = _pl.api.doi(doi=doi).curated
                if cache_manager:
                    cache_manager.set("doi", doi, publication_data)
            publications.append(publication_data)
        return sorted(publications, key=lambda i: i["date_tuple"], reverse=True)

    def make_name(user: dict):
        username = user["login"]
        if not user.get("name"):
            _logger.warning(
                f"GitHub user {username} has no name",
                f"Setting entity to legal person",
            )
            return {"legal": username}
        if user["type"] != "User":
            return {"legal": user["name"]}
        name_parts = user["name"].split(" ")
        if len(name_parts) != 2:
            _logger.warning(
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
            ("city", "location")
        ):
            if not entity.get(key_self) and github_user_info.get(key_gh):
                entity[key_self] = github_user_info[key_gh]
        if not entity.get("email", {}).get("id") and github_user_info.get("email"):
            email = entity.setdefault("email", {})
            email["id"] = github_user_info["email"]
        for social_name, social_data in github_user_info["socials"].items():
            if social_name in ("orcid", "researchgate", "linkedin", "twitter") and social_name not in entity:
                entity[social_name] = social_data
    if "orcid" in entity and entity["orcid"].get("get_pubs"):
        entity["orcid"]["pubs"] = get_orcid_publications(orcid_id=entity["orcid"]["user"])
    _validator.validate(
        data=entity,
        schema = "entity",
        before_substitution = True
    )
    entity_ = _ps.NestedDict(entity)
    entity_.fill()
    return entity_(), github_user_info



