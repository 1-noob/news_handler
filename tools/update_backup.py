import os
import json

import config as CONFIG
from subroutines.backup_manager import BackupManager


def sync_backup_to_new():
    source_path = r"C:\Users\Shiv\news-db-backup\article_backup.json"  # old backup
    new_path = CONFIG.backup  # current backup json

    if not os.path.exists(source_path):
        raise FileNotFoundError(f"Old backup JSON not found: {source_path}")

    # Load old backup JSON
    with open(source_path, "r", encoding="utf-8-sig") as f:
        source_data = json.load(f)

    if not isinstance(source_data, dict):
        raise ValueError("Expected old backup JSON to be a dictionary")

    # Build URL set from new backup JSON once
    if os.path.exists(new_path):
        with open(new_path, "r", encoding="utf-8-sig") as f:
            new_data = json.load(f)

            if isinstance(new_data, dict):
                current_urls = set(new_data.keys())
            else:
                raise ValueError ("Unexpected format in new backup JSON")

    else:
        current_urls = set()

    backupman = BackupManager()

    added = 0

    for article in source_data.values():
        url = article.get("URL", "").strip()

        if not url or url in current_urls:
            continue

        backupman.add(
            article.get("Name", "").strip(),
            url,
            article.get("Type", "").strip(),
            CONFIG.STATUS_DEFAULT,
            CONFIG.RATING_DEFAULT
        )

        current_urls.add(url)  # <<<< KEY FIX
        added += 1

        if added % CONFIG.BATCH_SIZE == 0:
            backupman.flush()

    backupman.flush()

    print(f"Added {added} new articles.")


if __name__ == "__main__":
    sync_backup_to_new()
