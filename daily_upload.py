#!/usr/bin/env python3
"""
Daily AI Knowledge Base Updater
Uploads AI knowledge base changes to GitHub.
"""

import os
import subprocess
from datetime import datetime

WORKSPACE_DIR = "/Users/tyler/.openclaw/workspace"
KNOWLEDGE_BASE_DIR = f"{WORKSPACE_DIR}/ai-knowledge-base"


def git_commit_and_push():
    os.chdir(KNOWLEDGE_BASE_DIR)
    result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)

    if result.stdout.strip():
        subprocess.run("git add .", shell=True, check=False)
        date_str = datetime.now().strftime("%Y-%m-%d")
        commit_msg = f"Daily AI news update: {date_str}"
        subprocess.run(f"git commit -m '{commit_msg}'", shell=True, check=False)
        subprocess.run("git push origin main", shell=True, check=False)
        print("✓ Successfully pushed changes to GitHub")
        return True
    else:
        print("No changes to commit")
        return False


def main():
    print(f"Starting AI Knowledge Base upload: {datetime.now()}")
    success = git_commit_and_push()

    if success:
        print("✓ Daily upload completed successfully")
    else:
        print("Daily upload completed (no changes)")


if __name__ == "__main__":
    main()
