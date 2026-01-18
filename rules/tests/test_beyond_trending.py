import pytest
from rules.beyond_trending import BeyondTrendingRule

pos_titles = [
    "Beyond Trending | What is military-industrial complex?",
    "Beyond Trending: What is multipolarity?",
    "Beyond Trending | What is honour?",
    "Beyond Trending | What is flow and contra-flow?"
]

neg_titles = [
    "UPSC Key: Military-industrial complex explained",
    "Knowledge Nugget | Multipolar world order",
    "World This Week | Global power shifts",
    "Mains Answer Practice (GS 2) – Week 130",
    "What is multipolarity? Explained"
]

@pytest.mark.parametrize("title", pos_titles)
def test_beyond_trending_positive(title):
    rule = BeyondTrendingRule()
    assert rule.match(title)

@pytest.mark.parametrize("title", neg_titles)
def test_beyond_trending_negative(title):
    rule = BeyondTrendingRule()
    assert not rule.match(title)
