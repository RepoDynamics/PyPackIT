from __future__ import annotations

from dataclasses import dataclass, field

import actionman
from loggerman import logger
import pyshellman

from proman.dstruct import Token


__all__ = ["create", "TokenManager"]


def create(
    *,
    github: str | None = None,
    github_admin: str | None = None,
    zenodo: str | None = None,
    zenodo_sandbox: str | None = None,
    remove_from_env: bool = False,
) -> TokenManager:
    """Create a token manager.

    For each token that is not provided,
    the function will attempt to read it from a set of locations.

    Parameters
    ----------
    github
        GitHub token.
    github_admin
        GitHub token with admin privileges.
    zenodo
        Zenodo token.
    zenodo_sandbox
        Zenodo sandbox token.
    remove_from_env
        If True, any token read from the environment will be removed from the environment
        after being read. This is useful for security reasons,
        but requires the caller to set the token in the environment again
        if it is needed later.
    """

    def set_github() -> str | None:
        if github:
            return github
        for env_var_name in ("GITHUB_TOKEN", "GITHUB_ADMIN_TOKEN"):
            token = actionman.env_var.read(env_var_name, typ=str, remove=remove_from_env)
            if token:
                return token
        token = pyshellman.run(
            command=["gh", "auth", "token"],
            logger=logger,
            raise_execution=False,
            raise_exit_code=False,
            raise_stderr=False,
        ).out
        return token or None

    def set_github_admin() -> str | None:
        if github_admin:
            return github_admin
        for env_var_name in ("GITHUB_ADMIN_TOKEN",):
            token = actionman.env_var.read(env_var_name, typ=str, remove=remove_from_env)
            if token:
                return token
        return class_args["github"].get()

    def set_zenodo() -> str | None:
        if zenodo:
            return zenodo
        return actionman.env_var.read("ZENODO_TOKEN", typ=str, remove=remove_from_env)

    def set_zenodo_sandbox() -> str | None:
        if zenodo_sandbox:
            return zenodo_sandbox
        return actionman.env_var.read("ZENODO_SANDBOX_TOKEN", typ=str, remove=remove_from_env)

    class_args = {}
    for token_id, token_parser, token_name in (
        ("github", set_github, "GitHub"),
        ("github_admin", set_github_admin, "GitHub Admin"),
        ("zenodo", set_zenodo, "Zenodo"),
        ("zenodo_sandbox", set_zenodo_sandbox, "Zenodo Sandbox"),
    ):
        class_args[token_id] = Token(token=token_parser(), name=token_name)
    return TokenManager(**class_args)


@dataclass(frozen=True, repr=False, kw_only=True)
class TokenManager:
    github: Token = field(repr=False)
    github_admin: Token = field(repr=False)
    zenodo: Token = field(repr=False)
    zenodo_sandbox: Token = field(repr=False)

    def __repr__(self) -> str:
        args = ", ".join(f"{k}=***" for k, v in self.__dict__.items() if v)
        return f"{self.__class__.__name__}({args})"
