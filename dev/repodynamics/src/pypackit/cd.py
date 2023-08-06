# Standard libraries
import argparse
import json
import os
import subprocess

from . import metadata


class MergeLogger:

    def __init__(self, path_event_payload_file: str, path_root: str = None):
        with open(path_event_payload_file) as f:
            self.event = json.load(f)
        self.metadata = metadata(path_root=path_root)
        return

    def run(self):
        latest_tag = self.latest_tag()
        if not latest_tag:
            self.initial_release()
        else:
            release, docs = self.update_type()
            if any(release):
                self.release(release, latest_tag)
            elif docs:
                self.docs()
            else:
                self.maintenance()
        return

    def initial_release(self):
        log = f"""
## [{self.metadata['project']['name']} 0.0.0]({self.metadata['url']['github']['releases']['home']}/tag/v0.0.0)
This is the initial release of the project. Infrastructure is now in place to support future releases.
        """
        changelog = f"""
# Changelog
This document tracks all changes to the {self.metadata['project']['name']} API.

{log}

"""
        with open("CHANGELOG.md", "w") as f:
            f.write(changelog)
        with open(os.environ["GITHUB_OUTPUT"], "a") as fh:
            print(f"release=true", file=fh)
            print(f"docs=true", file=fh)
            print(f"tag=v0.0.0", file=fh)
        with open("RELEASE.md", "w") as f:
            f.write(log)
        return

    def release(self, release: list[bool], latest_tag: list[int]):
        log = f"## {self.event['pull_request']['title']}\n{self.event['pull_request']['body']}"
        with open("CHANGELOG.md", "a") as f:
            f.write(log)
        if release[0]:
            new_version = f"v{latest_tag[0] + 1}.0.0"
        elif release[1]:
            new_version = f"v{latest_tag[0]}.{latest_tag[1] + 1}.0"
        else:
            new_version = f"v{latest_tag[0]}.{latest_tag[1]}.{latest_tag[2] + 1}"
        with open(os.environ["GITHUB_OUTPUT"], "a") as fh:
            print(f"tag={new_version}", file=fh)
            print(f"release=true", file=fh)
            print(f"docs=true", file=fh)
        with open("RELEASE.md", "w") as f:
            f.write(log)
        return

    def docs(self):
        with open("docs/CHANGELOG.md", "a") as f:
            f.write(f"## {self.event.pull_request.title}\n{self.event.pull_request.body}\n")
        with open(os.environ["GITHUB_OUTPUT"], "a") as fh:
            print(f"docs=true", file=fh)
            print(f"release=false", file=fh)
        return

    def maintenance(self):
        with open("dev/CHANGELOG.md", "a") as f:
            f.write(f"## {self.event.pull_request.title}\n{self.event.pull_request.body}\n")
        with open(os.environ["GITHUB_OUTPUT"], "a") as fh:
            print(f"docs=false", file=fh)
            print(f"release=false", file=fh)
        return

    @property
    def labels(self):
        return [label["name"] for label in self.event["pull_request"]["labels"]]

    def update_type(self):
        release = [False, False, False]
        docs = False
        for label in self.labels:
            if label == "Deploy: docs":
                docs = True
            elif label.startswith("Release: "):
                for segment, release_type in enumerate(["major", "minor", "patch"]):
                    if label == f"Release: {release_type}":
                        release[segment] = True
        return release, docs

    @staticmethod
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


def __main__():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str, help="Path to the root directory.")
    args = parser.parse_args()
    MergeLogger(path_event_payload_file=args.path).run()
    # with open("event_workload.json", "w") as f:
    #     json.dump(event, f, indent=4)
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
