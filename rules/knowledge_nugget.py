import re
from .base import ClassificationRule

class KnowledgeNuggetRule(ClassificationRule):
    category = "Knowledge nugget"

    _pattern = re.compile(
        r"Knowledge\s+Nugget",
        re.IGNORECASE
    )

    def match(self, title: str, url: str) -> bool:
        return bool(self._pattern.search(title))

    def extract_title(self, title: str) -> str:
        return self._pattern.sub("", title).strip(" -:|")
