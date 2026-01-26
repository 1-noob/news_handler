import re
from .base import ClassificationRule

class EthicsSimplifiedRule(ClassificationRule):
    category = "Ethics simplified"

    _pattern = re.compile(
        r"\bUPSC\s+Ethics\s+Simplified\b",
        re.IGNORECASE
    )

    def match(self, title: str) -> bool:
        return bool(self._pattern.search(title))

    def extract_title(self, title: str) -> str:
        return self._pattern.sub("", title).strip(" -:|")
