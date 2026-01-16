import pytest
from rules.upsc_key import UpscKeyRule

pos_titles = [
    "UPSC Key: India-Germany relations, Pax Silica, and Venezuela’s crude oil",
    "UPSC Key: Iran protests, Merz-Modi meet, and Zehanpora stupas",
    "UPSC Key: National IED Data Management System, NATO, and Trump’s Russia sanctions bill",
    "UPSC Key: Economic reforms & fiscal policy overview"
]

neg_titles = [
    "Key issues in UPSC exam strategy",
    "Understanding Key Concepts for UPSC",
    "India & Germany relations explained",
    "UPSC syllabus changes for 2026",
    "UPSC Current Affairs highlights"
]

@pytest.mark.parametrize("title", pos_titles)
def test_upsc_key_positive(title):
    rule = UPSCKeyRule()
    assert rule.match(title)

@pytest.mark.parametrize("title", neg_titles)
def test_upsc_key_negative(title):
    rule = UPSCKeyRule()
    assert not rule.match(title)
