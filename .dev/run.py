from __future__ import annotations as _annotations

import json
from pathlib import Path as _Path


class DevRunner:
    def __init__(self, metadata_filepath: _Path | str = ".github/.repodynamics/metadata.json"):
        self.data = json.loads(_Path(metadata_filepath).read_text())
        return

    @property
    def environments(self) -> list[str]:
        return [key[4:] for key in self.data if key.startswith("env_")]

    def run(self, environment: str, feature: str, task: str):
        env = self.data.get(f"env_{environment}")
        if not env:
            raise ValueError(
                f"Environment '{environment}' not found in metadata. "
                f"Available environments are: {', '.join(self.environments)}"
            )
        feature = env.get(feature)
        if not feature:
            raise ValueError(
                f"Feature '{feature}' not defined for environment '{environment}'. "
                f"Available features are: {', '.join(env.keys())}"
            )
        task = feature.get(task)
        if not task:
            raise ValueError(
                f"Task '{task}' not defined for feature '{feature}' in environment '{environment}'. "
                f"Available tasks are: {', '.join(feature.keys())}"
            )
