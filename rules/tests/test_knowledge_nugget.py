import pytest
from rules.knowledge_nugget import KnowledgeNuggetRule

pos_titles = [
    "Knowledge Nugget | Booth Level Officer (BLO): role and significance",
    "Knowledge Nugget: National Press Day and World Press Freedom Index",
    "Knowledge Nugget | India’s communication satellite CMS-03",
    "Knowledge Nugget | Police Commemoration Day and smart policing"
]

neg_titles = [
    "UPSC Key: Booth Level Officers explained",
    "World This Week | Press freedom under scrutiny",
    "UPSC Issue at a Glance | Police reforms in India",
    "Mains Answer Practice (GS 2) – Week 130",
    "Daily Subject Wise Quiz: Polity"
]

@pytest.mark.parametrize("title", pos_titles)
def test_knowledge_nugget_positive(title):
    rule = KnowledgeNuggetRule()
    assert rule.match(title)

@pytest.mark.parametrize("title", neg_titles)
def test_knowledge_nugget_negative(title):
    rule = KnowledgeNuggetRule()
    assert not rule.match(title)
