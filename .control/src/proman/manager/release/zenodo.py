from __future__ import annotations as _annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING

import pylinks as pl
from loggerman import logger

from proman.manager.release.asset import create_releaseman_intput

if _TYPE_CHECKING:
    from typing import Literal

    from versionman.pep440_semver import PEP440SemVer

    from proman.manager import Manager
    from proman.manager.user import User


class ZenodoManager:
    _ROLE_TYPES = [
        "ContactPerson",
        "DataCollector",
        "DataCurator",
        "DataManager",
        "Distributor",
        "Editor",
        "HostingInstitution",
        "Producer",
        "ProjectLeader",
        "ProjectManager",
        "ProjectMember",
        "RegistrationAgency",
        "RegistrationAuthority",
        "RelatedPerson",
        "Researcher",
        "ResearchGroup",
        "RightsHolder",
        "Supervisor",
        "Sponsor",
        "WorkPackageLeader",
        "Other",
    ]

    def __init__(self, manager: Manager):
        self._manager = manager
        self._api = {
            True: pl.api.zenodo(token=self._manager.token.zenodo_sandbox.get(), sandbox=True),
            False: pl.api.zenodo(token=self._manager.token.zenodo.get(), sandbox=False),
        }
        self._has_token = {
            True: bool(self._manager.token.zenodo_sandbox),
            False: bool(self._manager.token.zenodo),
        }
        self._varman = self._manager.variable
        self._changelog = self._manager.changelog
        return

    def get_or_make_drafts(self) -> tuple[dict | None, dict | None]:
        """Get current draft depositions in both Zenodo and Zenodo Sandbox,
        or create new ones if any of them doesn't exist.

        Returns
        -------
        main_draft_data, sandbox_draft_data, vars_updated, changelog_updated
        """
        main_draft_data = self.get_or_make_draft(sandbox=False)
        sandbox_draft_data = self.get_or_make_draft(sandbox=True)
        return main_draft_data, sandbox_draft_data

    def get_or_make_draft(self, sandbox: bool) -> dict | None:
        """Get the current draft deposition, or create a new one if a draft does not exist.

        This also creates the project concept, if no concept ID is defined already.

        Parameters
        ----------
        sandbox
            Whether the deposition is for Zenodo Sandbox versus the main Zenodo repository.

        Returns
        -------
        draft_data, vars_updated, changelog_updated
        """
        title = f"{self._platform_name(sandbox)} Draft"
        if (
            not self._has_token[sandbox]
            or self._workflow_config(sandbox=sandbox).get("action") != "auto"
        ):
            return None
        record = (
            self._changelog.current.get("dev", {}).get("zenodo_sandbox")
            if sandbox
            else self._changelog.current.get("zenodo")
        )
        if record and record["draft"]:
            logger.success(
                f"{title} Retrieval",
                "Retrieved current draft from changelog:",
                logger.data_block(record),
            )
            return record
        logger.info(
            f"{title} Retrieval",
            "No draft found in the current changelog:",
            logger.data_block(self._changelog.current),
        )
        api = self._api[sandbox]
        concept_record = self._varman.setdefault(self._var_key(sandbox), {}).setdefault(
            "concept", {}
        )
        if concept_record.get("id"):
            if concept_record.get("draft"):
                depo_id = int(concept_record["id"]) + 1
                logger.success(
                    f"{title} Creation",
                    f"Selected open draft defined in variables file wih deposition ID {depo_id}",
                )
            else:
                deposition = api.deposition_new_version(deposition_id=int(concept_record["id"]) + 1)
                logger.success(
                    f"{title} Creation", "Created new version draft:", logger.data_block(deposition)
                )
                depo_id = deposition["id"]
            draft = {
                "id": int(depo_id),
                "doi": self._doi(depo_id, sandbox=sandbox),
                "draft": True,
            }
            self._changelog.update_zenodo(sandbox=sandbox, **draft)
            return draft
        deposition = api.deposition_create()
        logger.success(
            f"{title} Concept Creation", "Created new concept draft:", logger.data_block(deposition)
        )
        concept, draft = [
            {
                "id": int(_id),
                "doi": self._doi(_id, sandbox=sandbox),
                "draft": True,
            }
            for _id in (deposition["conceptrecid"], deposition["id"])
        ]
        concept_record.update(concept)
        self._changelog.update_zenodo(sandbox=sandbox, **draft)
        return draft

    def update_drafts(
        self,
        version: PEP440SemVer | str,
        publish_main: bool = False,
        publish_sandbox: bool = False,
        id_main: int | None = None,
        id_sandbox: int | None = None,
    ):
        if not id_main:
            main_draft = self.get_or_make_draft(sandbox=False)
            id_main = main_draft["id"] if main_draft else None
        if not id_sandbox:
            sandbox_draft = self.get_or_make_draft(sandbox=True)
            id_sandbox = sandbox_draft["id"] if sandbox_draft else None

        outputs = []
        for draft_id, publish, sandbox in (
            (id_main, publish_main, False),
            (id_sandbox, publish_sandbox, True),
        ):
            if draft_id:
                self._update_metadata(
                    deposition_id=draft_id,
                    sandbox=sandbox,
                    version=version,
                )
                asset_key = f"workflow.publish.zenodo{'_sandbox' if sandbox else ''}.asset"
                outputs.append(
                    self._make_output(
                        deposition_id=draft_id,
                        asset_config=self._manager.fill_jinja_templates(
                            self._manager.data[asset_key],
                            jsonpath=asset_key,
                            env_vars={"version": version},
                        ),
                        publish=publish,
                    )
                )
            else:
                outputs.append(None)
        return outputs[0], outputs[1]

    def _update_metadata(
        self, deposition_id: str | int, sandbox: bool, version: PEP440SemVer | str
    ):
        metadata = self._create_metadata(version=version)
        return self._upload_metadata(
            deposition_id=deposition_id, metadata=metadata, sandbox=sandbox
        )

    def _create_metadata(self, version: PEP440SemVer | str) -> dict:
        # https://developers.zenodo.org/#deposit-metadata
        def create_person(user: User) -> dict:
            out = {"name": user["name"]["full_inverted"]}
            if "affiliation" in user:
                out["affiliation"] = user["affiliation"]
            if "orcid" in user:
                out["orcid"] = user["orcid"]["id"]
            if "gnd" in user:
                out["gnd"] = user["gnd"]["id"]
            return out

        def create_contributor(entry: str | dict):
            def add_from_role_types(role_types: list[str]):
                output_contributors = []
                for role_type in role_types:
                    if role_type not in self._ROLE_TYPES:
                        logger.error(
                            "Zenodo Contributors Metadata",
                            f"The role type '{role_type}' defined for contributor '{entry}' is invalid. "
                            "The entry will not be included in metadata.",
                        )
                    contributor_entry = person | {"type": role_type}
                    if contributor_entry not in output_contributors:
                        output_contributors.append(contributor_entry)
                return output_contributors

            def add_from_role_ids(person_role_ids: list[str]):
                role_types = [
                    self._manager.data["role"][person_role_id]["type"]
                    for person_role_id in person_role_ids
                ]
                return add_from_role_types(role_types)

            user = self._manager.user.from_id(entry)
            person = create_person(user=user)
            if isinstance(entry, str) or not any(
                key in entry for key in ("role_ids", "role_types")
            ):
                role_ids = user.get("role", {}).keys()
                if not role_ids:
                    logger.error(
                        "Zenodo Contributors Metadata",
                        f"Contributor '{entry}' has no defined roles and will not be included in metadata.",
                    )
                    return []
                return add_from_role_ids(role_ids)
            outputs = []
            if "role_types" in entry:
                input_types = entry["role_types"]
                if isinstance(input_types, str):
                    input_types = [input_types]
                outputs.extend(add_from_role_types(input_types))
            if "role_ids" in entry:
                input_ids = entry["role_ids"]
                if isinstance(input_ids, str):
                    input_ids = [input_ids]
                more_outputs = add_from_role_ids(input_ids)
                for output in more_outputs:
                    if output not in outputs:
                        outputs.append(output)
            return outputs

        metadata_raw = self._manager.data["zenodo"]
        metadata = {k: v for k, v in metadata_raw.items() if v}
        metadata["creators"] = [
            create_person(user=self._manager.user.from_id(entity_id))
            for entity_id in metadata["creators"]
        ]
        contributors_data = metadata_raw.get("contributors")
        if contributors_data:
            contributors_entry = []
            for contributor_data in contributors_data:
                contributors_entry.extend(create_contributor(entry=contributor_data))
            metadata["contributors"] = contributors_entry
        if "notes" in metadata:
            metadata["notes"] = self._manager.fill_jinja_template(metadata["notes"])
        if "communities" in metadata:
            metadata["communities"] = [
                {"identifier": identifier} for identifier in metadata["communities"]
            ]
        if "grants" in metadata:
            metadata["grants"] = [{"id": grant["id"]} for grant in metadata["grants"]]
        metadata |= {
            "version": str(version),
            "preserve_doi": True,
        }
        return metadata

    def _upload_metadata(self, deposition_id: str | int, metadata: dict, sandbox: bool):
        log_title = f"{self._platform_name(sandbox)} Draft Metadata Update"
        try:
            response = self._api[sandbox].deposition_update(
                deposition_id=deposition_id, metadata=metadata
            )
        except Exception:
            logger.error(
                log_title,
                "Failed to update metadata for deposition:",
                logger.traceback(),
            )
            return
        logger.success(log_title, "Updated metadata for deposition:", logger.data_block(response))
        return

    def _workflow_config(self, sandbox: bool):
        return self._manager.data[f"workflow.publish.{'zenodo_sandbox' if sandbox else 'zenodo'}"]

    @staticmethod
    def _make_output(deposition_id: str | int, asset_config: dict, publish: bool):
        return {
            "deposition_id": deposition_id,
            "delete_assets": "all",
            "assets": create_releaseman_intput(asset_config=asset_config, target="zenodo"),
            "publish": publish,
        }

    @staticmethod
    def _doi(deposition_id: str | int, sandbox: bool):
        doi_prefix = "10.5072" if sandbox else "10.5281"  # https://developers.zenodo.org/#testing
        return f"{doi_prefix}/zenodo.{deposition_id}"

    @staticmethod
    def _var_key(sandbox: bool) -> Literal["zenodo", "zenodo_sandbox"]:
        return "zenodo_sandbox" if sandbox else "zenodo"

    @staticmethod
    def _platform_name(sandbox: bool) -> str:
        return "Zenodo Sandbox" if sandbox else "Zenodo"
