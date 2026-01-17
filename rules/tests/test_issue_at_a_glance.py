import pytest
from rules.issue_at_a_glance import IssueAtAGlanceRule

pos_titles = [
    "UPSC Issue at a Glance | Princely States: India’s Journey of State Formation",
    "UPSC Issue at a Glance: Cyclones – Formation, Naming, Climate Link",
    "UPSC Issue at a Glance | Delhi’s Toxic Air and Beyond: Understanding Air Pollution"
]

@pytest.mark.parametrize("title", pos_titles)
def test_issue_at_a_glance_positive(title):
    rule = IssueAtAGlanceRule()
    assert rule.match(title)

neg_titles = [
    "Issue at a glance: Understanding UPSC trends",        # generic phrase
    "UPSC Essentials: Cyclones and climate effects",       # no exact pattern
    "World This Week | G20 Summit in South Africa",        # different category
    "UPSC Key: India and Germany relations",               # different category
    "Mains Answer Practice (GS 2) – Week 130"             # different article type
]

@pytest.mark.parametrize("title", neg_titles)
def test_issue_at_a_glance_negative(title):
    rule = IssueAtAGlanceRule()
    assert not rule.match(title)
