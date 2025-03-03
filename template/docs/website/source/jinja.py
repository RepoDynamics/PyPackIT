from __future__ import annotations

from typing import TYPE_CHECKING

import mdit

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


def create_citation():
    """Create citation information for the project."""
    return


def create_license_data():
    """Create data for each license component."""
    container = mdit.block_container()
    badge_data = metadata["__data__"]["badge"]
    green = badge_data["color"]["green"]
    red = badge_data["color"]["red"]
    for license_id, component in metadata.get("license", {}).get("component").items():
        container.append(f"## {component["name"]}")
        badge_list = [
            {
                "label": "SPDX License ID",
                "args": {"message": component["id"]},
                "alt": f"SPDX-License-ID: {component["id"]}",
                "link": component["url"]["reference"],
            },
            {"label": "Type", "args": {"message": component["type"]}},
            {
                "label": "Custom",
                "args": {"message": str(component["custom"]).lower()},
                "color": red if component["custom"] else green
            },
            {
                "label": "OSI Approved",
                "args": {"message": str(component["osi_approved"]).lower()},
                "color": green if component["osi_approved"] else red,
            },
            {
                "label": "FSF Libre",
                "args": {"message": str(component["fsf_libre"]).lower()},
                "color": green if component["osi_approved"] else red,
            }
        ]
        if "trove_classifier" in component:
            badge_list.append(
                {"label": "Trove Classifier", "args": {"message": component["trove_classifier"]}}
            )
        badges = mdit.element.badges(
            items=badge_list,
            separator=badge_data["separator"],
            service="static",
            style=badge_data["style"],
            label_color=badge_data["color"]["grey"],
            color=badge_data["color"]["blue"],
            classes=["shields-badge-medium"],
        )
        container.append(mdit.element.attribute(badges, block=True, classes=["jsonschema-badges"]))
        full_text_button = f""":::{{button-ref}} {license_id.lower()}/index\n:ref-type: myst\n:color: primary\n:expand:\n\n[Read Full Text]{{.homepage-button-text}}\n:::"""
        container.append(full_text_button)
        copyright_notice = component.get("header_plain")
        if copyright_notice:
            copyright_admonition = mdit.element.admonition(
                title="Copyright Notice",
                body=copyright_notice,
                type="danger",
            )
            container.append(copyright_admonition)
        cross_refs = component["url"]["cross_refs"]
        if cross_refs:
            resources = mdit.element.unordered_list(cross_refs)
            resources_admo = mdit.element.admonition(
                title="External Resources",
                body=resources,
                type="seealso",
            )
            container.append(resources_admo)
    return container.source()


def footer_template(license_path, version):
    """Create badges for footer template."""
    badge_list = [
        {
            "label": metadata["name"],
            "args": {"message": version or "0.0.0"},
            "logo": f"source/{metadata["web"]["file"]["icon"]["rel_path"]}",
            "logo_type": "file",
        },
        {
            "label": "Copyright",
            "args": {"message": metadata["copyright"]},
        },
        {
            "label": "SPDX License ID",
            "args": {"message": metadata["license"]["expression"]},
            "title": f"SPDX License Identifier: {metadata["license"]["expression"]}",
            "alt": f"SPDX License Identifier: {metadata["license"]["expression"]}",
            "link": license_path,
        }
    ]
    badges = mdit.element.badges(
        items=badge_list,
        service="static",
        style="flat-square",
        classes=["footer-badge"],
        separator=0,
        color=metadata["color"]["primary"]["light"],
        color_dark=metadata["color"]["primary"]["dark"],
        label_color="rgb(200,200,200)",
        label_color_dark="#555"
    )
    return badges.source(target="github")
