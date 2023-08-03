# Standard libraries
import re
from pathlib import Path
from typing import Literal, Optional
import argparse
import sys
import os

# Non-standard libraries
import ruamel.yaml
from pypackit import metadata


class Templates:
    def __init__(self, metadata: dict, log: Optional[Literal["github"]] = None):
        self.metadata = metadata
        self.log = log
        self._path_root = Path(self.metadata["path"]["abs"]["root"])
        return

    def update(self):
        self.update_license()
        self.update_health_files()
        self.update_codeowners()
        self.update_package_init_docstring()
        self.update_funding()
        return

    def update_health_files(self):
        def get_allowed_paths(template_name):
            # Health files are only allowed in the root, docs, and .github directories
            return [
                Path(self.metadata["path"]["abs"]["root"]) / allowed_path_rel / f"{template_name}.md"
                for allowed_path_rel in ['.', 'docs', '.github']
            ]
        log = "<h4>Health Files</h4>\n<ul>\n"
        health_files = ["CODE_OF_CONDUCT", "CONTRIBUTING", "GOVERNANCE", "SECURITY", "SUPPORT"]
        for health_file in health_files:
            allowed_paths = get_allowed_paths(health_file)
            if not self.metadata["path"]["health_file"][health_file.casefold()]:
                # Health file is disabled; delete it if it exists
                removed = False
                for path in allowed_paths:
                    if path.exists():
                        path.unlink()
                        removed = True
                log += f"&nbsp;&nbsp;&nbsp;&nbsp;{'🔴' if removed else '⚫'}  {health_file}<br>"
                continue
            path_target = Path(
                self.metadata["path"]["abs"]["health_file"][health_file.casefold()]
            ) / f"{health_file}.md"
            if path_target not in allowed_paths:
                error = f"⛔ ERROR: Path '{path_target}' is not an allowed path for health files."
                if self.log == "github":
                    print(error)
                    sys.exit(1)
                raise ValueError(error)
            if path_target.exists():
                with open(path_target) as f:
                    text_old = f.read()
            else:
                text_old = ""
            allowed_paths.remove(path_target)
            for allowed_path in allowed_paths:
                # Again, make sure no duplicates exist
                if allowed_path.exists():
                    allowed_path.unlink()
            with open(
                Path(self.metadata["path"]["abs"]["meta"]["template"]["health_file"]) / f"{health_file}.md"
            ) as f:
                text_template = f.read()
            text_new = text_template.format(metadata=self.metadata)
            if text_old == text_new:
                # File exists and is unchanged
                log += f"&nbsp;&nbsp;&nbsp;&nbsp;⚪️  {health_file}<br>"
                continue
            elif not text_old:
                # File is being created
                log += f"&nbsp;&nbsp;&nbsp;&nbsp;🟢  {health_file}<br>"
            else:
                # File is being modified
                log += f"""
<details>
    <summary>🟣  {health_file}</summary>
    <table width="100%">
        <tr>
            <th>Before</th>
            <th>After</th>
        </tr>
        <tr>
            <td>
                <pre>
                    <code>
                        {text_old}
                    </code>
                </pre>
            </td>
            <td>
                <pre>
                    <code>
                        {text_new}
                    </code>
                </pre>
            </td> 
        </tr>
    </table>
</details>
"""
            if self.log == "github":
                with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as fh:
                    print(log, file=fh)
            with open(path_target, "w") as f:
                f.write(text_new)
            return

    def update_license(self):
        filename = self.metadata["project"]["license"]['id'].lower().rstrip("+")
        with open(
            Path(self.metadata["path"]["abs"]["meta"]["template"]["license"]) / f"{filename}.txt"
        ) as f:
            text = f.read()
        with open(self._path_root / "LICENSE", "w") as f:
            f.write(text.format(metadata=self.metadata))
        return

    def update_package_init_docstring(self):
        filename = self.metadata["project"]["license"]['id'].lower().rstrip("+")
        with open(
            Path(self.metadata["path"]["abs"]["meta"]["template"]["license"])
            / f"{filename}_notice.txt"
        ) as f:
            text = f.read()
        copyright_notice = text.format(metadata=self.metadata)
        docstring = f"""{self.metadata['project']['name']}

{self.metadata['project']['tagline']}

{self.metadata['project']['description']}

{copyright_notice}"""
        path_src = self._path_root / "src"
        path_package = path_src / self.metadata["package"]["name"]
        if not path_package.exists():
            package_dirs = [
                sub
                for sub in [sub for sub in path_src.iterdir() if sub.is_dir()]
                if "__init__.py" in [subsub.name for subsub in sub.iterdir()]
            ]
            if len(package_dirs) > 1:
                raise ValueError(f"More than one package directory found in '{path_src}'.")
            package_dirs[0].rename(path_package)
        path_init = path_package / "__init__.py"
        with open(path_init) as f:
            text = f.read()
        docstring_pattern = r"(\"\"\")(.*?)(\"\"\")"
        match = re.search(docstring_pattern, text, re.DOTALL)
        if match:
            # Replace the existing docstring with the new one
            new_text = re.sub(docstring_pattern, rf"\1{docstring}\3", text, flags=re.DOTALL)
        else:
            # If no docstring found, add the new docstring at the beginning of the file
            new_text = f'"""\n{docstring}\n"""\n{text}'
        # Write the modified content back to the file
        with open(path_init, "w") as file:
            file.write(new_text)
        return

    def update_codeowners(self):
        """

        Returns
        -------

        References
        ----------
        https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners#codeowners-syntax
        """
        max_len = max(
            [len(entry["pattern"]) for entry in self.metadata["maintainer"]["pulls"]]
        )
        text = ""
        for entry in self.metadata["maintainer"]["pulls"]:
            reviewers = " ".join([f"@{reviewer}" for reviewer in entry["reviewers"]])
            text += f'{entry["pattern"]: <{max_len}}   {reviewers}\n'
        with open(
            Path(self.metadata["path"]["abs"]["health_file"]["codeowners"]) / "CODEOWNERS", "w"
        ) as f:
            f.write(text)
        return

    def update_funding(self):
        """

        Returns
        -------

        References
        ----------
        https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/displaying-a-sponsor-button-in-your-repository#about-funding-files
        """
        path_funding_file = self._path_root / ".github" / "FUNDING.yml"
        if not self.metadata["project"]["funding"]:
            path_funding_file.unlink(missing_ok=True)
            return
        funding = dict()
        for funding_platform, users in self.metadata["project"]["funding"].items():
            if funding_platform not in [
                "community_bridge",
                "github",
                "issuehunt",
                "ko_fi",
                "liberapay",
                "open_collective",
                "otechie",
                "patreon",
                "tidelift",
                "custom",
            ]:
                raise ValueError(f"Funding platform '{funding_platform}' is not recognized.")
            if funding_platform in ["github", "custom"]:
                if isinstance(users, list):
                    if len(users) > 4:
                        raise ValueError("The maximum number of allowed users is 4.")
                    flow_list = ruamel.yaml.comments.CommentedSeq()
                    flow_list.fa.set_flow_style()
                    flow_list.extend(users)
                    funding[funding_platform] = flow_list
                elif isinstance(users, str):
                    funding[funding_platform] = users
                else:
                    raise ValueError(
                        f"Users of the '{funding_platform}' funding platform must be either "
                        f"a string or a list of strings, but got {users}."
                    )
            else:
                if not isinstance(users, str):
                    raise ValueError(
                        f"User of the '{funding_platform}' funding platform must be a single string, "
                        f"but got {users}."
                    )
                funding[funding_platform] = users
        with open(path_funding_file, "w") as f:
            ruamel.yaml.YAML().dump(funding, f)
        return

    def update_issue_forms(self):
        pass


