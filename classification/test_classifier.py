from classification.types import ClassificationStatus
from classification.classifier import ArticleClassifier


# --------------------
# Dummy rules
# --------------------

class DummySkipRule:
    def match(self, title: str) -> bool:
        return "SKIP" in title


class DummyClassifyRule:
    def __init__(self, keyword: str, category: str):
        self.keyword = keyword
        self.category = category

    def match(self, title: str) -> bool:
        return self.keyword in title


# --------------------
# Tests
# --------------------

def test_article_is_skipped():
    classifier = ArticleClassifier(
        skip_rules=[DummySkipRule()],
        classification_rules=[]
    )

    result = classifier.classify("THIS ARTICLE SHOULD SKIP")

    assert result.status == ClassificationStatus.SKIPPED
    assert result.category is None


def test_article_is_classified():
    classifier = ArticleClassifier(
        skip_rules=[],
        classification_rules=[
            DummyClassifyRule("ETHICS", "UPSC Ethics")
        ]
    )

    result = classifier.classify("UPSC ETHICS simplified case study")

    assert result.status == ClassificationStatus.CLASSIFIED
    assert result.category == "UPSC Ethics"


def test_article_requires_review():
    classifier = ArticleClassifier(
        skip_rules=[],
        classification_rules=[
            DummyClassifyRule("ETHICS", "Ethics"),
            DummyClassifyRule("UPSC", "General UPSC"),
        ]
    )

    result = classifier.classify("UPSC ETHICS overview")

    assert result.status == ClassificationStatus.REVIEW_REQUIRED
    assert result.category is None
