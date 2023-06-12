
from pathlib import Path


def main():
    print("The path is:", Path.cwd())
    return Path.cwd()


if __name__ == "__main__":
    main()