import feedparser
import os
import re
import json
from pathlib import Path

from classification.classifier import ArticleClassifier
from classification.types import ClassificationStatus
from subroutines.hash_generator import HashGenerator

import config as CONFIG

class FeedWatcher:

    def __init__(self):
        self.webpage = CONFIG.news_site
        self.articles = {}
        self.save_location = Path(CONFIG.CACHE_FILE)
        self.review_location = Path(CONFIG.REVIEW_FILE)
        self.classifier = ArticleClassifier(CONFIG.SKIP_RULE, CONFIG.CLASSIFICATION_RULES)

        # Ensuring that the cache file exists
        self.save_location.parent.mkdir(parents=True, exist_ok=True)
        self.review_location.parent.mkdir(parents=True, exist_ok=True)
     
    def _read_json(self,path) -> dict:
        """Read existing JSON or returns epmty dict"""
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
        
        # working with news titles.
        for news in news_feed.entries:
            # Fetching the raw title 
            raw_title = news.title
            url = news.link

            # Skipping quizes
            if "quiz" in raw_title.lower():
                continue
            
            hash_id = HashGenerator.generate(url)
            if self.dbMan.check_duplicate(hash_id):
                # print(f"Skipping: {url}")
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
            else:
                review_data[url] = record

        self._write_json(classified_data, self.save_location)
        self._write_json(review_data, self.review_location)
            




# Main code
if __name__ == "__main__":
    watchman = FeedWatcher()
    watchman.check_feed()
