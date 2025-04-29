from __future__ import annotations

from typing import TYPE_CHECKING

from proman import const

if TYPE_CHECKING:
    from typing import Literal


def create_releaseman_intput(
    asset_config: dict[str, dict[str, str | list[dict[str, str]]]],
    target: Literal["github", "zenodo"],
) -> list[dict]:
    """Create input parameter `assets` for ReleaseMan action.

    Parameters
    ----------
    asset_config
        Asset configuration for a platform
        with the same structure as in control center configurations,
        i.e. a dictionary where keys are user-defined asset IDs (irrelevant here),
        and values are [Release Asset](https://controlman.repodynamics.com/schema/release-asset) objects.
    target
        The target platform for the asset.

    Returns
    -------
    The `assets` input for ReleaseMan action.
    """

    def make_files(asset_files: list[dict[str, str]]) -> list[dict[str, str]]:
        files = []
        for file in asset_files:
            dir_path = (
                const.OUTPUT_RELEASE_ARTIFACT_PATH
                if file["artifact"]
                else const.OUTPUT_RELEASE_REPO_PATH
            )
            out = {
                "source": f"{dir_path}/{file['source']}",
                "destination": file["destination"],
            }
            pattern = file.get("pattern")
            if pattern:
                out["pattern"] = pattern
            files.append(out)
        return files

    top_level_keys = ["name", "format"]
    if target == "github":
        top_level_keys.extend(["label", "media_type"])

    out_assets = []
    for asset in asset_config.values():
        asset_out = {key: asset[key] for key in top_level_keys if asset.get(key)} | {
            "files": make_files(asset["files"])
        }
        out_assets.append(asset_out)
    return out_assets
