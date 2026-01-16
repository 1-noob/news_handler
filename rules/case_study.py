import re
from .base import ClassificationRule

class CaseStudyRule(ClassificationRule):
    category = "Case study"

    _pattern = re.compile(
        r"Case\s+Study",
        re.IGNORECASE
    )

    def match(self, title: str, url: str) -> bool:
        return bool(self._pattern.search(title))

    def extract_title(self, title: str) -> str:
        return self._pattern.sub("", title).strip(" -:|")
