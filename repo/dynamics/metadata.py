# Standard libraries
import datetime
import json
import re
from pathlib import Path

# Non-standard libraries
import requests
from ruamel.yaml import YAML


def read_metadata(dir_path: str | Path) -> dict:
    metadata_dir = Path(dir_path).resolve()
    if not (metadata_dir.exists() and metadata_dir.is_dir()):
        raise ValueError(
            f"Metadata directory '{metadata_dir}' does not exist or is not a directory."
        )
    metadata = dict()
    for metadata_file in metadata_dir.glob("*.yaml"):
        metadata[metadata_file.stem] = dict(YAML().load(metadata_file))
    return metadata


def verify_project_name(name: str) -> None:
    if not re.match(r"^([A-Z0-9]|[A-Z0-9][A-Z0-9._-]*[A-Z0-9])$", name, flags=re.IGNORECASE):
        raise ValueError(
            "Project name must only consist of alphanumeric characters, period (.), underscore (_) and hyphen (-), "
            f"and can only start and end with an alphanumeric character, but got {name}. "
            "See https://packaging.python.org/en/latest/specifications/name-normalization/ for more details."
        )
    return


def verify_project_start_year(year: int | str) -> None:
    year = int(year)
    if year < 1970 or year > datetime.date.today().year:
        raise ValueError(
            f"Project's start year must be between 1970 and {datetime.date.today().year}, but got {year}."
        )
    return


def verify_github_repo_name(name: str) -> None:
    if not re.match(r"^[A-Za-z0-9_.-]+$", name):
        raise ValueError(
            "Repository names can only contain alphanumeric characters, hyphens (-), underscores (_), and dots (.), "
            f"but got {name}."
        )


def github_user_info(username) -> dict:
    response = requests.get(f"https://api.github.com/users/{username}")
    response.raise_for_status()
    info = response.json()
    info["external_urls"] = {"website": info["blog"]}
    response2 = requests.get(f"https://api.github.com/users/{username}/social_accounts")
    response2.raise_for_status()
    social_accounts = response2.json()
    for account in social_accounts:
        if account["provider"] == "twitter":
            info["external_urls"]["twitter"] = account["url"]
        elif account["provider"] == "linkedin":
            info["external_urls"]["linkedin"] = account["url"]
        else:
            url_pattern = "(?:https?://)?(?:www\.)?({}/[\w\-]+)"
            for url, key in [
                ("orchid\.org", "orcid"),
                ("researchgate\.net/profile", "researchgate"),
            ]:
                match = re.compile(url_pattern.format(url)).fullmatch(account["url"])
                if match:
                    info["external_urls"][key] = f"https://{match.group(1)}"
                    break
    return info


def github_repo_info(username, repo_name) -> dict:
    response = requests.get(f"https://api.github.com/repos/{username}/{repo_name}")
    response.raise_for_status()
    info = response.json()
    return info


def generate_package_name(project_name: str) -> str:
    return re.sub(r"[._-]+", "-", project_name.lower())


def main(path_metadata: str | Path = None) -> dict:
    path = (
        Path(path_metadata).resolve()
        if path_metadata
        else Path(__file__).parent.parent / "metadata"
    )
    metadata = read_metadata(path)

    verify_project_start_year(metadata["project"]["start_year"])

    metadata["project"]["owner"] = github_user_info(metadata["project"]["github"]["username"])
    metadata["project"]["authors"] = [
        github_user_info(author) for author in metadata["project"]["authors"]
    ]
    metadata["project"]["github"] = github_repo_info(
        metadata["project"]["github"]["username"], metadata["project"]["name"]
    )
    # TODO
    metadata["project"]["license_name_short"] = ""
    metadata["project"]["license_name_full"] = ""

    if not metadata["project"].get("name"):
        metadata["project"]["name"] = metadata["project"]["github"]["name"]
    verify_project_name(metadata["project"]["name"])

    metadata["package"]["name"] = generate_package_name(metadata["project"]["name"])

    metadata["url"] = dict()

    metadata["url"]["homepage"] = (
        f"https://{metadata['website']['rtd_name']}.readthedocs.io/en/latest"
        if metadata["website"].get("rtd_name")
        else (
            f"https://{metadata['project']['owner']['login']}.github.io"
            f"""{"" if metadata['website']['is_gh_user_site'] else f"/{metadata['project']['github']['name']}"}"""
        )
    )
    metadata["url"]["announcement"] = (
        f"https://raw.githubusercontent.com/{metadata['project']['github']['full_name']}/"
        f"{metadata['project']['github']['default_branch']}/{metadata['paths']['website_sphinx_announcement']}"
    )
    metadata["url"]["contributors"] = f"{metadata['url']['homepage']}/about#contributors"
    metadata["url"]["license"] = f"{metadata['url']['homepage']}/license"

    metadata["url"]["gh_repo"] = metadata["project"]["github"]["html_url"]
    metadata["url"]["gh_issues"] = f"{metadata['url']['gh_repo']}/issues"
    metadata["url"]["gh_pulls"] = f"{metadata['url']['gh_repo']}/pulls"
    metadata["url"]["gh_discussions"] = f"{metadata['url']['gh_repo']}/discussions"
    metadata["url"]["gh_releases"] = f"{metadata['url']['gh_repo']}/releases"

    metadata["url"]["pypi"] = f"https://pypi.org/project/{metadata['package']['name']}/"

    return metadata


if __name__ == "__main__":
    # Standard libraries
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--path", type=str, help="Path to the metadata directory.", required=False
    )
    args = parser.parse_args()
    path = Path(args.path).resolve() if args.path else Path(__file__).parent.parent / "metadata"
    try:
        metadata = main(path)
        with open(path / "metadata_full.json", "w") as f:
            json.dump(metadata, f, indent=4)
        print(json.dumps(main(path)))
    except Exception as e:
        # Standard libraries
        import sys

        print(f"Error: {e}")
        sys.exit(1)
