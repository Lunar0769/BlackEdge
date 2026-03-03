# 🚀 Quick Start - BlackEdge

## Installation (5 minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Get Gemini API Key
1. Go to https://makersuite.google.com/app/apikey
2. Create a new API key
3. Copy the key

### Step 3: Configure
Create `.env` file:
```
GOOGLE_API_KEY=your_api_key_here
```

### Step 4: Run
```bash
# Web interface (recommended)
python app.py

# Or CLI
python main.py
```

## Web Interface

Open http://localhost:5000

Features:
- Real-time streaming analysis
- Interactive agent pipeline visualization
- Memory panel showing past mistakes
- Tabbed results view

## CLI Interface

```bash
python main.py
```

Enter your market question and get:
1. Research summary
2. Risk analysis
3. Investment decision
4. Critic evaluation

## Example Questions

### Multi-Factor Analysis
```
The Federal Reserve cuts interest rates unexpectedly while 
inflation remains above target. Tech earnings are mixed, and 
oil prices spike. How should a diversified investor rebalance?
```

### Contradictory Signals
```
Nvidia reports record revenue growth, but insider selling 
increases sharply and valuation multiples are at historic 
highs. Is this a buy, hold, or sell?
```

### Shock Scenario
```
A sudden banking crisis hits regional banks, while large 
tech stocks rally. How should capital be repositioned?
```

## Troubleshooting

### "API key not found"
Check `.env` file exists with:
```
GOOGLE_API_KEY=your_key
```

### "Rate limit reached"
Wait 30 minutes between analyses

### Import errors
Run: `pip install -r requirements.txt`

---

**Ready?** Run `python app.py` and open http://localhost:5000 🔥
