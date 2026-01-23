from typing import List, Sequence

from classification.types import ClassificationResult, ClassificationStatus


class ClassificationManager:
    """Coordinates classification rules and resolves final classification."""

    def __init__(self, rules: Sequence):
        self._rules = rules
        

    def classify(self, raw_title: str) -> ClassificationResult:
        """
        Classify an article.

        Returns a ClassificationResult.
        """
        matched_rules = []

        for rule in self._rules:
            if rule.match(raw_title):
                matched_rules.append(rule)

        if len(matched_rules) == 1:
            rule = matched_rules[0]
            return ClassificationResult(
                status=ClassificationStatus.CLASSIFIED,
                raw_title=raw_title,
                category=rule.category,
            )
        
        return ClassificationResult(
            status=ClassificationStatus.REVIEW_REQUIRED,    
            raw_title=raw_title,
            category=None
        )