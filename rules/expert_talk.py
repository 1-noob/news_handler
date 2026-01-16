import re
from .base import ClassificationRule

class ExpertTalkRule(ClassificationRule):
    category = "Expert talk"

    _pattern = re.compile(
        r"Expert\s+Talk",
        re.IGNORECASE
    )

    def match(self, title: str, url: str) -> bool:
        return bool(self._pattern.search(title))

    def extract_title(self, title: str) -> str:
        return self._pattern.sub("", title).strip(" -:|")
