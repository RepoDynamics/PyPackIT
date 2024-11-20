from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Sequence


metadata: dict = {}


def team_members_with_role_ids(role_ids: str | Sequence[str], active_only: bool = True) -> list[dict]:
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
    out = []
    if isinstance(role_ids, str):
        role_ids = [role_ids]
    for member_id, member_data in metadata.get("team", {}).items():
        if active_only and not member_data["active"]:
            continue
        for role_id, member_priority in member_data.get("role", {}).items():
            if role_id in role_ids:
                out.append(
                    (member_data | {"id": member_id}, role_ids.index(role_id), member_priority)
                )
                break
    return [member_data for member_data, _, _ in sorted(out, key=lambda i: (i[1], i[2]), reverse=True)]
