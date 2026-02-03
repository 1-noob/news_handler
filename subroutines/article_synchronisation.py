import json
import asyncio
from pathlib import Path
from typing import Dict

import config as CONFIG
from subroutines.database_manager import DatabaseManager
from subroutines.hash_generator import HashGenerator
from subroutines.backup_manager import BackupManager

class ArticleSyncService:
    """
    Handles inserting articles from json files into MongoDB
    API Ready service layer
    """

    def __init__(self, json_path: Path):
        self.json_path = json_path
        self.dbMan = DatabaseManager()
        self.backupMan = BackupManager()

    def load_articles(self)-> Dict:
        if not self.json_path.exists():
            raise FileNotFoundError(f"File not found: {self.json_path}")
        
        with open(self.json_path, 'r', encoding="utf-8") as f:
            data=json.load(f)
        
        if not isinstance(data,dict):
            raise ValueError("Expected JSON to be a dictionary")
        
        return data
    
    async def _insert_single(self, url: str, article: dict) -> bool:
        """
        Inserts a single article asynchronously.
        """

        hash_id = HashGenerator.get_hash_str(url)

        # duplicate check (async-safe)

        if await asyncio.to_thread(self.dbMan.check_duplicate, hash_id):
            return False
        
        title = article.get("title","").strip()
        category = article.get("category","").strip()

        if not title or not category:
            return False

        success = await asyncio.to_thread(
            self.dbMan.insert_record,
            hash_id,
            title,
            category,
            url
        )

        if not success:
            return False
        
        await asyncio.to_thread(
            self.backupMan.add,
            title, 
            url,
            category,
            CONFIG.STATUS_DEFAULT,
            CONFIG.RATING_DEFAULT
        )
        await asyncio.to_thread(self.backupMan.flush)
        return True

    async def _batch_insert(self) -> Dict:
        """
        Batch inserts all articles asynchronously.
        Returns stats dict for API
        """
        articles = self.load_articles()

        tasks = [
            self._insert_single(url, article)
            for url, article in articles.items()
        ]

        results = await asyncio.gather(tasks)

        return {
            "inserted": sum(results),
            "skipped": len(results) - sum(results),
            "total": len(results)
        }



