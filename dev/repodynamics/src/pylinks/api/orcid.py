# Standard libraries
import re
import warnings

# Non-standard libraries
import pylinks


class Orcid:
    def __init__(self, orcid_id: str):
        match = re.match(r"(?:https?://)?(?:orcid\.org/)?(\d{4}-\d{4}-\d{4}-\d{3}[0-9X])", orcid_id)
        if not match:
            raise ValueError(f"Invalid ORCID ID: {orcid_id}")
        self.id = match.group(1)
        self.url = f"https://orcid.org/{self.id}"
        self._data: dict = None
        self._dois: list[str] = None
        return

    @property
    def records(self) -> dict:
        if not self._data:
            self._data = pylinks.request(
                url=f"https://pub.orcid.org/v3.0/{self.id}",
                headers={"Accept": "application/json"},
                response_type="json",
            )
        return self._data

    @property
    def doi(self) -> list[str]:
        if self._dois:
            return self._dois
        self._dois = []
        for work in self.records["activities-summary"]["works"]["group"]:
            for identifier in work["work-summary"][0]["external-ids"]["external-id"]:
                if identifier["external-id-type"] == "doi":
                    self._dois.append(identifier["external-id-value"])
                    break
            else:
                warnings.warn(f"Could not find DOI for work {work}.")
        return self._dois


def orcid(orcid_id: str) -> Orcid:
    return Orcid(orcid_id=orcid_id)
