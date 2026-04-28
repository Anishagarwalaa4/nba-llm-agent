# 🏀 NBA Stats Agentic Analysis System

> Ask any question about 30 years of NBA data in plain English. Powered by the Claude API and Pandas.

An agentic AI system that lets users ask natural language questions about NBA history. Claude autonomously decides which Python tools to call, chains them across multiple reasoning turns, and returns specific, data-backed answers — all without any hardcoded query logic.

**Live demo:** [anish-nba-agent.streamlit.app](https://anish-nba-agent.streamlit.app) *(coming soon)*

---

## ✨ What it does

Type a question like:

> *"Who were the top 5 scorers in the 2023-24 season, and how did LeBron's career evolve over 20 years?"*

Behind the scenes, Claude:
1. Recognizes it needs to call `get_top_players(stat="pts", n=5, season="2023-24")`
2. Then decides to call `player_career(name="LeBron James")`
3. Synthesizes both results into a written analysis with real numbers

No hardcoded if/else logic — Claude picks the tools and the order on its own.

---

## 🧠 How it works

```
User question
     ↓
Claude (with tool definitions)
     ↓
Decides which tool(s) to call
     ↓
Python functions run on Pandas DataFrame
     ↓
Results sent back to Claude
     ↓
Claude either calls more tools or writes final answer
```

This is the standard "agentic loop" pattern used in every modern AI agent (Cursor, Perplexity, Claude Code).

---

## 🛠️ Tech stack

- **Python 3.13**
- **Claude Sonnet 4.5** via the official `anthropic` SDK
- **Pandas** for data manipulation
- **JSON Schema** for tool input definitions
- **Kaggle NBA Players Dataset** — 30 years of historical stats (1996–2024)

---

## 📂 Project structure

```
nba-llm-agent/
├── nba_agent.py        # Main agent loop + tool registry
├── all_seasons.csv     # NBA stats dataset (from Kaggle)
├── requirements.txt    # Python dependencies
├── .env.example        # Template for API key (real .env is gitignored)
├── .gitignore
└── README.md
```

---

## 🚀 Getting started

### Prerequisites
- Python 3.10 or newer
- An [Anthropic API key](https://console.anthropic.com)

### Setup

```bash
# Clone the repo
git clone https://github.com/Anishagarwalaa4/nba-llm-agent.git
cd nba-llm-agent

# Install dependencies
pip install -r requirements.txt

# Add your API key
cp .env.example .env
# Then open .env and paste your real key
```

### Get the dataset
Download `all_seasons.csv` from [Kaggle: NBA Players Data](https://www.kaggle.com/datasets/justinas/nba-players-data) and place it in the project root.

### Run it

```bash
python nba_agent.py
```

---

## 🔧 Tool registry

Claude has access to four typed Python tools, each defined with a JSON schema:

| Tool | What it does |
|------|--------------|
| `get_top_players` | Returns top N players ranked by any stat, with optional season filter |
| `player_career` | Returns full career stat history for a specific player |
| `get_stat_summary` | Returns mean, min, max, std for any numeric column |
| `find_outliers` | Identifies players with statistically unusual performances |

Tools are registered with full input schemas, descriptions, and required-field validation.

---

## 🧩 Engineering highlights

- **Multi-turn agentic loop** — Claude can call tools repeatedly until it has enough information to answer.
- **Defensive error handling** — Invalid tool inputs (e.g., wrong column names) return helpful error messages instead of crashing, allowing Claude to self-correct on the next turn.
- **Structured context injection** — Pandas schemas are serialized into the system prompt so Claude knows exact column names upfront.
- **Modular design** — Tool registry is fully separated from the agent loop, making it easy to add new analytical capabilities.

---

## 💡 Sample questions to try

- "Compare Kobe Bryant and Kevin Durant as scorers — who was more dominant statistically?"
- "Which players had statistically freakish scoring seasons?"
- "Show me LeBron James's career arc — how did his game change?"
- "Do first-round draft picks score more than second-round picks on average?"
- "Who has the most unbalanced stat line — great at one thing but weak elsewhere?"

---

## 📚 What I learned building this

- How to design tool schemas that Claude can reliably interpret
- The agentic loop pattern: `while not done → call tool → feed result back → repeat`
- How to engineer prompts so the LLM picks correct tool arguments (column names, filters)
- Why graceful error handling matters more in agent systems than traditional code — the LLM uses errors as signal for self-correction

---

## 🔮 What's next

- [ ] Streamlit web UI for live demo
- [ ] Add chart rendering tools so Claude can return matplotlib visualizations
- [ ] Support for game-by-game data (currently season-aggregated)
- [ ] Streaming responses for faster perceived latency

---

## 👋 About

Built by **Anish Agarwal**, a 10th grade student in San Diego interested in sensor data pipelines and LLM-assisted research. Currently seeking summer research opportunities in environmental sensing, robotics, or applied AI.

📧 anishagarwalaa4@gmail.com
🔗 [github.com/Anishagarwalaa4](https://github.com/Anishagarwalaa4)
