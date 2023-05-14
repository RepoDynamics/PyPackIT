
from typing import Union, List
import json
import datetime

class ProjectMetaData:
    
    @property
    def app_name(self) -> str:
        return "MyAppName"
    
    @property
    def owner_name(self) -> str:
        return "Armin Ariamajd"

    @property
    def copyright_notice(self) -> Union[str, List[str]]:
        return f"Copyright (c) 2020–{datetime.date.today().year} {self.owner_name}"

    @property
    def first_release_date(self) -> datetime.date:
        return datetime.date.today()

    @property
    def version(self) -> str:
        return "0.0"

    @property
    def release(self) -> str:
        return "0.0.0"