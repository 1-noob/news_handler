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
            if rule.match(raw_title):
                return ClassificationResult(
                    status=ClassificationStatus.SKIPPED,
                    title=raw_title,
                    category=None,
                )
        
        # Classification rules
        matches = []
        cleaned_title = raw_title

        for rule in self._classification_rules:
            if rule.match(raw_title):
                matches.append(rule)
                cleaned_title = rule.extract_title(raw_title)
        
        if len(matches) == 1:
            rule = matches[0]
            return ClassificationResult(
                status=ClassificationStatus.CLASSIFIED,
                title=cleaned_title,
                category=rule.category,
            )

        # Review required
        return ClassificationResult(
            status=ClassificationStatus.REVIEW_REQUIRED,
            title=raw_title,
            category=None,
        )        

# Example usage:
if __name__ == "__main__":
    article_classifier = ArticleClassifier(CONFIG.SKIP_RULE, CONFIG.CLASSIFICATION_RULES)