from __future__ import annotations

from typing import TYPE_CHECKING

from controlman.changelog_manager import ChangelogManager

if TYPE_CHECKING:
    from typing import Callable, Any
    from pathlib import Path


class InlineHooks:

    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.get = None
        self.changelog = ChangelogManager(repo_path=self.repo_path)
        return

    def __call__(self, get_metadata: Callable[[str, Any, bool], Any]):
        self.get = get_metadata
        self.changelog(get_metadata=get_metadata)

    def trove_classifiers(self) -> list[str]:

        def programming_language():
            base = "Programming Language :: Python"
            return [base] + [
                f"{base} :: {version}" for version in self.get(".python.version.minors") + ["3 :: Only"]
            ]

        def operating_system():
            base = "Operating System :: {}"
            trove = {
                "ubuntu": "",
                "macos": "",
                "windows": "",
            }
            out = [
                trove[runner_type] for runner_type in set(
                    [os["runner"].split("-")[0] for os in self.get(".os").values()]
                )
            ]
            if self.get(".python.pure"):
                out.append(base.format("OS Independent"))
            return out

        def development_phase():
            log = self.changelog.current_public
            ver = log.version
            phase = log.get("phase")
            if ver == "0.0.0":
                code = 1
            elif phase == "dev":
                code = 2
            elif phase == "alpha":
                code = 3
            elif phase in ("beta", "rc") or ver.startswith("0"):
                code = 4
            else:
                highest_major = max(int(version[0]) for version in self.get("project.versions"))
                if int(ver[0]) == highest_major:
                    code = 5
                else:
                    code = 6
            code_name = {
                1: "Planning",
                2: "Pre-Alpha",
                3: "Alpha",
                4: "Beta",
                5: "Production/Stable",
                6: "Mature",
                7: "Inactive",
            }
            return f"Development Status :: {code} - {code_name[code]}"

        out = programming_language() + operating_system() + [development_phase()]
        if self.get(".typed"):
            out.append("Typing :: Typed")
        return out
