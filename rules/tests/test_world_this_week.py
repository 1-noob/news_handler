import pytest
from rules.world_this_week import WorldThisWeekRule

pos_titles = [
    "World This Week | Trump holds off on military action in Iran, European troops in Greenland and the first Taliban-appointed diplomat in India",
    "The World This Week: Trump holds off on action in Iran and China tensions escalate",
    "world this week — G20 Summit in South Africa, US-China talks on Taiwan, and Russia-Ukraine peace plan",
    "The world this week | Sheikh Hasina sentenced to death, Trump peace talks and Gen Z protests"
]

@pytest.mark.parametrize("title", pos_titles)
def test_world_this_week_positive(title):
    rule = WorldThisWeekRule()
    assert rule.match(title)

neg_titles = [
    "World issues update: global trade tensions rise",
    "This week in geopolitics: Russia-Ukraine and China",
    "Top global headlines of the week",
    "Weekly world overview on climate change"
]

@pytest.mark.parametrize("title", neg_titles)
def test_world_this_week_negative(title):
    rule = WorldThisWeekRule()
    assert not rule.match(title)
