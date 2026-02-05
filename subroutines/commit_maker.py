import os
import time
import subprocess
from datetime import datetime

import config as CONFIG


class GitHandler:
    """
    Makes commit on the backup json file to a git repository with date-based commit message
    """

    def __init__(self):
        self.repo_dir = os.path.abspath(os.path.dirname(CONFIG.backup))


    def _run(self, command:list[str]):
        return subprocess.run(
            command,
            cwd = self.repo_dir,
            stdout = subprocess.PIPE,
            stderr = subprocess.DEVNULL,
            text = True,
            check = False
        )

    def has_changes(self):
        result = self._run(["git","status", "--porcelain"])
        return bool(result.stdout.strip())
    
    def stage_files(self, files: list[str]):
        self._run(["git", "add", *files])

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
        self.git = GitHandler()

    def commit_if_needed(self) -> str|None:
        """
        Checks if backup json file has changed and commits it
        """
        if not self.git.has_changes():
            return None
        
        commit_msg = self._build_commit_message()
        self.git.stage_files([self.backup_file])
        self.git.commit(commit_msg)
        return commit_msg
    
    @staticmethod
    def _build_commit_message() -> str:
        today = datetime.now()
        return f"Data entry for {today.day}-{today.month:02d}-{today.year}"
    
if __name__ == "__main__":
    commit_maker = CommitMaker()

    commit_msg = commit_maker.commit_if_needed()
    if commit_msg:
        print(f"Committed: {commit_msg}")
