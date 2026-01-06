import feedparser
import os
import re
import json

import config as CONFIG

class FeedWatcher:

    def __init__(self):
        self.webpage = CONFIG.news_site
        self.articles = {}

    def check_feed(self):
        """
        It monitors rss feed using feedparser library and fetches all new news articles and links.

        Params:
            
        Returns:
            A dictionary of all links from the feed
        """

        news_feed = feedparser.parse(self.webpage)

        # displaying news titles.
        for news in news_feed.entries:
            # Storing the articles inside a file.
            article_name = news.title
            article_url = news.link

            




# Main code
if __name__ == "__main__":
    watchman = FeedWatcher()
    watchman.check_feed()
