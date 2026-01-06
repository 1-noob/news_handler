import os
import json

import config as CONFIG
from subroutines.backup_manager import BackupManager

def migrate_json_to_backup():
    
    destination_path = CONFIG.backup
    source_path = r"C:\Users\Shiv\news-db-backup\article_backup.json"

    if not os.path.exists(source_path):
        raise FileNotFoundError (f"Source JSON not found: {source_path}")

    # Load source JSON
    with open(source_path, "r", encoding="utf-8-sig") as f:
        source_data = json.load(f)

    if not isinstance(source_data, dict):
        raise ValueError("Expected source JSON to be a dictionary")
    
    backupman = BackupManager()

    # Support both dict ad list inputs
    if isinstance(source_data, dict):
        articles = source_data.values()
    elif isinstance(source_data, list):
        article = source_data
    else:
        raise ValueError("Unsupported JSON structure")

    for _,article in source_data.items():
        name = article.get("Name", "").strip()
        url = article.get("URL", "").strip()
        category = article.get("Type", "").strip()

        # Defaults
        status = 0
        rating = 1

        # Use BackupManager class
        backupman.add(
            name, url, category, status, rating
        )

if __name__=="__main__":
    migrate_json_to_backup()