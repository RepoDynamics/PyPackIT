import argparse

from . import pyproject, readme, templates


def update_readme(self):
    text = readme.ReadMe(metadata=self.metadata).header()
    with open(self._path_root / "README.md", "w") as f:
        f.write(str(text))
    return


def update_pyproject(self):
    pyproject.PyProjectTOML(metadata=self.metadata).update()
    return


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root", type=str, help="Path to the root directory.", required=False
    )
    parser.add_argument(
        "--pathfile", type=str, help="Path to the paths metadata file.", required=False
    )
    parser.add_argument(
        "--cachefile", type=str, help="Path for the cache metadata file.", required=False
    )
    parser.add_argument(
        "--output", type=str, help="Path for the output metadata file.", required=False
    )
    parser.add_argument(
        "--output_pretty",
        type=str,
        help="Path for the pretty formatted output metadata file.",
        required=False,
    )
    parser.add_argument(
        "--update_cache",
        action=argparse.BooleanOptionalAction,
        help="Force update cache metadata file.",
        required=False,
    )
    args = parser.parse_args()
    try:
        Templates(
            path_root=args.root,
            path_pathfile=args.pathfile,
            path_cache=args.cachefile,
            update_cache=args.update_cache,
        ).update()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    return


if __name__ == "__main__":
    main()




