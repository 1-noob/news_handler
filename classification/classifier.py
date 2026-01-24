from typing import List, Sequence

from classification.types import ClassificationResult, ClassificationStatus


class ArticleClassifier:
    """Rule-based article classifier.
           1. Apply skip rules.
           2. Apply classification rules.
           3. Resolve final status."""

    def __init__(self, skip_rule, classification_rules):
        self._skip_rule = skip_rule
        self._classification_rules = classification_rules

    def classify(self, raw_title: str) -> ClassificationResult:
        
        # Skip rules
        for rule in self._skip_rule:
            if rule.matches(raw_title):
                return ClassificationResult(
                    status=ClassificationStatus.SKIPPED,
                    raw_title=raw_title,
                    category=None,
                )
        
        # Classification rules
        matches = [
            r for r in self._classification_rules if r.matches(raw_title)
            ]

        if len(matches) == 1:
            rule = matches[0]
            return ClassificationResult(
                status=ClassificationStatus.CLASSIFIED,
                raw_title=raw_title,
                category=rule.category,
            )

        # Review required
            # No matches or multiple matches
        return ClassificationResult(
            status=ClassificationStatus.REVIEW_REQUIRED,    
            raw_title=raw_title,
            category=None, 
        )