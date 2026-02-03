import os
import time
import json
import hashlib
import subprocess
from datetime import datetime
from typing import Set, Dict

import config as CONFIG

class FileTracker:
    """Track file state using Hash comparision"""

    def __init__(self):
        self.file_path = CONFIG.backup
        self.last_hash = self._compute_hash()
    
    def _compute_hash(self) -> str:
        if not os.path(self.file_path):
            return ""
        
        with open(self.file_path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
        
    def has_changed(self) -> bool:
        current_hash = self._compute_hash()
        if current_hash != self.last_hash:
            self.last_hash = current_hash
            return True
        return False


class GitHandler:
    """
    Makes commit on the backup json file to a git repository with date-based commit message
    """

    def __init__(self):
        self.backup_path = CONFIG.backup

    def _run(self, command:list[str]):
        subprocess.run(
            command,
            cwd = self.backup_path,
            stdout = subprocess.DEVNULL,
            stderr = subprocess.DEVNULL,
            check = False
        )

    def stage_files(self, files: list[str]):
        self._run(["git","add", *files])

    def commit(self, message: str):
        self._run(["git", "commit", "-m", message])


class CommitMaker:
    """
    Commits backup.json when it changes
    """
    def __init__(self):
        # (Resolve the path issue)
        self.repo_dir = os.path.abspath(os.path.dirname(CONFIG.backup))
        self.backup_file = os.path.basename(CONFIG.backup)
        self.file_path = os.path.join(self.repo_dir, self.backup_file)
        self.tracker = FileTracker()
        self.git = GitHandler()

    def commit_if_needed(self) -> str|None:
        """
        Checks if backup json file has changed and commits it
        """
        if not self.tracker.has_changed():
            return None
        
        commit_msg = self.build_commit_message()
        self.git.stage_files([self.backup_file])
        self.git.commit(commit_msg)
        return commit_msg
    
    @staticmethod
    def _build_commit_message() -> str:
        today = datetime.now().strftime("%-d-%m-%Y")
        return f"Data entry for {today}"