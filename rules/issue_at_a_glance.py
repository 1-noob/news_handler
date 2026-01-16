import re
from .base import ClassificationRule

class IssueAtAGlanceRule(ClassificationRule):
    category = "Upsc issue at a glance"

    _pattern = re.compile(
        r"UPSC\s+Issue\s+at\s+a\s+Glance",
        re.IGNORECASE
    )

    def match(self, title: str, url: str) -> bool:
        return bool(self._pattern.search(title))

    def extract_title(self, title: str) -> str:
        return self._pattern.sub("", title).strip(" -:|")
