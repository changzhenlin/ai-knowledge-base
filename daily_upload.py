#!/usr/bin/env python3
"""
Daily AI Knowledge Base Updater - Customized for Java Agent Interviews & AI News
Generates and uploads 2 Java agent development interview files + 1 AI news file daily
"""

import os
import random
import subprocess
from datetime import datetime, timedelta

WORKSPACE_DIR = "/Users/tyler/.openclaw/workspace"
KNOWLEDGE_BASE_DIR = f"{WORKSPACE_DIR}/ai-knowledge-base"
EXCLUDED_FILES = {"README.md", "SETUP.md", "TODO.md", "LICENSE"}

# Import content generator
import sys
sys.path.append(KNOWLEDGE_BASE_DIR)
try:
    from content_generator import ContentGenerator
except ImportError:
    print("Warning: ContentGenerator not found, will only process existing files")
    ContentGenerator = None

def find_java_agent_interview_files():
    """Find Java agent development interview question files."""
    java_files = []
    for root, dirs, files in os.walk(WORKSPACE_DIR):
        # Skip hidden directories and ai-knowledge-base itself
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'ai-knowledge-base']
        
        for file in files:
            if file.endswith('.md') and file not in EXCLUDED_FILES:
                full_path = os.path.join(root, file)
                # Look for files containing Java agent interview content
                if os.path.isfile(full_path):
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read().lower()
                        if any(keyword in content for keyword in ['java', 'agent', 'interview', '面试', '开发']):
                            if 'interview' in content or '面试' in content:
                                java_files.append(full_path)
    return java_files

def find_ai_news_files():
    """Find AI news files with hot topics."""
    news_files = []
    for root, dirs, files in os.walk(WORKSPACE_DIR):
        # Skip hidden directories and ai-knowledge-base itself
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'ai-knowledge-base']
        
        for file in files:
            if file.endswith('.md') and file not in EXCLUDED_FILES:
                full_path = os.path.join(root, file)
                # Look for files containing AI news content
                if os.path.isfile(full_path):
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read().lower()
                        if any(keyword in content for keyword in ['ai news', 'tech news', '热门', 'hot', 'news', '新闻']):
                            # Exclude files that are just configuration or setup
                            if not any(exclude in file.lower() for exclude in ['setup', 'config', 'cron', 'script']):
                                news_files.append(full_path)
    return news_files

def select_files_to_upload(java_files, news_files, java_count=2, news_count=1):
    """Select specific counts of Java interview and AI news files."""
    selected = []
    
    # Select Java agent interview files
    if len(java_files) <= java_count:
        selected.extend(java_files)
    else:
        selected.extend(random.sample(java_files, java_count))
    
    # Select AI news files
    if len(news_files) <= news_count:
        selected.extend(news_files)
    else:
        selected.extend(random.sample(news_files, news_count))
    
    return selected

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
    
    # Read file content for better categorization
    if os.path.isfile(filepath):
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read().lower()
    else:
        content = ""
    
    # Category mappings - prioritize Java agent interviews
    if any(keyword in content for keyword in ['java', 'agent', 'interview', '面试']) or \
       any(keyword in filename_lower for keyword in ['java', 'agent', 'interview', '面试']):
        return 'interview-preparation'
    elif any(keyword in filename_lower for keyword in ['rag', 'llm', 'nlp', 'language', 'transformer']):
        return 'nlp'
    elif any(keyword in filename_lower for keyword in ['vision', 'image', 'computer', 'cv']):
        return 'computer-vision'
    elif any(keyword in filename_lower for keyword in ['news', 'hot', '热门', 'ai news', 'tech news']):
        return 'ai-news'
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
        commit_msg = f"Daily update: {date_str} - Java Agent Interviews & AI News"
        
        # Commit
        subprocess.run(f"git commit -m '{commit_msg}'", shell=True)
        
        # Push
        subprocess.run("git push origin main", shell=True)
        
        print("✓ Successfully pushed changes to GitHub")
        return True
    else:
        print("No changes to commit")
        return False

def generate_daily_content():
    """Generate today's AI news and Java Agent interview content."""
    if ContentGenerator is None:
        print("ContentGenerator not available, skipping content generation")
        return []
    
    print("Generating daily content...")
    generator = ContentGenerator()
    
    # Generate yesterday's AI news (for daily summary)
    yesterday = datetime.now() - timedelta(days=1)
    ai_news = generator.generate_ai_news(yesterday)
    
    # Generate 2-3 Java Agent interview questions
    java_questions = []
    topics = [
        "Java Agent Instrumentation", 
        "Bytecode Manipulation",
        "Class Loading in Java Agents"
    ]
    
    # Select 2-3 random topics
    selected_topics = random.sample(topics, min(3, len(topics)))
    
    for topic in selected_topics:
        java_questions.append(generator.generate_java_agent_interview_question(topic))
    
    # Save all generated content
    all_content = [ai_news] + java_questions
    generated_files = generator.save_generated_content(all_content)
    
    print(f"Generated {len(generated_files)} new files")
    return generated_files


def main():
    """Main function to run daily update."""
    print(f"Starting AI Knowledge Base update: {datetime.now()}")
    print("Focus: 2-3 Java Agent Interview files + 1 AI News file")
    
    # Change to workspace directory
    os.chdir(WORKSPACE_DIR)
    
    # Generate today's content first
    generated_files = generate_daily_content()
    
    # Find specific file types (including newly generated ones)
    java_files = find_java_agent_interview_files()
    news_files = find_ai_news_files()
    
    print(f"Found {len(java_files)} Java agent interview files")
    print(f"Found {len(news_files)} AI news files")
    
    if not java_files and not news_files:
        print("No matching files to upload")
        return
    
    # Select files to upload (2 Java + 1 AI news)
    files_to_upload = select_files_to_upload(java_files, news_files, java_count=2, news_count=1)
    
    print(f"Selected {len(files_to_upload)} files for upload:")
    for file in files_to_upload:
        file_type = "Java Agent Interview" if file in java_files else "AI News"
        print(f"  - [{file_type}] {os.path.basename(file)}")
    
    # Copy files to knowledge base
    copied_files = copy_to_knowledge_base(files_to_upload)
    print(f"Copied {len(copied_files)} files to knowledge base")
    
    # Commit and push
    success = git_commit_and_push()
    
    if success:
        print("✓ Daily update completed successfully")
        print("📊 Summary: 2 Java Agent Interviews + 1 AI News uploaded")
    else:
        print("Daily update completed (no changes)")

if __name__ == "__main__":
    main()