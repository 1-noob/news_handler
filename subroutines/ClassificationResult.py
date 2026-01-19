from dataclasses import dataclass
from typing import Optional

@dataclass
class ClassificationResult:
    status: ClassificationStatus
    url: str
    raw_title: str
    
    category: Optional[str] = None
    clean_title: Optional[str] = None
    reason: Optional[str] = None
