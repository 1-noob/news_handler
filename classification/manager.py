from typing import List

from classification.types import ClassificationResult, ClassificationStatus


class ClassificationManager:
    """Base class for implementing rules"""
    
    def __init__(self, rules: List, filters: List):
        self._rules = rules
        self._filters = filters

    def classify(self, raw_title: str) -> ClassificationResult:
        """
        Classify an article based only on its raw title.

        Returns a ClassificationResult.
        """
        raise NotImplementedError
