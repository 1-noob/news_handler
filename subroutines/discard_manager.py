import json 
from pathlib import Path
from typing import Set

import config as CONFIG 
from subroutines.hash_generator import HashGenerator

class DiscardManager:
    """
    Manages the discard list of news articles. So user are not asked to review the same article multiple times.
    """

    def __init__(self):
        self.discard_file = Path(CONFIG.DISCARD_FILE)
        self.discard_file.parent.mkdir(parents=True, exist_ok=True)

        self.cache: Set[str] = set()
        self._loaded = False

    def _read_json_once(self):
        """Reads the discard list from the JSON file once and keeps it in memory"""
        if self._loaded:
            return 
        
        if self.discard_file.exists():
            try:
                with open(self.discard_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                if isinstance(data, list):
                    self.cache = set(data)
                
            except (json.JSONDecodeError, IOError):
                    self.cache = set()

        self._loaded = True
            
    def _write_json(self):
        """Writes the discard list to the JSON file."""
        try:
            with open(self.discard_file, 'w', encoding='utf-8') as f:
                json.dump(list(self.cache), f, indent=4)
        except IOError as e:
            print(f"Error writing to discard file: {e}")

    def add_to_discard(self, article_url: str):
        """Adds an article URL to the discard list."""
        self._read_json_once()
        article_hash = HashGenerator.get_hash_str(article_url)
        
        if article_hash not in self.cache:
            self.cache.add(article_hash)
            self._write_json()

    def is_discarded(self, article_url: str) -> bool:
        """Checks if an article URL is in the discard list."""
        self._read_json_once()
        article_hash = HashGenerator.get_hash_str(article_url)
        return article_hash in self.cache