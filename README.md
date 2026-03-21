# AI Development Knowledge Base 🤖

A curated collection of markdown documents covering various aspects of AI development, including machine learning, deep learning, NLP, computer vision, LLMs, and more.

## 📁 Repository Structure

```
ai-knowledge-base/
├── interview-preparation/
│   ├── rag-pitfalls-interview.md      # RAG development interview cases
│   └── java-lock-interview.md         # Java concurrency for AI systems
├── machine-learning/
├── deep-learning/
├── nlp/
├── computer-vision/
├── llms/
├── ai-ethics/
└── tools/
```

## 🚀 Getting Started

### Initial Setup Required

1. **Create GitHub Repository:**
   - Go to GitHub.com → New repository
   - Name: `ai-knowledge-base`
   - Description: `A curated collection of AI development knowledge`
   - Click "Create repository"

2. **Connect Local Repository:**
   ```bash
   cd /Users/tyler/.openclaw/workspace/ai-knowledge-base
   git remote add origin https://github.com/YOUR_USERNAME/ai-knowledge-base.git
   git push -u origin main
   ```

3. **Configure Daily Updates:** See [SETUP.md](SETUP.md) for automation details.

## 📚 Current Content

### Interview Preparation
- **RAG Development Interview Cases** - Common pitfalls and solutions in Retrieval-Augmented Generation
- **Java Concurrency for AI** - Thread safety and performance in AI applications

## 🎯 Daily Updates

This repository is automatically updated daily with 1-3 new markdown documents covering:
- AI research papers and implementations
- Interview preparation materials
- Technical deep-dives
- Best practices and tutorials

## 📝 How to Contribute

Want to add your own AI knowledge?

1. Save any `.md` file to `/Users/tyler/.openclaw/workspace`
2. The daily automation script will:
   - Find your file
   - Categorize it based on content
   - Upload it to the appropriate directory
   - Commit and push to GitHub

**Example:** Save `transformer-tutorial.md` → Automatically categorized to `nlp/`

## 🛠️ Automation

The `daily_upload.py` script handles:
- **Smart categorization** based on filename and content
- **Random selection** of 1-3 files per day
- **Automatic commits** with descriptive messages
- **GitHub synchronization**

### Categories

- **interview-preparation/** - Interview questions and preparation
- **nlp/** - Natural language processing, RAG, LLMs
- **machine-learning/** - ML algorithms and fundamentals
- **deep-learning/** - Neural networks and frameworks
- **computer-vision/** - Image processing and vision AI
- **ai-ethics/** - Responsible AI and ethics
- **tools/** - Development tools and utilities

## 📊 Progress Tracking

Check the commit history on GitHub to see daily updates and new additions to your AI knowledge base.

---

**Made with ❤️ by OpenClaw AI Assistant**