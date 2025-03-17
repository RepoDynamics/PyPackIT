from __future__ import annotations

from pathlib import Path
import hashlib
import json
import subprocess

import actionman


def main(
    repo_path: str | Path,
    devcontainer_keys: list[str] | str | None = None,
    activate_env: str | None = None,
) -> dict[str, str]:
    repo_path = Path(repo_path).resolve()
    if isinstance(devcontainer_keys, str):
        devcontainer_keys = devcontainer_keys.split(",")

    metadata_filepath = repo_path / ".github/.repodynamics/metadata.json"
    if not metadata_filepath.is_file():
        raise FileNotFoundError(f"Metadata file not found: {metadata_filepath}")
    metadata = json.loads(metadata_filepath.read_text())

    out = {
        "apt_filepaths": [],
        "task_filepaths": [],
        "activate_env": activate_env,
        "env_hash": None,
        "env_filepaths": [],
        "env_names": [],
    }
    for local_dir in ["cache", "temp", "report"]:
        local_dirpath = repo_path / metadata["local"][local_dir]["path"]
        out[f"{local_dir}_dirpath"] = str(local_dirpath)
        local_dirpath.mkdir(parents=True, exist_ok=True)

    for top_key, top_value in metadata.items():
        if not top_key.startswith("devcontainer_") or (
            devcontainer_keys and top_key.removeprefix("devcontainer_") not in devcontainer_keys
        ):
            continue
        devcontainer = top_value
        if "apt" in devcontainer:
            out["apt_filepaths"].append(str(repo_path / devcontainer["path"]["apt"]))
        if "task" in devcontainer:
            out["task_filepaths"].append(str(repo_path / devcontainer["path"]["tasks_global"]))
        for env in devcontainer.get("environment", {}).values():
            if not out["activate_env"]:
                out["activate_env"] = env["name"]
            out["env_filepaths"].append(str(repo_path / env["path"]))
            out["env_names"].append(env["name"])
    out["env_hash"] = hash_files(out["env_filepaths"])

    out["branch_name"] = subprocess.run(
        ["git", "branch", "--show-current"], cwd=repo_path, capture_output=True, text=True, check=True
    ).stdout.strip()
    return out


def hash_files(filepaths: list[str]) -> str:
    """Compute a SHA256 hash for the given files.

    This calculates the hash based on the collective content of the given files.
    The order of filepaths and the filenames themselves do not affect the hash.

    Parameters
    ----------
    filepaths
        List of filepaths to hash.
    """
    file_hashes = []
    for filepath_str in filepaths:
        filepath = Path(filepath_str)
        if not filepath.is_file():
            raise FileNotFoundError(f"File not found: {filepath}")
        hash_obj = hashlib.sha256()
        with filepath.open("rb") as f:
            # Read in chunks to handle large files efficiently
            while chunk := f.read(8192):
                hash_obj.update(chunk)
        file_hashes.append(hash_obj.hexdigest())
    # Sort the individual file hashes to ensure order independence
    file_hashes.sort()
    # Compute final hash from the sorted list of hashes
    final_hash = hashlib.sha256()
    for file_hash in file_hashes:
        final_hash.update(file_hash.encode())
    return final_hash.hexdigest()


if __name__ == "__main__":
    inputs = actionman.env_var.read("ACTION_INPUTS", dict)
    outputs = main(**{k: v for k, v in inputs.items() if k not in ("load_cache",)})
    for key, value in outputs.items():
        actionman.step_output.write(key, value)
