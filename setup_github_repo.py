#!/usr/bin/env python3
"""
Setup script for AI Knowledge Base GitHub Repository
This script creates a GitHub repository and sets up automation for daily updates.
"""

import os
import subprocess
import sys
from datetime import datetime

def run_command(command, check=True):
    """Execute a shell command and return the result."""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True, check=check)
    if result.stdout:
        print(f"Output: {result.stdout}")
    if result.stderr:
        print(f"Stderr: {result.stderr}")
    return result

def check_github_cli():
    """Check if GitHub CLI is installed."""
    try:
        result = run_command("gh --version", check=False)
        if result.returncode == 0:
            print("✓ GitHub CLI is installed")
            return True
        else:
            print("✗ GitHub CLI is not installed")
            return False
    except Exception as e:
        print(f"✗ Error checking GitHub CLI: {e}")
        return False

def install_github_cli():
    """Install GitHub CLI if not present."""
    print("Installing GitHub CLI...")
    try:
        # Try different installation methods
        if run_command("which brew", check=False).returncode == 0:
            run_command("brew install gh")
        else:
            print("Homebrew not found, trying alternative installation...")
    except Exception as e:
        print(f"Failed to install GitHub CLI: {e}")
        return False
    return True

def create_github_repo(repo_name, description):
    """Create a GitHub repository."""
    try:
        # Check if already logged in
        result = run_command("gh auth status", check=False)
        if result.returncode != 0:
            print("Please log in to GitHub CLI first:")
            run_command("gh auth login")
        
        # Create repository
        run_command(f"gh repo create {repo_name} --public --description '{description}' --source=. --remote=origin")
        
        # Push initial commit
        run_command("git push -u origin main")
        
        return True
    except Exception as e:
        print(f"Failed to create GitHub repository: {e}")
        return False

def setup_daily_upload_cron():
    """Set up a cron job for daily markdown uploads."""
    cron_script = '''#!/usr/bin/env python3
"""
Daily AI Knowledge Base Updater
Uploads 1-3 random markdown files to the GitHub repository daily
"""

import os
import random
import subprocess
import glob
from datetime import datetime

WORKSPACE_DIR = "/Users/tyler/.openclaw/workspace"
KNOWLEDGE_BASE_DIR = f"{WORKSPACE_DIR}/ai-knowledge-base"
EXCLUDED_FILES = {"README.md", "SETUP.md", "TODO.md", "LICENSE", "*.py", "*.sh"}

def find_markdown_files():
    """Find all markdown files in workspace, excluding specified files."""
    markdown_files = []
    for root, dirs, files in os.walk(WORKSPACE_DIR):
        # Skip hidden directories and ai-knowledge-base itself
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'ai-knowledge-base']
        
        for file in files:
            if file.endswith('.md') and not any(file.endswith(excl.replace('*', '')) for excl in EXCLUDED_FILES if '*' in excl):
                if file not in EXCLUDED_FILES:
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
    elif any(keyword in filename_lower for keyword in ['rag', 'llm', 'nlp', 'language']):
        return 'nlp'
    elif any(keyword in filename_lower for keyword in ['vision', 'image', 'computer']):
        return 'computer-vision'
    elif any(keyword in filename_lower for keyword in ['ml', 'machine', 'learning']):
        return 'machine-learning'
    elif any(keyword in filename_lower for keyword in ['deep', 'neural', 'network']):
        return 'deep-learning'
    elif any(keyword in filename_lower for keyword in ['ethics', 'responsible', 'bias']):
        return 'ai-ethics'
    elif any(keyword in filename_lower for keyword in ['tool', 'framework', 'library']):
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
'''
    
    # Write the script
    with open(f"{KNOWLEDGE_BASE_DIR}/daily_upload.py", "w") as f:
        f.write(cron_script)
    
    # Make it executable
    run_command(f"chmod +x {KNOWLEDGE_BASE_DIR}/daily_upload.py")
    
    # Create cron job (run daily at 9 AM)
    cron_entry = f"0 9 * * * cd {KNOWLEDGE_BASE_DIR} && python3 daily_upload.py >> /tmp/ai_knowledge_base_update.log 2>&1"
    
    # Add to crontab
    run_command(f'(crontab -l 2>/dev/null; echo "{cron_entry}") | crontab -')
    
    print("✓ Daily upload cron job configured")
    print("  Cron: 0 9 * * * (9 AM daily)")

def main():
    """Main setup function."""
    repo_name = "ai-knowledge-base"
    description = "A curated collection of AI development knowledge - automatically updated daily with 1-3 markdown documents"
    
    print("🚀 Setting up AI Knowledge Base GitHub Repository")
    print("=" * 60)
    
    # Check/install GitHub CLI
    if not check_github_cli():
        if not install_github_cli():
            print("Failed to install GitHub CLI. Please install manually and run this script again.")
            sys.exit(1)
    
    # Create GitHub repository
    print(f"\n📁 Creating GitHub repository: {repo_name}")
    if create_github_repo(repo_name, description):
        print("✓ GitHub repository created successfully")
    else:
        print("Failed to create GitHub repository")
        sys.exit(1)
    
    # Setup daily upload automation
    print("\n⚙️ Setting up daily upload automation")
    setup_daily_upload_cron()
    
    print("\n✅ Setup completed successfully!")
    print("\nNext steps:")
    print("1. Check your GitHub account for the new repository")
    print("2. The daily upload will run automatically at 9 AM")
    print("3. You can manually run the daily upload script:")
    print(f"   cd {KNOWLEDGE_BASE_DIR} && python3 daily_upload.py")

if __name__ == "__main__":
    main()