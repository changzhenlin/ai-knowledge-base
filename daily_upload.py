#!/usr/bin/env python3
"""
Daily AI Knowledge Base Updater
Uploads 1-3 random markdown files to the GitHub repository daily
"""

import os
import random
import subprocess
from datetime import datetime

WORKSPACE_DIR = "/Users/tyler/.openclaw/workspace"
KNOWLEDGE_BASE_DIR = f"{WORKSPACE_DIR}/ai-knowledge-base"
EXCLUDED_FILES = {"README.md", "SETUP.md", "TODO.md", "LICENSE"}

def find_markdown_files():
    """Find all markdown files in workspace, excluding specified files."""
    markdown_files = []
    for root, dirs, files in os.walk(WORKSPACE_DIR):
        # Skip hidden directories and ai-knowledge-base itself
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'ai-knowledge-base']
        
        for file in files:
            if file.endswith('.md') and file not in EXCLUDED_FILES:
                full_path = os.path.join(root, file)
                markdown_files.append(full_path)
    return markdown_files

def select_files_to_upload(available_files, count=3):
    """Randomly select files to upload."""
    if len(available_files) <= count:
        return available_files
    return random.sample(available_files, count)

def copy_to_knowledge_base(files):
    """Copy selected files to knowledge base with proper categorization."""
    copied_files = []
    
    for file_path in files:
        filename = os.path.basename(file_path)
        relative_path = os.path.relpath(file_path, WORKSPACE_DIR)
        
        # Determine category based on filename/content
        category = determine_category(filename, file_path)
        
        # Create category directory if it doesn't exist
        category_dir = f"{KNOWLEDGE_BASE_DIR}/{category}"
        os.makedirs(category_dir, exist_ok=True)
        
        # Copy file
        subprocess.run(f"cp '{file_path}' '{category_dir}/{filename}'", shell=True)
        
        copied_files.append(f"{category_dir}/{filename}")
    
    return copied_files

def determine_category(filename, filepath):
    """Determine the category for a file based on its content and name."""
    filename_lower = filename.lower()
    
    # Category mappings
    if any(keyword in filename_lower for keyword in ['interview', 'question', 'leetcode']):
        return 'interview-preparation'
    elif any(keyword in filename_lower for keyword in ['rag', 'llm', 'nlp', 'language', 'transformer']):
        return 'nlp'
    elif any(keyword in filename_lower for keyword in ['vision', 'image', 'computer', 'cv']):
        return 'computer-vision'
    elif any(keyword in filename_lower for keyword in ['ml', 'machine', 'learning', 'algorithm']):
        return 'machine-learning'
    elif any(keyword in filename_lower for keyword in ['deep', 'neural', 'network', 'cnn', 'rnn']):
        return 'deep-learning'
    elif any(keyword in filename_lower for keyword in ['ethics', 'responsible', 'bias', 'fairness']):
        return 'ai-ethics'
    elif any(keyword in filename_lower for keyword in ['tool', 'framework', 'library', 'api']):
        return 'tools'
    else:
        # Default category for AI-related content
        return 'nlp'

def git_commit_and_push():
    """Commit and push changes to GitHub."""
    os.chdir(KNOWLEDGE_BASE_DIR)
    
    # Check if there are changes
    result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    
    if result.stdout.strip():
        # Add all changes
        subprocess.run("git add .", shell=True)
        
        # Create commit message
        date_str = datetime.now().strftime("%Y-%m-%d")
        commit_msg = f"Daily update: {date_str} - Added AI knowledge base documents"
        
        # Commit
        subprocess.run(f"git commit -m '{commit_msg}'", shell=True)
        
        # Push
        subprocess.run("git push origin main", shell=True)
        
        print("✓ Successfully pushed changes to GitHub")
        return True
    else:
        print("No changes to commit")
        return False

def main():
    """Main function to run daily update."""
    print(f"Starting daily AI Knowledge Base update: {datetime.now()}")
    
    # Change to workspace directory
    os.chdir(WORKSPACE_DIR)
    
    # Find markdown files
    available_files = find_markdown_files()
    print(f"Found {len(available_files)} available markdown files")
    
    if not available_files:
        print("No files to upload")
        return
    
    # Select files to upload
    files_to_upload = select_files_to_upload(available_files, min(3, len(available_files)))
    print(f"Selected {len(files_to_upload)} files for upload:")
    for file in files_to_upload:
        print(f"  - {os.path.basename(file)}")
    
    # Copy files to knowledge base
    copied_files = copy_to_knowledge_base(files_to_upload)
    print(f"Copied {len(copied_files)} files to knowledge base")
    
    # Commit and push
    success = git_commit_and_push()
    
    if success:
        print("✓ Daily update completed successfully")
    else:
        print("Daily update completed (no changes)")

if __name__ == "__main__":
    main()