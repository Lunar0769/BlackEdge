# 🔥 BlackEdge - AI Market Intelligence

A self-correcting AI market analysis system powered by Google Gemini.

## Features

- ✅ Multi-agent analysis (Researcher → Analyst → Trader → Critic)
- ✅ Self-correcting architecture with feedback loop
- ✅ Real-time streaming web interface
- ✅ Memory system that learns from mistakes
- ✅ Rate limiting: 1 analysis per 30 minutes

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Key
Create a `.env` file:
```
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 3. Run Web Interface
```bash
python app.py
```

Open http://localhost:5000 in your browser.

### Or Run CLI
```bash
python main.py
```

## How It Works

```
Query → RAG → Researcher → Analyst → Trader → Critic → Feedback Loop
```

### Agents
1. **Researcher**: Market context and trend analysis
2. **Analyst**: Risk assessment and outlook
3. **Trader**: BUY/SELL/HOLD decisions
4. **Critic**: Quality evaluation (1-10 score)

### Self-Correction
- Critic scores each decision
- Low scores (< 7) trigger retry with enhanced context
- Past mistakes stored in memory
- Future analyses learn from errors

## Tech Stack

- **LLM**: Google Gemini 2.5 Flash
- **Embeddings**: HuggingFace (all-MiniLM-L6-v2)
- **Vector Store**: FAISS
- **Framework**: LangChain + Flask
- **Frontend**: Vanilla JS with SSE streaming

## File Structure

```
blackedge/
├── app.py                   # Flask web server
├── main.py                  # CLI interface
├── rate_limiter.py          # 30-min cooldown
├── config.py                # Configuration
├── agents/                  # AI agents
│   ├── researcher.py
│   ├── analyst.py
│   ├── trader.py
│   └── critic.py
├── memory/                  # Learning system
│   ├── feedback_manager.py
│   └── error_log.json
├── rag/                     # Document retrieval
│   ├── vector_store.py
│   ├── retriever.py
│   └── market_history.json
├── workflow/                # Orchestration
│   └── graph.py
├── templates/               # HTML templates
│   └── index.html
└── static/                  # Frontend assets
    ├── app.js
    └── style.css
```

## Example Queries

- "Should I buy NVDA given AI boom and high valuation?"
- "Fed cuts rates while inflation remains high — buy or sell equities?"
- "Banking crisis erupts while tech rallies — what is the play?"

## License

MIT

---

**BlackEdge** - AI Market Intelligence System
