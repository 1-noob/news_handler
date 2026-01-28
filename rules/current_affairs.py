import re
from .base import ClassificationRule

class CurrentAffairsRule(ClassificationRule):
    category = "Current Affairs"

    _pattern = re.compile(
        r"\bUPSC\s+Current\s+Affairs\b",
        re.IGNORECASE
    )

    _cleanup = re.compile(
        r"^.*?(?:Pointers\s+of\s+the\s+past\s+week\s*)?\|\s*",
        re.IGNORECASE
    )

    def match(self, title: str) -> bool:
        return bool(self._pattern.search(title))

    def extract_title(self, title: str) -> str:
        return self._cleanup.sub("", title).strip(" -:|")
