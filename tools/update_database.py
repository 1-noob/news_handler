import json
import os

import config as CONFIG
from subroutines.database_manager import DatabaseManager
from subroutines.hash_generator import HashGenerator


def sync_backup_to_database():
    """
    Detects new articles in backup.json and pushes only those into MongoDB.
    """

    backup_path = CONFIG.backup

    if not os.path.exists(backup_path):
        raise FileNotFoundError(f"Backup JSON not found at: {backup_path}")

    # Load backup JSON
    with open(backup_path, "r", encoding="utf-8-sig") as f:
        backup_data = json.load(f)

    if not isinstance(backup_data, dict):
        raise ValueError("Expected backup JSON to be a dictionary")

    dbman = DatabaseManager()

    inserted = 0
    skipped = 0

    for url, article in backup_data.items():
        hash_id = HashGenerator.get_hash_str(url)

        # Skip if already present in DB
        if dbman.check_duplicate(hash_id):
            skipped += 1
            continue

        title = article.get("Article Title", "").strip()
        category = article.get("Category", "").strip()

        if not title or not category:
            skipped += 1
            continue

        success = dbman.insert_record(
            hash_id=hash_id,
            title=title,
            category=category,
            url=url
        )

        if success:
            inserted += 1

    # Final status message
    if inserted == 0:
        print("Database is already in sync. No new articles found.")
    else:
        print(f"Inserted {inserted} new article(s) into the database. Skipped {skipped} existing/invalid entries.")


if __name__ == "__main__":
    sync_backup_to_database()
