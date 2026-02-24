import json
from pathlib import Path
from typing import Dict

import config as CONFIG
from subroutines.database_manager import DatabaseManager
from subroutines.hash_generator import HashGenerator
from subroutines.backup_manager import BackupManager
from subroutines.discard_manager import DiscardManager
from subroutines.commit_maker import CommitMaker


class Reviewer:
    """
    Handles manual supervision to deal with skipped articles
    """

    def __init__(self):
        self.review_path = Path(CONFIG.REVIEW_FILE)
        self.dbMan = DatabaseManager()
        self.backupMan = BackupManager()
        self.discardMan = DiscardManager()
        self.commitMaker = CommitMaker()

    def _response(self, success: bool, status: str, message: str = None, data: Dict = None) -> Dict:
        """Helper response builder."""
        return {
            "success": success,
            "status": status,
            "message": message,
            "data": data
        }

    def load_review_articles(self) -> Dict:
        if not self.review_path.exists():
            # raise FileNotFoundError(f"Review file not found: {self.review_path}")
            return {}
        
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

        # Handle empty review.json        
        review_data = self.load_review_articles()
        if not review_data:
            print("Review.json is empty")
            
            # Ensure backup file is up to date
            self.backupMan.flush() 

            # Commit discard file if needed
            discard_msg = self.commitMaker.commit_discard_if_needed()   
            if discard_msg:
                print(discard_msg)

            return
        
        remaining = {}

        print(f"\nLoaded {len(review_data)} articles for review. \n")

        for url,article in review_data.items():

            # Skip if article is in discard list
            if self.discardMan.is_discarded(url):
                continue

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
                # Discard article forever
                print("Article discarded.")
                self.discardMan.add_to_discard(url)
                continue

            # -------------------------
            # Category handling
            # -------------------------
            if choice == "1":
                category = input("Enter category name: ").strip()
                if not category:
                    print("Empty category. Article kept in review file.")
                    remaining[url] = article
                    continue

            elif choice == "2":
                category = CONFIG.SPECIAL_REVIEW_CATEGORY

            else:
                print("Invalid choice. Article kept in review file.")
                remaining[url] = article
                continue

            # -------------------------
            # Insert into DB
            # -------------------------
            hash_id = HashGenerator.get_hash_str(url)

            if self.dbMan.check_duplicate(hash_id):
                print("Article already exists in DB. Removing from the file.")
                continue

            success = self.dbMan.insert_record(
                hash_id=hash_id,
                title=raw_title,
                category=category,
                url=url
            )

            if success:
                print("Article inserted into database.")

                # Adding to backup file
                self.backupMan.add(
                    title = raw_title,
                    link = url,
                    category = category,
                    status = CONFIG.STATUS_DEFAULT,
                    stars = CONFIG.RATING_DEFAULT 
                )
            else:
                print("Failed to insert. Article kept in review file.")
                remaining[url] = article
                continue
        
        self.backupMan.flush()

        # Save leftover articles (if any)
        self.save_review_articles(remaining)

        # Commit changes in discard file (if any)
        discard_msg = self.commitMaker.commit_discard_if_needed()

        print("\nReview session completed.")
        print(f"Review completed. {len(remaining)} articles remain in review file.")
        if discard_msg:
            print(discard_msg)


    def process_review_api (self, action:str, url:str = None, category:str = None) -> Dict:
        """
        API version of the review processor.
        Handles one article at a time and returns a structured response.
        """

        review_data = self.load_review_articles()

        # GET NEXT ARTICLE
        if action == "get_next":
            for article_url, article in review_data.items():
                if not self.discardMan.is_discarded(url):
                    return {
                        "status": "success", 
                        "action": "get_next", 
                        "article": {
                            "url": url, 
                            "title": article.get("title", "")
                            }
                        }
            return {
                "success": True,
                "status": "empty",
                "article": None
            }
        
        # VALIDATION
        if not url or url not in review_data:
            return {
                "success": False,
                "status": "failed",
                "message": "Invalid or missing URL"
            }
        
        article = review_data[url]
        raw_title = article.get("title", "").strip()

        try:
            # DISCARD
            if action == "discard":
                self.discardMan.add_to_discard(url)
                review_data.pop(url, None)

            # INSERT WITH CATEGORY
            elif action == "insert_prebuilt":
                if not category:
                    return {
                        "success": False,
                        "status": "failed",
                        "error": "Category must be provided for insert_prebuilt action"
                    }
                
                hash_id = HashGenerator.get_hash_str(url)

                # Duplicate check
                if self.dbMan.check_duplicate(hash_id):
                    review_data.pop(url, None)
                
                else:
                    success = self.dbMan.insert_record(
                        hash_id=hash_id,
                        title=raw_title,
                        category=category,
                        url=url
                    )

                    if not success:
                        return {
                            "success": False,   
                            "status": "failed",
                            "message": "Failed to insert into DB"
                        }
                    
                    self.backupMan.add(
                        title = raw_title,  
                        link = url,
                        category = category,
                        status = CONFIG.STATUS_DEFAULT,
                        stars = CONFIG.RATING_DEFAULT
                    )
                    review_data.pop(url, None)
            
            # INSERT WITH SPECIAL CATEGORY
            elif action == "insert_special":
                category = CONFIG.SPECIAL_REVIEW_CATEGORY
                hash_id = HashGenerator.get_hash_str(url)

                if not self.dbMan.check_duplicate(hash_id):
                    success = self.dbMan.insert_record(
                        hash_id=hash_id,
                        title=raw_title,
                        category=category,
                        url=url
                    )

                    if success:
                        self.backupMan.add(
                            title = raw_title,
                            link = url,
                            category = category,
                            status = CONFIG.STATUS_DEFAULT,
                            stars = CONFIG.RATING_DEFAULT 
                        )
                review_data.pop(url, None)
            else:
                return {
                    "success": False,
                    "status": "failed",
                    "message": "Failed to insert into DB"
                }

            # FINALIZE CHANGES
            self.backupMan.flush()
            self.save_review_articles(review_data)
            self.commitMaker.commit_discard_if_needed()

            # RETURN NEXT ARTICLE
            for next_url, next_article in review_data.items():
                if not self.discardMan.is_discarded(next_url):
                    return {
                        "success": True,
                        "status": "completed",
                        "article": {
                            "url": next_url,
                            "title": next_article.get("title", "")
                        }
                    }
                
            return {
                "success": True,
                "status": "completed",
                "next_article": None
            }
            

        except Exception as e:
            return {
                "success": False,
                "status": "failed",
                "message": str(e)
            }
        



if __name__ == "__main__":
    from pathlib import Path
    Reviewer().process_review()
