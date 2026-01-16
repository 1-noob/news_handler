import re
from .base import ClassificationRule

class EthicsSimplifiedRule(ClassificationRule):
    category = "Ethics simplified"

    _pattern = re.compile(
        r"Ethics\s+Simplified",
        re.IGNORECASE
    )

    def match(self, title: str, url: str) -> bool:
        return bool(self._pattern.search(title))

    def extract_title(self, title: str) -> str:
        return self._pattern.sub("", title).strip(" -:|")
