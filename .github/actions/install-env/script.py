"""Run the installation script."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
import shlex

import actionman
import pkgdata


def main(
    repo_path: str | Path,
    devcontainer_keys: list[str] | str | None = None,
) -> tuple[dict[str, list[str]], dict[str, str]]:
    """Run the action script."""
    repo_path = Path(repo_path).resolve()
    if devcontainer_keys and isinstance(devcontainer_keys, str):
        devcontainer_keys = devcontainer_keys.split(",")

    metadata_filepath = repo_path / ".github/.repodynamics/metadata.json"
    if not metadata_filepath.is_file():
        err_msg = f"Metadata file not found: {metadata_filepath}"
        raise FileNotFoundError(err_msg)
    metadata = json.loads(metadata_filepath.read_text())

    pkg_setup_feature_path = metadata["devfeature_pkg_setup"]["path"]

    install_script = pkgdata.import_module_from_path(
        repo_path / metadata["control"]["path"]["pkg_install_script"],
        "install_script",
    )

    out_list: dict[str, list[str]] = {
        "apt_filepaths": [],
        "bash_filepaths": [],
        "task_filepaths": [],
        "env_filepaths": [],
        "env_names": [],
        "post_commands": [],
    }
    out_str = {
        "env_hash": "",
        "branch_name": "",
    }

    for local_dir in ["cache", "temp", "report"]:
        local_dirpath = repo_path / metadata["local"][local_dir]["path"]
        out_list[f"{local_dir}_dirpath"] = str(local_dirpath)
        local_dirpath.mkdir(parents=True, exist_ok=True)

    for top_key, top_value in metadata.items():
        if (not top_key.startswith("devcontainer_")) or (
            devcontainer_keys and top_key.removeprefix("devcontainer_") not in devcontainer_keys
        ):
            continue
        devcontainer = top_value
        if "apt" in devcontainer:
            out_list["apt_filepaths"].append(str(repo_path / devcontainer["path"]["apt"]))
        if "task" in devcontainer or any(
            "task" in env for env in devcontainer.get("environment", {}).values()
        ):
            out_list["task_filepaths"].append(str(repo_path / devcontainer["path"]["tasks_global"]))
        for env in devcontainer.get("environment", {}).values():
            out_list["env_filepaths"].append(str(repo_path / env["path"]))
            out_list["env_names"].append(env["name"])

        devcontainer_features = devcontainer["container"].get("features", {})
        for feature_name, feature_data in devcontainer_features.items():
            if feature_name.endswith(pkg_setup_feature_path):
                pkg_setup_json_string = feature_data["packages"]
                break
        else:
            pkg_setup_json_string = None
        if not pkg_setup_json_string:
            continue
        pkg_setup = json.loads(pkg_setup_json_string.replace("\\\"", "\""))
        for conda_env_name, conda_env_data in pkg_setup.items():
            _, files, self_installation_cmd = install_script.DependencyInstaller(
                {k: metadata.get(k) for k in metadata if k.startswith("pypkg_")},
            ).run(
                packages=conda_env_data["packages"],
                python_version=conda_env_data.get("python_version"),
                conda_env_name=conda_env_name,
                path_to_repo=repo_path,
            )
            out_list["post_commands"].append(shlex.join(self_installation_cmd))
            filepaths = install_script.write_files(
                files,
                output_dir=out_list["temp_dirpath"],
                filename_suffix=conda_env_name,
            )
            if "conda" in filepaths:
                out_list["env_filepaths"].append(str(filepaths["conda"]))
                out_list["env_names"].append(conda_env_name)
            for source_name in ["apt", "bash"]:
                if source_name in filepaths:
                    out_list[f"{source_name}_filepaths"].append(str(filepaths[source_name]))

    out_str["env_hash"] = hash_files(out_list["env_filepaths"])
    out_str["branch_name"] = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    return out_list, out_str


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
            err_msg = f"File not found: {filepath}"
            raise FileNotFoundError(err_msg)
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
    action_logger = actionman.log.Logger()
    inputs = actionman.env_var.read("ACTION_INPUTS", dict)
    out_list, out_str = main(**{k: v for k, v in inputs.items() if k not in ("load_cache", "activate_env")})
    action_logger.group(
        json.dumps(out_str | out_list, indent=3, sort_keys=True),
        title="Script Outputs",
    )
    for key, value in out_list.items():
        out_val = ("\n".join(value))
        actionman.step_output.write(key, out_val)
    for key, value in out_str.items():
        actionman.step_output.write(key, value)
