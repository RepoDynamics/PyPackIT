import subprocess


def run(path_root: str = ".", path_config: str = "pyproject.toml"):
    cmd = ["pytest", f"--rootdir={path_root}", f"--config-file={path_config}"]
    process = subprocess.run(cmd, text=True, cwd=path_root, capture_output=False)
    return
