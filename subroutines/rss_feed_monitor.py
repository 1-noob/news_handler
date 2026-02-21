import feedparser
import os
import re
import json
from pathlib import Path

from classification.classifier import ArticleClassifier
from classification.types import ClassificationStatus
from subroutines.hash_generator import HashGenerator
from subroutines.database_manager import DatabaseManager
from subroutines.discard_manager import DiscardManager

import config as CONFIG

class FeedWatcher:

    def __init__(self):
        self.webpage = CONFIG.news_site
        self.articles = {}
        self.save_location = Path(CONFIG.CACHE_FILE)
        self.review_location = Path(CONFIG.REVIEW_FILE)
        self.classifier = ArticleClassifier(CONFIG.SKIP_RULE, CONFIG.CLASSIFICATION_RULES)
        self.dbMan = DatabaseManager()
        self.discardMan = DiscardManager()
        
        # Ensuring that the cache file exists
        self.save_location.parent.mkdir(parents=True, exist_ok=True)
        self.review_location.parent.mkdir(parents=True, exist_ok=True)
     
    def _read_json(self,path) -> dict:
        """Read existing JSON or returns empty dict"""
        if not path.exists():
            return {}

        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            # Corrupted JSON file
            return {}
    
    def _write_json(self, data: dict, path: Path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


    def check_feed(self):
        """
        It monitors rss feed using feedparser library and fetches all new news articles and links.

        Params:
            
        Returns:
            A dictionary of all links from the feed
        """

        news_feed = feedparser.parse(self.webpage)

        classified_data = self._read_json(self.save_location)
        review_data = self._read_json(self.review_location)

        # Remove already classified articles from review data to avoid duplicates
        review_data = {}
        raw_review = self._read_json(self.review_location)
        for url, article in raw_review.items():
            hash_id = HashGenerator.get_hash_str(url)
            if not self.discardMan.is_discarded(url) and not self.dbMan.check_duplicate(hash_id)    :
                review_data[url] = article

        stats = {
            "rss_entries": len(news_feed.entries),
            "skipped_quizzes": 0,
            "skipped_duplicates": 0,
            "classified": 0,
            "needs_review": 0,
            "new_articles": 0
        }
        
        # working with news titles.
        for news in news_feed.entries:
            # Fetching the raw title 
            raw_title = news.title
            url = news.link

            # Skipping quizes
            if "quiz" in raw_title.lower():
                stats["skipped_quizzes"] += 1
                continue
            
            hash_id = HashGenerator.get_hash_str(url)

            # Skip if already in discard list
            if self.discardMan.is_discarded(url) :
                stats["skipped_duplicates"] += 1
                continue
            
            if self.dbMan.check_duplicate(hash_id):
                # print(f"Skipping: {url}")
                stats["skipped_duplicates"] += 1
                continue

            # Classification
            result = self.classifier.classify(raw_title)
            
            record = {
                "title": result.title,
                "category": result.category,
                "status": result.status.name
            }

            if result.status == ClassificationStatus.CLASSIFIED and result.category is not None:
                classified_data[url] = record
                stats["classified"] += 1
            else:
                # Add only if not already in review data to avoid duplicates
                hash_id = HashGenerator.get_hash_str(url)
                if url not in review_data and not self.discardMan.is_discarded(hash_id):
                    review_data[url] = record
                    stats["needs_review"] += 1

            stats["new_articles"] += 1

        self._write_json(classified_data, self.save_location)
        self._write_json(review_data, self.review_location)
            
        return stats
            



# Main code
if __name__ == "__main__":
    watchman = FeedWatcher()
    stats = watchman.check_feed()
    print(json.dumps(stats, indent=4))
