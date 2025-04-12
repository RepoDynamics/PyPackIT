"""Helper functions to retrieve and generate data."""

from __future__ import annotations as _annotations

import re as _re
from typing import TYPE_CHECKING as _TYPE_CHECKING

import pylinks as _pl
import pyserials as _ps
from loggerman import logger as _logger

from controlman import data_validator as _validator

if _TYPE_CHECKING:
    from collections.abc import Callable, Sequence

    from proman.manager.cache import CacheManager


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
                (
                    member_data | {"id": member_id},
                    max_priority,
                    member_data["name"]["full_inverted"],
                )
            )
    return [
        member_data for member_data, _, _ in sorted(out, key=lambda i: (i[1], i[2]), reverse=True)
    ]


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
    return [
        member_data for member_data, _, _ in sorted(out, key=lambda i: (i[1], i[2]), reverse=True)
    ]


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
