from __future__ import annotations as _annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING

from loggerman import logger
import mdit


if _TYPE_CHECKING:
    from typing import Literal

    from proman.manager import Manager


class DocManager:
    def __init__(self, manager: Manager):
        self._manager = manager
        return

    def license_data() -> str:
        """Create data for each license component."""
        container = mdit.block_container()
        badge_data = metadata["theme"]["badge"]
        green = badge_data["color"]["green"]
        red = badge_data["color"]["red"]
        for license_id, component in metadata.get("license", {}).get("component").items():
            container.append(f"## {component['name']}")
            badge_list = [
                {
                    "label": "SPDX License ID",
                    "args": {"message": component["id"]},
                    "alt": f"SPDX-License-ID: {component['id']}",
                    "link": component["url"]["reference"],
                },
                {"label": "Type", "args": {"message": component["type"]}},
                {
                    "label": "Custom",
                    "args": {"message": str(component["custom"]).lower()},
                    "color": red if component["custom"] else green,
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
                },
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

    def footer_template(license_path: str, version: str) -> str:
        """Create badges for footer template."""
        badge_list = [
            {
                "label": metadata["name"],
                "args": {"message": version or "0.0.0"},
                "logo": metadata["web"]["file"]["icon"]["path"],
                "logo_type": "file",
            },
            {
                "label": "Copyright",
                "args": {"message": metadata["copyright"]},
            },
            {
                "label": "SPDX License ID",
                "args": {"message": metadata["license"]["expression"]},
                "title": f"SPDX License Identifier: {metadata['license']['expression']}",
                "alt": f"SPDX License Identifier: {metadata['license']['expression']}",
                "link": license_path,
            },
        ]
        badges = mdit.element.badges(
            items=badge_list,
            service="static",
            style="flat-square",
            classes=["footer-badge"],
            separator=0,
            color=metadata["theme"]["color"]["primary"]["light"],
            color_dark=metadata["theme"]["color"]["primary"]["dark"],
            label_color="rgb(200,200,200)",
            label_color_dark="#555",
        )
        return badges.source(target="github")

    def dependency_availability() -> dict:
        """Get the availability and count of dependencies in different package repositories."""
        deps = metadata["pkg"]["dependency"]
        dep_types = ["core", "optional"]
        repos = ["pip", "conda", "apt"]
        counts = {dep_type: dict.fromkeys(["total", *repos], 0) for dep_type in dep_types}
        for core_dep in deps.get("core", {}).values():
            counts["core"]["total"] += 1
            for repo in repos:
                if repo in core_dep:
                    counts["core"][repo] += 1
        for opt_group in deps.get("optional", {}).values():
            for opt_dep in opt_group["package"].values():
                counts["optional"]["total"] += 1
                for repo in repos:
                    if repo in opt_dep:
                        counts["optional"][repo] += 1
        for dep_type in dep_types:
            count_total = counts[dep_type]["total"]
            for repo in repos:
                count_repo = counts[dep_type][repo]
                if count_repo == count_total:
                    counts[dep_type][repo] = "✅"
                elif count_repo == 0:
                    counts[dep_type][repo] = "❌"
                else:
                    counts[dep_type][repo] = f"{count_repo}/{count_total}"
        return counts

    def comma_list_of_dependencies(
        pkg: Literal["pkg", "test"], dep: Literal["core", "optional"]
    ) -> str:
        """Get a Markdown string of comma-separated dependencies for a package or test suite.

        This generates a Markdown string representing a comma-separated list
        of required or optional runtime dependencies for the package or the test suite.
        """

        def add_link(dep_id: str, dep_data: dict) -> None:
            names.append(f"[{dep_data['name']}](#dep-{pkg}-{dep_id})")
            return

        def sort_func(item: tuple[str, dict]) -> str:
            return item[1]["name"]

        src = metadata.get(pkg, {}).get("dependency", {}).get(dep)
        if not src:
            return "---"
        names = []
        if dep == "core":
            for dep_id, dep_data in sorted(src.items(), key=sort_func):
                add_link(dep_id, dep_data)
        else:
            for dep_group in src.values():
                for dep_id, dep_data in sorted(dep_group["package"].items(), key=sort_func):
                    add_link(dep_id, dep_data)
        return ", ".join(names)
