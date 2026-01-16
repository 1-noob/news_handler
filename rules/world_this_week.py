import re
from .base import ClassificationRule

class WorldThisWeekRule(ClassificationRule):
    category = "World this week"

    _pattern = re.compile(
        r"World\s+This\s+Week",
        re.IGNORECASE
    )

    def match(self, title: str, url: str) -> bool:
        return bool(self._pattern.search(title))

    def extract_title(self, title: str) -> str:
        return self._pattern.sub("", title).strip(" -:|")
