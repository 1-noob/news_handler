import pytest
from rules.art_and_culture import ArtAndCultureRule

pos_titles = [
    "Art and Culture with Devdutt Pattanaik | Are horses native to India?",
    "Devdutt Pattanaik | Karma’s cosmic order in Jain manuscripts",
    "Devdutt Pattanaik | Lotus remains India’s simplest yet most profound symbol"
]

neg_titles = [
    "UPSC Key: Indian heritage and culture",
    "Ancient Indian art forms explained",
    "World This Week | Cultural diplomacy",
    "Knowledge Nugget | Jain philosophy",
    "Art of governance in ancient India"
]

@pytest.mark.parametrize("title", pos_titles)
def test_art_and_culture_positive(title):
    rule = ArtAndCultureRule()
    assert rule.match(title)

@pytest.mark.parametrize("title", neg_titles)
def test_art_and_culture_negative(title):
    rule = ArtAndCultureRule()
    assert not rule.match(title)
