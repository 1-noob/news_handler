import json
import os

import config as CONFIG
from subroutines.database_manager import DatabaseManager
from subroutines.hash_generator import HashGenerator



def migrate_backup_json():
    backup_path = CONFIG.backup

    if not os.path.exists(backup_path):
        raise FileNotFoundError(f"Backup JSON not found at: {backup_path}")

    # Load backup JSON
    with open(backup_path, "r", encoding="utf-8-sig") as f:
        backup_data = json.load(f)
    
    if not isinstance(backup_data, dict):
        raise ValueError("Expected backup JSON to be a dictionary")
    
    dbman = DatabaseManager()

    for url, article in backup_data.items():
        # Generate hash ID for URL
        hash_id = HashGenerator.get_hash_str(url)

        title = article.get("Article Title","").strip()
        category = article.get("Category","").strip()

        # Skip malformed entries
        if not url or not title:
            print(f"Skipping malformed entry for URL: {url} and title: {title}")
            continue

        # Insert into database
        inserted = dbman.insert_record(
            hash_id,
            title,
            category,
            url
        )

        if not inserted:
            print(f"Duplicate entry found for URL: {url}, skipping insertion.")



if __name__ == "__main__":
    migrate_backup_json()