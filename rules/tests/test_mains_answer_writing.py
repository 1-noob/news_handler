import pytest
from rules.mains_answer_writing import MainsAnswerWritingRule

pos_titles = [
    "UPSC Essentials | Mains Answer Practice (GS 2) – Week 130",
    "UPSC Essentials | Mains Answer Practice (GS 3) – Week 129",
    "UPSC Essentials | Mains Answer Practice (GS 1) – Week 125",
    "UPSC Mains Answer Practice (GS 2) – Week 133",
    "Mains Answer Writing: GS 1 – Week 137"
]

neg_titles = [
    "UPSC Key: India-Germany relations",
    "Knowledge Nugget: Translocation of cheetahs",
    "UPSC Essentials | World This Week",
    "Daily Subject Wise Quiz: Polity",
    "UPSC Prelims Practice Questions"
]

@pytest.mark.parametrize("title", pos_titles)
def test_mains_answer_writing_positive(title):
    rule = MainsAnswerWritingRule()
    assert rule.match(title)

@pytest.mark.parametrize("title", neg_titles)
def test_mains_answer_writing_negative(title):
    rule = MainsAnswerWritingRule()
    assert not rule.match(title)
