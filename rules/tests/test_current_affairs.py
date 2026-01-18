import pytest
from rules.current_affairs import CurrentAffairsRule

pos_titles = [
    "UPSC Current Affairs Pointers | Past Week January 5–11, 2026",
    "UPSC Current Affairs Pointers of Past Week November 17 to 23, 2025",
    "UPSC Current Affairs Pointers | Past Week November 10–16, 2025",
    "UPSC Current Affairs Pointers of the Past Week November 3–9, 2025",
    "UPSC Current Affairs Pointers of Past Week October 27–November 2, 2025"
]

neg_titles = [
    "UPSC Key: India-Germany relations",
    "Beyond Trending | What is multipolarity?",
    "Knowledge Nugget | Booth Level Officer",
    "World This Week | Global geopolitics",
    "UPSC Essentials: Current affairs explained",
    "UPSC Current Affairs analysis for prelims"
]

@pytest.mark.parametrize("title", pos_titles)
def test_current_affairs_positive(title):
    rule = CurrentAffairsRule()
    assert rule.match(title)

@pytest.mark.parametrize("title", neg_titles)
def test_current_affairs_negative(title):
    rule = CurrentAffairsRule()
    assert not rule.match(title)
