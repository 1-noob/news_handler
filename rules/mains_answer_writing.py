import re
from .base import ClassificationRule

class MainsAnswerWritingRule(ClassificationRule):
    category = "Mains Answer Writing"

    _pattern = re.compile(
        r"Mains[-\s]+answer[-\s]+practice",
        re.IGNORECASE
    )

    _cleanup = re.compile(
        r"^.*?(?=GS\s*\d+)",
        re.IGNORECASE
    )

    def match(self, title: str) -> bool:
        return bool(self._pattern.search(title))

    def extract_title(self, title: str) -> str:
        cleaned = self._cleanup.sub("", title)
        return cleaned.strip(" -:|—")
