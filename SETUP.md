# AI Knowledge Base Setup Guide

This guide will help you create a GitHub repository for your AI development knowledge base and set up automatic daily updates.

## 📁 Repository Structure

Your AI knowledge base is already set up with the following structure:

```
ai-knowledge-base/
├── README.md
├── interview-preparation/
│   ├── rag-pitfalls-interview.md
│   └── java-lock-interview.md
├── machine-learning/
├── deep-learning/
├── nlp/
├── computer-vision/
├── llms/
├── ai-ethics/
├── tools/
├── SETUP.md (this file)
└── daily_upload.py (automation script)
```

## 🚀 Quick Start

### Step 1: Create GitHub Repository

Since the automated setup requires GitHub authentication, please create the repository manually:

1. **Go to GitHub.com** and log in to your account
2. **Click the "+" icon** in the top-right corner and select "New repository"
3. **Fill in the details:**
   - Repository name: `ai-knowledge-base`
   - Description: `A curated collection of AI development knowledge - automatically updated daily`
   - Visibility: Public (or Private if you prefer)
   - Do NOT initialize with README, .gitignore, or license
4. **Click "Create repository"**

### Step 2: Connect Local Repository

After creating the repository on GitHub:

```bash
# Add the remote repository (replace <your-username> with your GitHub username)
cd /Users/tyler/.openclaw/workspace/ai-knowledge-base
git remote add origin https://github.com/<your-username>/ai-knowledge-base.git

# Push the initial commit
git push -u origin main
```

### Step 3: Test the Setup

Verify everything is working:

```bash
# Check remote connection
git remote -v

# Check repository status
git status
```

## ⚙️ Daily Automation Setup

### The `daily_upload.py` Script

This script automatically:
- Finds new markdown files in your workspace
- Categorizes them based on content
- Commits and pushes them to GitHub

### Configure Cron Job

To run daily at 9 AM, set up a cron job:

```bash
# Open crontab
crontab -e

# Add this line (adjust paths if needed)
0 9 * * * cd /Users/tyler/.openclaw/workspace/ai-knowledge-base && python3 daily_upload.py >> /tmp/ai_knowledge_base_update.log 2>&1
```

### Manual Test Run

You can test the automation manually:

```bash
cd /Users/tyler/.openclaw/workspace/ai-knowledge-base
python3 daily_upload.py
```

## 📝 How It Works

### File Categorization

The script categorizes files based on filename and content:

- **interview-preparation/** - Interview questions and preparation materials
- **nlp/** - Natural language processing, RAG, LLMs
- **machine-learning/** - ML algorithms and concepts
- **deep-learning/** - Neural networks and deep learning
- **computer-vision/** - Image processing and vision tasks
- **ai-ethics/** - Ethics and responsible AI
- **tools/** - Development tools and frameworks

### Daily Update Process

1. **Scans workspace** for `.md` files (excluding system files)
2. **Randomly selects 1-3 files** to upload each day
3. **Categorizes and copies** files to appropriate directories
4. **Commits and pushes** changes to GitHub

## 🔧 Customization

### Modify Categories

Edit the `determine_category()` function in `daily_upload.py` to add or change categories:

```python
def determine_category(filename, filepath):
    filename_lower = filename.lower()
    
    if 'interview' in filename_lower:
        return 'interview-preparation'
    elif 'rag' in filename_lower or 'nlp' in filename_lower:
        return 'nlp'
    # ... add more conditions
```

### Change Update Frequency

To update more or less frequently, modify the cron schedule:

- **Every day at 9 AM:** `0 9 * * *`
- **Every Monday at 8 AM:** `0 8 * * 1`
- **Twice daily (9 AM and 6 PM):** `0 9,18 * * *`

### Adjust Number of Files

Change the number of files uploaded per day in `daily_upload.py`:

```python
files_to_upload = select_files_to_upload(available_files, count=3)  # Change 3 to your preference
```

## 📊 Monitoring

### Check Logs

View automation logs:

```bash
cat /tmp/ai_knowledge_base_update.log
```

### GitHub Activity

Monitor your repository's commit history on GitHub to see daily updates.

## 🛠️ Troubleshooting

### Permission Denied

If you get permission errors:

```bash
# Make script executable
chmod +x daily_upload.py
```

### Git Push Issues

If push fails, check remote URL:

```bash
git remote set-url origin https://github.com/<your-username>/ai-knowledge-base.git
```

### Python Dependencies

Ensure required Python packages are available:

```bash
python3 -c "import os, random, subprocess, datetime"
```

## 🎯 Next Steps

1. ✅ **Complete Step 1** - Create GitHub repository
2. ✅ **Complete Step 2** - Connect local repository
3. ✅ **Test manually** - Run `python3 daily_upload.py`
4. ✅ **Set up cron** - Configure daily automation
5. **Monitor** - Check logs and GitHub activity

## 📚 Adding Content

To add new AI knowledge files:

1. Save any `.md` file to your workspace (`/Users/tyler/.openclaw/workspace`)
2. The daily script will automatically find and upload it
3. Files are categorized based on filename and content

**Example:** Save a file named `transformer-architecture.md` and it will be uploaded to the `nlp/` category.

---

**Happy learning!** 🤖 Your AI knowledge base will grow automatically every day!