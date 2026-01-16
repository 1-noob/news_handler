import re
from .base import ClassificationRule

class BeyondTrendingRule(ClassificationRule):
    category = "Beyond trending"

    _pattern = re.compile(
        r"Beyond\s+Trending",
        re.IGNORECASE
    )

    def match(self, title: str, url: str) -> bool:
        return bool(self._pattern.search(title))

    def extract_title(self, title: str) -> str:
        return self._pattern.sub("", title).strip(" -:|")
