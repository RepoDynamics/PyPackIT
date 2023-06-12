
from pathlib import Path
import argparse
import json


<<<<<<< Updated upstream
def main():
    print(["3.8", "3.9"])
=======
def main(filepath):
    path = Path(filepath)
    with open(filepath) as f:
        json_obj = json.load(f)
    print(json.dumps(json_obj))
>>>>>>> Stashed changes
    return


if __name__ == "__main__":
<<<<<<< Updated upstream
    main()
=======
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath")
    args = parser.parse_args()
    main(args.filepath)
>>>>>>> Stashed changes
