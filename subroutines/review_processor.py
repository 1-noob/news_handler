import json
from pathlib import Path
from typing import Dict

import config as CONFIG
from subroutines.database_manager import DatabaseManager
from subroutines.hash_generator import HashGenerator


class Reviewer:
    """
    Handles manual supervision to deal with skipped articles
    """

    def __init__(self, review_path: Path):
        self.review_path = review_path
        self.dbMan = DatabaseManager()

    def load_review_articles(self) -> Dict:
        if not self.review_path.exists():
            raise FileNotFoundError(f"Review file not found: {self.review_path}")
        
        with open(self.review_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            raise ValueError("Expected json to be a dictionary")

        return data

    def save_review_articles(self, data: Dict):
        """ Save updated review file. """
        with open(self.review_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    # review loop
    def process_review(self):
        
        review_data = self.load_review_articles()
        remaining = {}

        print(f"\nLoaded {len(review_data)} articles for review. \n")

        for url,article in review_data.items():
            raw_title = article.get("title", "").strip()

            print("\n" + "=" * 80)
            print(f"TITLE:\n{raw_title}")
            print("=" * 80)

            print("\nChoose an action:")
            print("1. Insert into DB (choose category)")
            print("2. Insert into DB with SPECIAL category")
            print("3. Discard article")

            choice = input("\nEnter choice (1 / 2 / 3): ").strip()

            # -------------------------
            # Discard
            # -------------------------
            if choice == "3":
                print("❌ Article discarded.")
                continue

            # -------------------------
            # Category handling
            # -------------------------
            if choice == "1":
                category = input("Enter category name: ").strip()
                if not category:
                    print("⚠ Empty category. Article kept in review file.")
                    remaining[url] = article
                    continue

            elif choice == "2":
                category = CONFIG.SPECIAL_REVIEW_CATEGORY

            else:
                print("⚠ Invalid choice. Article kept in review file.")
                remaining[url] = article
                continue

            # -------------------------
            # Insert into DB
            # -------------------------
            hash_id = HashGenerator.get_hash_str(url)

            if self.dbMan.check_duplicate(hash_id):
                print("⚠ Article already exists in DB. Skipping.")
                continue

            success = self.dbMan.insert_record(
                hash_id=hash_id,
                title=raw_title,
                category=category,
                url=url
            )

            if success:
                print("✅ Article inserted into database.")
            else:
                print("⚠ Failed to insert. Article kept in review file.")
                remaining[url] = article

        # Save leftover articles (if any)
        self.save_review_articles(remaining)

        print("\nReview session completed.")
        print(f"Remaining articles in review file: {len(remaining)}")
