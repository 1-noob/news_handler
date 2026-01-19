import pytest
from rules.ethics_simplified import EthicsSimplifiedRule

pos_titles = [
    "UPSC Ethics simplified | Cough syrup tragedy: a case study",
    "UPSC Ethics simplified – Indigo crisis: safety, trust and service",
    "UPSC Ethics simplified: Police officer duty and moral courage",
]

neg_titles = [
    "UPSC Mains GS4: Ethics paper analysis",
    "Ethics case study: public accountability",
    "Knowledge Nugget | Ethical governance",
    "UPSC Key: Ethics in civil services",
]

@pytest.mark.parametrize("title", pos_titles)
def test_ethics_simplified_positive(title):
    rule = EthicsSimplifiedRule()
    assert rule.match(title)

@pytest.mark.parametrize("title", neg_titles)
def test_ethics_simplified_negative(title):
    rule = EthicsSimplifiedRule()
    assert not rule.match(title)
