"""
Configuration template for news_handler.

Copy this file to `config.py` and fill in the required values
before running the project.
"""

# RSS Feed Configuration
NEWS_SITE = "https://indianexpress.com/section/upsc-current-affairs/feed/"


# File Storage Paths

# Path to store newly fetched article links
CACHE_FILE = "<PATH_TO>/article_cache/new_articles.json"

# Path to store articles pending manual review
REVIEW_FILE = "<PATH_TO>/article_cache/review.json"

# Path to backup file (used for git commits)
    # Ideally in a seperate folder
BACKUP_FILE = "<PATH_TO>/backup.json"


# Processing Configuration

BATCH_SIZE = 5          # Number of articles processed in one run
RATING_DEFAULT = 1      # Default rating for newly inserted articles
STATUS_DEFAULT = 0      # Default status flag


# Database Configuration

DB_URI = "<DATABASE_URI>"
DB_NAME = "<DATABASE_NAME>"
DB_COLLECTION = "<COLLECTION_NAME>"


# Classification Rules

from rules.art_and_culture import ArtAndCultureRule
from rules.beyond_trending import BeyondTrendingRule
from rules.current_affairs import CurrentAffairsRule
from rules.ethics_simplified import EthicsSimplifiedRule
from rules.issue_at_a_glance import IssueAtAGlanceRule
from rules.knowledge_nugget import KnowledgeNuggetRule
from rules.mains_answer_writing import MainsAnswerWritingRule
from rules.upsc_key import UpscKeyRule
from rules.world_this_week import WorldThisWeekRule

CLASSIFICATION_RULES = [
    ArtAndCultureRule(),
    BeyondTrendingRule(),
    EthicsSimplifiedRule(),
    IssueAtAGlanceRule(),
    KnowledgeNuggetRule(),
    MainsAnswerWritingRule(),
    UpscKeyRule(),
    WorldThisWeekRule(),
    CurrentAffairsRule(),
]


# Skip Rules

from rules.skip_rule import SkipRule

SKIP_RULES = [
    SkipRule(),
]


# Review Configuration

SPECIAL_REVIEW_CATEGORY = "Inserted manually"
