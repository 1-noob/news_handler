from typing import List, Sequence

from classification.types import ClassificationResult, ClassificationStatus


class Classifier:
    """Coordinates classification rules and resolves final classification."""

    def __init__(self, rules: Sequence):
        self._rules = rules
        

    def classify(self, raw_title: str) -> ClassificationResult:
        """
        Rule engine.
        Applies classification rules and resolves conflicts.
        Decides a category.
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