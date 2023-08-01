# Standard libraries
import argparse
import json
import subprocess


def latest_tag() -> list[int] | None:
    git_describe = subprocess.run(
        args=["git", "describe", "--match", "v[0-9]*.[0-9]*.[0-9]*", "--abbrev=0"],
        capture_output=True,
    )
    return (
        list(map(int, git_describe.stdout.decode().strip().removeprefix("v").split(".")))
        if git_describe.returncode == 0
        else None
    )


def func(event: dict):
    pass


def __main__():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str, help="Path to the root directory.")
    args = parser.parse_args()
    with open(args.path, "r") as f:
        event = json.load(f)
    with open("event_workload.json", "w") as f:
        json.dump(event, f, indent=4)
    # try:
    #     meta = Metadata(
    #         path_root=args.root,
    #         path_pathfile=args.pathfile,
    #         path_cache=args.cachefile,
    #         update_cache=args.update_cache,
    #     )
    # except Exception as e:
    #     print(f"Error: {e}")
    #     sys.exit(1)
    # # print(meta.json())
    # meta.json(write_to_file=True, output_filepath=args.output)
    # meta.json(write_to_file=True, output_filepath=args.output_pretty, indent=4)
    return


if __name__ == "__main__":
    __main__()
