import re
from .base import ClassificationRule

class MainsAnswerWritingRule(ClassificationRule):
    category = "Mains Answer Writing"

    _pattern = re.compile(
        r"\bMains\s+Answer\s+(Practice|Writing)\b",
        re.IGNORECASE
    )

    def match(self, title: str, url: str) -> bool:
        return bool(self._pattern.search(title))

    def extract_title(self, title: str) -> str:
        cleaned = self._pattern.sub("", title)
        return cleaned.strip(" -:|—")
