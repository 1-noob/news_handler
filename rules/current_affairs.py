import re
from .base import ClassificationRule

class CurrentAffairsRule(ClassificationRule):
    category = "Current Affairs"

    _pattern = re.compile(
        r"^.*?\|\s*",
        re.IGNORECASE
    )

    def match(self, title: str) -> bool:
        return bool(self._pattern.search(title))

    def extract_title(self, title: str) -> str:
        return self._pattern.sub("", title).strip(" -:|")
