import re
from .base import ClassificationRule

class GeneralArticleRule(ClassificationRule):
    category = "General article"

    _pattern = re.compile(
        r"General\s+Article",
        re.IGNORECASE
    )

    def match(self, title: str, url: str) -> bool:
        return bool(self._pattern.search(title))

    def extract_title(self, title: str) -> str:
        return self._pattern.sub("", title).strip(" -:|")
