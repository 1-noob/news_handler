import os
import json
import subprocess
from datetime import datetime

import config as CONFIG
from subroutines.database_manager import DatabaseManager


def run_git(command: list[str], cwd: str):
    return subprocess.run(
        command,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False
    )


def confirm_deletion(path: str) -> bool:
    answer = input(
        f"backup.json exists at:\n{path}\n"
        "Do you want to delete and rebuild it? (yes/no): "
    ).strip().lower()
    return answer == "yes"


def rebuild_backup_from_database(backup_path: str):
    db = DatabaseManager()

    records = db.collection.find()

    backup_data = {}

    for doc in records:
        url = doc.get("URL")
        if not url:
            continue
    
        backup_data[url] = {
            "Article Title": doc.get("Article Title"),
            "Category": doc.get("Category"),
            "Status": doc.get("Status"),    
            "Rating": doc.get("Rating")
        }

    with open(backup_path, "w", encoding="utf-8") as f:
        json.dump(backup_data, f, indent=4)

    print(f"Rebuilt backup with {len(backup_data)} articles")


def commit_backup(repo_dir: str, backup_file: str):
    today = datetime.now()
    commit_msg = (
        f"Backup reinitialisation on "
        f"{today.day:02d}-{today.month:02d}-{today.year}"
    )

    run_git(["git", "add", backup_file], repo_dir)
    result = run_git(["git", "commit", "-m", commit_msg], repo_dir)

    if "nothing to commit" in result.stdout.lower():
        print("Nothing to commit")
    else:
        print(f"Committed: {commit_msg}")


def main():
    repo_dir = os.path.abspath(os.path.dirname(CONFIG.backup))
    backup_path = os.path.abspath(CONFIG.backup)
    backup_file = os.path.basename(backup_path)

    if os.path.exists(backup_path):
        if not confirm_deletion(backup_path):
            print("Aborted by user")
            return
        os.remove(backup_path)

    rebuild_backup_from_database(backup_path)
    commit_backup(repo_dir, backup_file)


if __name__ == "__main__":
    main()
