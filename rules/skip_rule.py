import re


class SkipRule:
    """
    Skips articles that must not be classified at all.
    """

    _pattern = re.compile(
        r"""
        daily\s+quiz
        |subject\s+wise\s+quiz
        |csat\s+quiz
        |expert\s+talk
        |interview\s+special
        |case\s+study
        """,
        re.IGNORECASE | re.VERBOSE
    )

    def match(self, title: str) -> bool:
        return bool(self._pattern.search(title))
