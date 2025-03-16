from __future__ import annotations

import argparse
from typing import TYPE_CHECKING
import re

from loggerman import logger
import mdit
import pyshellman as _pyshellman
import ansi_sgr as sgr
from gittidy import Git

if TYPE_CHECKING:
    from typing import Literal


def run(
    config: str,
    action: Literal["report", "run", "validate"] = "run",
    hook_id: str | None = None,
    hook_stage: str | None = None,
    files: list[str] | None = None,
    all_files: bool = False,
    ref_range: tuple[str, str] | None = None,
):
    hook_runner = PreCommitHooks(
        config=config,
        action=action,
        hook_id=hook_id,
        hook_stage=hook_stage,
        files=files,
        all_files=all_files,
        ref_range=ref_range,
    )
    return hook_runner.run()


class PreCommitHooks:

    def __init__(
        self,
        config: str,
        action: Literal["report", "run", "validate"] = "run",
        hook_id: str | None = None,
        hook_stage: str | None = None,
        files: list[str] | None = None,
        all_files: bool = False,
        ref_range: tuple[str, str] | None = None,
    ):
        logger.info(
            "Pre-Commit",
            f"Running Pre-Commit hooks in '{action}' mode.",
            f"Ref Range: {ref_range}",
        )
        if action not in ["report", "run", "validate"]:
            raise ValueError(f"Invalid action '{action}'.")
        if hook_id and hook_stage:
            raise ValueError("Only one of 'hook_id' or 'hook_stage' can be specified.")
        if sum(bool(file_input) for file_input in (files, all_files, ref_range)) > 1:
            raise ValueError("Only one of 'files', 'all_files', or 'ref_range' can be specified.")
        if ref_range and not (
            isinstance(ref_range, (tuple, list))
            and len(ref_range) == 2
            and all(isinstance(ref, str) for ref in ref_range)
        ):
            raise ValueError(
                f"Argument 'ref_range' must be a list or tuple of two strings, but got {ref_range}.")
        version_result = _pyshellman.run(
            command=["pre-commit", "--version"],
            raise_execution=False,
            raise_exit_code=False,
            raise_stderr=False,
            text_output=True,
        )
        logger.log(
            "success" if version_result.succeeded else "critical",
            "Pre-Commit: Check Version",
            version_result.report(),
        )
        self._git = Git(path=config, logger=logger)
        self._action = action
        self._path_root = self._git.repo_path

        self._from_ref = ref_range[0] if ref_range else None
        self._to_ref = ref_range[1] if ref_range else None
        self._files = files
        self._hook_id = hook_id
        self._hook_stage = hook_stage

        self._command = [
            part for part in [
                "pre-commit",
                "run",
                hook_id,
                "--config",
                config,
                "--color=always",
                "--show-diff-on-failure",
                "--verbose",
                "--hook-stage" if hook_stage else None,
                hook_stage,
                "--all-files" if all_files else None,
                "--files" if files else None,
                *(files or []),
                "--from-ref" if ref_range else None,
                self._from_ref,
                "--to-ref" if ref_range else None,
                self._to_ref,
            ] if part
        ]

        self._shell_runner = _pyshellman.Runner(
            pre_command=self._command,
            cwd=self._path_root,
            raise_exit_code=False,
            logger=logger,
            stack_up=1,
        )
        self._emoji = {"Passed": "✅", "Failed": "❌", "Skipped": "⏭️", "Modified": "✏️️"}
        self._dropdown_color = {"Passed": "success", "Failed": "danger", "Skipped": "muted", "Modified": "warning"}
        self._commit_hash: str = ""
        return

    def run(self) -> dict:
        logger.info("Run Mode", self._action)
        if self._action == "report":
            self._git.stash(include="all")
        output_first = self._run_hooks(validation_run=self._action != "validate")
        if self._action == "report":
            self._git.discard_changes()
            self._git.stash_pop()
        if self._action != "validate":
            return self._create_summary(output_validation=output_first)
        if output_first["passed"] or not output_first["modified"]:
            return self._create_summary(output_fix=output_first)
        output_validate = self._run_hooks(validation_run=True)
        return self._create_summary(output_validation=output_validate, output_fix=output_first)

    def _run_hooks(self, validation_run: bool) -> dict:

        def raise_error(error: str):
            logger.critical("Unexpected Pre-Commit Error", error)
            raise ValueError(error)

        result = self._shell_runner.run(
            command=[],
            log_title=f"{"Validation" if validation_run else "Fix"} Run",
            log_level_exit_code="error" if validation_run else "notice",
        )
        if result.err:
            raise_error(sgr.remove_sequence(result.err))
        out_plain = sgr.remove_sequence(result.out)
        for line in out_plain.splitlines():
            for prefix in ("An error has occurred", "An unexpected error has occurred", "[ERROR]"):
                if line.startswith(prefix):
                    raise_error(out_plain)
        results = _process_shell_output(out_plain)
        return self._process_results(results, validation_run=validation_run)

    def _process_results(self, results: tuple[dict[str, dict], str], validation_run: bool) -> dict:
        hook_details = []
        count = {"Failed": 0, "Modified": 0, "Skipped": 0, "Passed": 0}
        for hook_id, result in results[0].items():
            if result["result"] == "Failed" and result["modified"]:
                result["result"] = "Modified"
            count[result["result"]] += 1
            result_str = f"{result['result']} {result['message']}" if result["message"] else result["result"]
            detail_list = mdit.element.field_list(
                [
                    ("Result", result_str),
                    ("Modified Files", str(result['modified'])),
                    ("Exit Code", result['exit_code']),
                    ("Duration", result['duration']),
                    ("Description", result['description']),
                ]
            )
            dropdown_elements = mdit.block_container(detail_list)
            if result["details"]:
                dropdown_elements.append(mdit.element.code_block(result["details"], caption="Details"), conditions=["full"])
            dropdown = mdit.element.dropdown(
                title=hook_id,
                body=dropdown_elements,
                color=self._dropdown_color[result["result"]],
                icon=self._emoji[result["result"]],
                opened=result["result"] == "Failed",
            )
            hook_details.append(dropdown)
        passed = count["Failed"] == 0 and count["Modified"] == 0
        summary_details = ", ".join([f"{count[key]} {key}" for key in count])
        doc = mdit.document(
            heading="Validation Run" if validation_run else "Fix Run",
            body=[f"{self._emoji["Passed" if passed else "Failed"]} {summary_details}"] + hook_details,
        )
        if results[1]:
            git_diff = mdit.element.code_block(results[1], language="diff")
            admo = mdit.element.admonition(title="Git Diff", body=git_diff, type="note", dropdown=True)
            doc.body.append(mdit.element.thematic_break(), conditions=["full"])
            doc.body.append(admo, conditions=["full"])
        output = {
            "passed": passed,
            "modified": count["Modified"] != 0,
            "count": count,
            "report": doc,
        }
        return output

    def _create_summary(self, output_validation: dict = None, output_fix: dict = None) -> dict:
        if output_validation and not output_fix:
            output = output_validation
            outputs = [output_validation]
        elif output_fix and not output_validation:
            output = output_fix
            outputs = [output_fix]
        else:
            output = output_validation
            output["modified"] = output["modified"] or output_fix["modified"]
            output["count"]["Modified (2nd Run)"] = output["count"]["Modified"]
            output["count"]["Modified"] = output_fix["count"]["Modified"]
            outputs = [output_fix, output_validation]

        summary_parts = []
        for mode, mode_count in output["count"].items():
            if mode_count:
                summary_parts.append(f"{mode_count} {mode}")
        summary = f"{", ".join(summary_parts)}."

        passed = output["passed"]
        modified = output["modified"]
        result_emoji = self._emoji["Passed" if passed else "Failed"]
        result_keyword = "Pass" if passed else "Fail"
        summary_result = f"{result_emoji} {result_keyword}"
        if modified:
            summary_result += " (modified files)"
        action_emoji = {"report": "📄", "commit": "💾", "amend": "📌"}[self._action]
        action_title = {"report": "Validate & Report", "commit": "Fix & Commit", "amend": "Fix & Amend"}[
            self._action
        ]
        scope = f"From ref. <code>{self._from_ref}</code> to ref. <code>{self._to_ref}</code>" if self._from_ref else "All files"
        body = mdit.element.field_list(
            [
                ("Result", summary_result),
                ("Action", f"{action_emoji} {action_title}"),
                ("Scope", scope),
            ]
        )
        final_output = {
            "passed": passed,
            "modified": modified,
            "summary": summary,
            "body": body,
            "section": [output["report"] for output in outputs],
            "commit_hash": self._commit_hash,
        }
        return final_output


def _process_shell_output(output: str) -> tuple[dict[str, dict[str, str | bool]], str]:
    """Parse the output of the pre-commit run command.

    Returns
    -------
    A 2-tuple of hook results and git diff.
    Hook results is a dictionary with hook IDs as keys and dictionaries
    containing the following keys as values:
    - description: Description of the hook.
    - message: Message from the hook.
    - result: Result of the hook run. One of "Passed", "Failed", "Skipped".
    - hook_id: The ID of the hook.
    - exit_code: The exit code of the hook.
    - duration: The duration of the run.
    - modified: Whether the hook modified files.
    - details: Details of the hook run.
    """

    def process_last_entry(details: str) -> tuple[str, str]:
        """Process the last entry in the hook output.

        The last entry in the output does not have a trailing separator,
        and pre-commit adds extra details at the end. These details are
        not part of the last hook's details, so they are separated out.

        References
        ----------
        - [Pre-commit run source code](https://github.com/pre-commit/pre-commit/blob/de8590064e181c0ad45d318a0c80db605bf62a60/pre_commit/commands/run.py#L303-L319)
        """
        info_text = (
            'pre-commit hook(s) made changes.\n'
            'If you are seeing this message in CI, '
            'reproduce locally with: `pre-commit run --all-files`.\n'
            'To run `pre-commit` as part of git workflow, use '
            '`pre-commit install`.'
        )
        details_cleaned = details.replace(info_text, "").strip()
        lines = details_cleaned.splitlines()
        diff_line_indices = [idx for idx, line in enumerate(lines) if line.strip() == "All changes made by hooks:"]
        if not diff_line_indices:
            return details_cleaned, ""
        last_idx = diff_line_indices[-1]
        hook_details = "\n".join(lines[:last_idx]).strip()
        git_diff = "\n".join(lines[last_idx + 1 :]).strip()
        return hook_details, git_diff

    pattern = re.compile(
        r"""
            ^(?P<description>[^\n]+?)
            \.{3,}
            (?P<message>[^\n]*(?=\(Passed|Failed|Skipped\))?)?
            (?P<result>Passed|Failed|Skipped)\n
            -\s*hook\s*id:\s*(?P<hook_id>[^\n]+)\n
            (-\s*duration:\s*(?P<duration>\d+\.\d+)s\n)?
            (-\s*exit\s*code:\s*(?P<exit_code>\d+)\n)?
            (-\s*files\s*were\s*modified\s*by\s*this\s*hook(?P<modified>\n))?
            (?P<details>(?:^(?![^\n]+?\.{3,}.*?(Passed|Failed|Skipped)).*\n)*)
        """,
        re.VERBOSE | re.MULTILINE,
    )
    matches = list(
        # Add a newline for when the last entry ends with the "hook id" line.
        pattern.finditer(output + "\n")
    )
    results = {}
    git_diff = ""
    for idx, match in enumerate(matches):
        data = match.groupdict()
        data["duration"] = data["duration"] or "0"
        data["exit_code"] = data["exit_code"] or "0"
        data["modified"] = bool(match.group("modified"))
        if idx + 1 != len(matches):
            data["details"] = data["details"].strip()
        else:
            data["details"], git_diff = process_last_entry(data["details"])
        if data["hook_id"] in results:
            logger.critical(f"Duplicate hook ID '{data['hook_id']}' found.")
        results[data["hook_id"]] = data
    logger.debug("Results", logger.pretty(results))
    return results, git_diff


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run pre-commit hooks.")

    parser.add_argument("-x", "--action", choices=["report", "run", "validate"], default="run", help="Required positional argument.")
    parser.add_argument("-c", "--config", help="Path to the pre-commit configuration file.")

    hook_group = parser.add_mutually_exclusive_group()
    hook_group.add_argument("-i", "--hook-id", help="Only run the hook with the given ID.")
    hook_group.add_argument("-s", "--hook-stage", help="Only run hooks of the given stage.")

    file_group = parser.add_mutually_exclusive_group()
    file_group.add_argument("-a", "--all-files", action="store_true", help="Run on all files.")
    file_group.add_argument("-f", "--files", nargs='+', help="Run on specific filepaths.")
    file_group.add_argument("-r1", "--from-ref", help="Run on files changed since the given git ref. This must be accompanied by --to-ref.")
    parser.add_argument("-r2", "--to-ref", help="Run on files changed up to the given git ref.")

    args = parser.parse_args()
    if (args.from_ref and not args.to_ref) or (args.to_ref and not args.from_ref):
        parser.error("Both --from-ref and --to-ref must be provided together.")
    logger.debug("Parsed arguments", args)
    out = run(
        config=args.config,
        action=args.action,
        hook_id=args.hook_id,
        hook_stage=args.hook_stage,
        files=args.files,
        all_files=args.all_files,
        ref_range=(args.from_ref, args.to_ref) if args.from_ref else None,
    )
    logger.info("Output", out)
