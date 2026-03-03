# 🚀 BlackEdge Deployment Guide

## ✅ Successfully Deployed to GitHub

Repository: https://github.com/Lunar0769/BlackEdge

## What Was Done

### 1. Rebranded to BlackEdge
- Changed all references from "Market Agent" to "BlackEdge"
- Updated title: "BlackEdge - AI Market Intelligence"
- Updated subtitle: "AI Market Intelligence · Gemini Powered"

### 2. UI Improvements
- ✅ Removed critic score card section below agent pipeline
- ✅ Reduced market query textarea from 4 rows to 2 rows
- ✅ Cleaner interface without scroll bar
- ✅ All content fits perfectly on screen

### 3. Cleaned Up Files
- ✅ Removed unnecessary documentation (DEMO_INFO.md)
- ✅ Removed get-shit-done folder
- ✅ Created proper .gitignore
- ✅ Kept only essential files

### 4. Pushed to GitHub
- ✅ Initialized git repository
- ✅ Added all files
- ✅ Committed with message: "Initial commit: BlackEdge AI Market Intelligence System"
- ✅ Pushed to https://github.com/Lunar0769/BlackEdge.git

## Final File Structure

```
BlackEdge/
├── .gitignore
├── README.md
├── QUICKSTART.md
├── DEPLOYMENT.md
├── requirements.txt
├── config.py
├── main.py                  # CLI interface
├── app.py                   # Web server
├── rate_limiter.py          # 30-min cooldown
├── agents/
│   ├── researcher.py
│   ├── analyst.py
│   ├── trader.py
│   └── critic.py
├── memory/
│   ├── feedback_manager.py
│   └── __init__.py
├── rag/
│   ├── vector_store.py
│   ├── retriever.py
│   ├── market_history.json
│   └── __init__.py
├── workflow/
│   ├── graph.py
│   └── __init__.py
├── templates/
│   └── index.html
└── static/
    ├── app.js
    └── style.css
```

## How to Use

### Clone Repository
```bash
git clone https://github.com/Lunar0769/BlackEdge.git
cd BlackEdge
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Configure
Create `.env` file:
```
GOOGLE_API_KEY=your_gemini_api_key
```

### Run Web Interface
```bash
python app.py
```
Open http://localhost:5000

### Or Run CLI
```bash
python main.py
```

## Features

- 🔥 Real-time streaming analysis
- 🤖 Multi-agent pipeline (RAG → Researcher → Analyst → Trader → Critic)
- 🧠 Memory system that learns from mistakes
- 📊 Interactive web interface
- ⏱️ Rate limiting (1 analysis per 30 minutes)
- 🎯 Self-correcting architecture

## Tech Stack

- Google Gemini 2.5 Flash
- LangChain
- Flask + SSE streaming
- FAISS vector store
- HuggingFace embeddings

---

**BlackEdge** - AI Market Intelligence System
Repository: https://github.com/Lunar0769/BlackEdge
