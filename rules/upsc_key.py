import re
from .base import ClassificationRule

class UpscKeyRule(ClassificationRule):
    category = "Upsc key"

    _pattern = re.compile(
        r"(^|\b)UPSC\s+Key(\b|[:\-\|])",
        re.IGNORECASE
    )

    def match(self, title: str, url: str) -> bool:
        return bool(self._pattern.search(title))

    def extract_title(self, title: str) -> str:
        return self._pattern.sub("", title).strip(" -:|")
