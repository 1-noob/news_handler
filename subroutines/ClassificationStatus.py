from enum import Enum

class ClassificationStatus(Enum):
    ACCEPTED = "accepted"
    SKIPPED = "skipped"
    NEEDS_REVIEW = "needs_review"
