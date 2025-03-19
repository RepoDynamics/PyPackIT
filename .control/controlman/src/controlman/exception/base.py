from __future__ import annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING
from functools import partial as _partial
from exceptionman import ReporterException as _ReporterException
import mdit as _mdit

if _TYPE_CHECKING:
    from mdit import Document


class ControlManException(_ReporterException):
    """Base class for all exceptions raised by ControlMan."""

    def __init__(self, report: Document):
        sphinx_config = {"html_title": "ControlMan Error Report"}
        report.target_configs["sphinx"] = _mdit.target.sphinx(
            renderer=_partial(
                _mdit.render.sphinx,
                config=_mdit.render.get_sphinx_config(sphinx_config)
            )
        )
        super().__init__(report=report)
        return
