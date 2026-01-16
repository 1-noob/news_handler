import re

class QuizRejectRule:
    _pattern = re.compile(r"\bquiz\b", re.IGNORECASE)

    def match(self, title: str, url: str) -> bool:
        return bool(self._pattern.search(title) 
        or self._pattern.search(url))