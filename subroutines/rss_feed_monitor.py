import feedparser
import os
import re
import json
from pathlib import Path

from classification.classifier import ArticleClassifier
from classification.types import ClassificationStatus

import config as CONFIG

class FeedWatcher:

    def __init__(self):
        self.webpage = CONFIG.news_site
        self.articles = {}
        self.save_location = Path(CONFIG.CACHE_FILE)
        self.classifier = ArticleClassifier(CONFIG.SKIP_RULE, CONFIG.CLASSIFICATION_RULES)

        # Ensuring that the cache file exists
        self.save_location.parent.mkdir(parents=True, exist_ok=True)
     
    def _read_json(self) -> dict:
        """Read existing JSON or returns epmty dict"""
        if not self.save_location.exists():
            return {}

        try:
            with open(self.save_location, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            # Corrupted JSON file
            return {}
    
    def _write_json(self, data: dict):
        with open(self.save_location, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


    def check_feed(self):
        """
        It monitors rss feed using feedparser library and fetches all new news articles and links.

        Params:
            
        Returns:
            A dictionary of all links from the feed
        """

        news_feed = feedparser.parse(self.webpage)

        data = self._read_json()

        # working with news titles.
        for news in news_feed.entries:
            # Fetching the raw title 
            raw_title = news.title
            url = news.link

            # Sending it to classify and clean
            result = self.classifier.classify(raw_title)

            # Skipping SKIPPED articles
            if result.status == ClassificationStatus.SKIPPED:
                continue
            
            data[url]={
                "title": result.title,
                "category": result.category,
                "status": result.status.name
            }

        self._write_json(data)

            




# Main code
if __name__ == "__main__":
    watchman = FeedWatcher()
    watchman.check_feed()
