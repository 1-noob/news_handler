import re
from .base import ClassificationRule

class ArtAndCultureRule(ClassificationRule):
    category = "Art & Culture"

    _pattern = re.compile(
        r"Art\s*&\s*Culture",
        re.IGNORECASE
    )

    def match(self, title: str, url: str) -> bool:
        return bool(self._pattern.search(title))

    def extract_title(self, title: str) -> str:
        return self._pattern.sub("", title).strip(" -:|")
