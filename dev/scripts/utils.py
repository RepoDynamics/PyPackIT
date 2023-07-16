# Standard libraries
import argparse
import json
from pathlib import Path


def main(filepath):
    with open(filepath) as f:
        json_obj = json.load(f)
    print(json.dumps(json_obj))
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath")
    args = parser.parse_args()
    main(args.filepath)
