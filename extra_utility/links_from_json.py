import os
import json

import config as CONFIG
from subroutines.backup_manager import BackupManager

def migrate_json_to_backup():
    
    source_path = r"C:\Users\Shiv\news-db-backup\article_backup.json"

    if not os.path.exists(source_path):
        raise FileNotFoundError (f"Source JSON not found: {source_path}")

    # Load source JSON
    with open(source_path, "r", encoding="utf-8-sig") as f:
        source_data = json.load(f)

    if not isinstance(source_data, dict):
        raise ValueError("Expected source JSON to be a dictionary")
    
    backupman = BackupManager()

    articles = source_data.values()

    count = 0

    for article in articles:
        name = article.get("Name", "").strip()
        url = article.get("URL", "").strip()
        category = article.get("Type", "").strip()

        if not url:
            continue  # Skip entries without URL
            
        # Use BackupManager class
        backupman.add(
            name, url, category, CONFIG.STATUS_DEFAULT, CONFIG.RATING_DEFAULT
        )
        count += 1

        if count % CONFIG.BATCH_SIZE == 0:
            backupman.flush()

    # Final flush
    backupman.flush() 

if __name__=="__main__":
    migrate_json_to_backup()