from enum import Enum
from dataclasses import dataclass
from typing import Optional

# define status for classification of title
class ClassificationStatus(Enum):
    CLASSIFIED = "classified"
    REVIEW_REQUIRED = "review_required"
    
    
    



# define a classification results
@dataclass(frozen=True)
class ClassificationResult:
    status: ClassificationStatus
    raw_title: str
    category: Optional[str] = None