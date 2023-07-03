
from pathlib import Path
import argparse
import json


def main():
    with open("./metadata/templates/CONTRIBUTING.md") as f:
        text = f.read()
    with open("./docs/CONTRIBUTING.md", "w") as f:
        f.write(text.format(project_name="PyPackIT"))
    return


if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument("filepath")
    # args = parser.parse_args()
    # main(args.filepath)
    main()
