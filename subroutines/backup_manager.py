import json
import os
from pathlib import Path

import config as CONFIG

class BackupManager:
    """
    Handles tasks relating to taking backups of news articles
    """
    def __init__(self):
        self.backup_file = CONFIG.backup
        # Ensure that file exists
        Path(self.backup_file).parent.mkdir(parents=True, exist_ok=True)
        self.data = self._load()
    
    def _load(self):
        """
        Load JSON safely. Returns dict.
        """
        try:
            if not os.path.exists(self.backup_file):
                return {}
            
            with open(self.backup_file, "r", encoding="utf-8") as f:
                json_data = json.load(f)
                return json_data if isinstance(json_data, dict) else {}
        
        except json.JSONDecodeError:
            return {}

        except (OSError, IOError) as e:
            raise RuntimeError(
                f"Failed to read JSON file: {self.backup_file}"
            ) from e
    
    def flush(self):
        """
        Persist current data to disk.
        """
        self._save()

    
    def add(self, title, link, category, status, stars):

        """
        Append article and persist safely.
        """
        try:
            self.data[link] = {
                "Article Title":title,
                "Category":category,
                "Status":status,
                "Rating":stars
            }
        
        except (OSError, IOError) as e:
            raise RuntimeError("Failed to write article to JSON store") from e

    def _save(self):
        # Atomic Write
        temp_path = self.backup_file + ".tmp"

        try:
            with open(temp_path, 'w', encoding="utf-8") as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            
            os.replace(temp_path, self.backup_file)
        
        except Exception:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise
