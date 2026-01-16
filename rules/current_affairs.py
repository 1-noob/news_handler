import re
from .base import ClassificationRule

class CurrentAffairsRule(ClassificationRule):
    category = "Current Affairs"

    _pattern = re.compile(
        r"Current\s+Affairs",
        re.IGNORECASE
    )

    def match(self, title: str, url: str) -> bool:
        return bool(self._pattern.search(title))

    def extract_title(self, title: str) -> str:
        return self._pattern.sub("", title).strip(" -:|")
