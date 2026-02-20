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

    def _read_json(self):
        """Reads the discard list from the JSON file."""
        if not self.discard_file.exists():
            return set()
        
        try:
                with open(self.discard_file, 'r') as f:
                    data = json.load(f)
                
                if not isinstance(data, list):
                    return set()
                return set(data)
            
        except (json.JSONDecodeError, IOError):
                return set()
        
    def _write_json(self, discard_set: Set[str]):
        """Writes the discard list to the JSON file."""
        try:
            with open(self.discard_file, 'w') as f:
                json.dump(list(discard_set), f, indent=4)
        except IOError as e:
            print(f"Error writing to discard file: {e}")

    def add_to_discard(self, article_url: str):
        """Adds an article URL to the discard list."""
        discard_set = self._read_json()
        article_hash = HashGenerator.get_hash_str(article_url)
        
        if article_hash not in discard_set:
            discard_set.add(article_hash)
            self._write_json(discard_set)

    def is_discarded(self, article_url: str) -> bool:
        """Checks if an article URL is in the discard list."""
        discard_set = self._read_json()
        article_hash = HashGenerator.get_hash_str(article_url)
        return article_hash in discard_set