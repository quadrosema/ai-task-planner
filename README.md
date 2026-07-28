# AI Task Planner

An AI-powered task planner built across two phases: LangChain chains (Day 1), then Agents + LangGraph + a Flask frontend (Day 2). It summarizes, classifies, and prioritizes tasks/text using OpenAI's `gpt-4o-mini`.

## Project structure

```
ai-task-planner/
├── day1_chains/              # Phase 1: LangChain chains
└── day2_agents_langgraph/    # Phase 2: Agents, LangGraph, Flask
```

---

## Day 1 — LangChain Chains

**Location:** `day1_chains/`

Builds a summarizer chain and a sequential chain (summarize → count words → classify) using `LLMChain`.

### Structure
```
day1_chains/
├── config.py                  # model name + API key loading
├── word_count.py               # plain Python word counter (not an LLM call)
├── main.py                     # orchestrates the sequential pipeline
├── requirements.txt
└── chains/
    ├── summarize_chain.py       # LLMChain: summarizes input text
    └── classify_chain.py        # LLMChain: classifies into a fixed label set
```

### Key design decisions
- **`LLMChain` is used deliberately**, even though it's deprecated and removed in LangChain 1.x. `requirements.txt` pins `langchain==0.3.7` / `langchain-openai==0.2.6` / `langchain-community==0.3.7`, the last line where `LLMChain` still works, per instructor requirement.
- **Word counting is plain Python** (`len(text.split())`), not an LLM call — LLMs are unreliable at exact counting, so this task is pulled out of chain-land entirely.
- **Classification uses a fixed label set** (Education, Business, Health, Technology, Personal/Other) rather than open-ended output, so results are predictable and testable.

### Setup & run
```bash
cd day1_chains
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY=your-key-here
python main.py
```

Runs the pipeline against sample business/health inputs and prints: original text, summary, summary word count, and classified topic for each.

---

## Day 2 — Agents, LangGraph & Flask

**Location:** `day2_agents_langgraph/`

Upgrades the planner with two standalone file-processing Agents, a LangGraph workflow that runs the full task-planning pipeline, and a Flask frontend to display results.

### Structure
```
day2_agents_langgraph/
├── config.py
├── requirements.txt
├── sample_files/
│   └── project_notes.txt        # sample file for the two agents to process
├── agents/
│   ├── file_summarizer_agent.py  # Agent: summarizes a text file
│   └── word_count_agent.py       # Agent: counts a specific word in a file
├── graph/
│   ├── state.py                  # shared state (TypedDict) passed between nodes
│   ├── nodes_summarize.py        # Node 1: summarize the task input
│   ├── nodes_classify.py         # Node 2: classify into Work / Study / Personal
│   ├── nodes_prioritize.py       # Node 3: the real Agent — reasons about urgency/importance
│   ├── nodes_plan.py             # Node 4: generates the Smart Plan
│   └── planner_graph.py          # wires all 4 nodes into the compiled graph
├── templates/
│   └── index.html                # minimal form + results page
└── app.py                        # Flask app (single route)
```

### Key design decisions
- **Both file-processing agents are built as literal LangChain/LangGraph `Agent` objects** (via `create_react_agent` + a `@tool`-decorated function), even though word-counting doesn't require reasoning — per instructor requirement to use real Agents for both tasks.
- **The prioritize node is the one genuine agent inside the graph.** Unlike summarize/classify/plan (fixed-order LCEL chains), deciding task priority benefits from actual reasoning, so it's given a `get_today_date` tool and reasons about urgency relative to any deadline mentioned in the task.
- **Modern LangChain/LCEL is used throughout** (not `LLMChain`), since this phase's brief doesn't require `LLMChain` and LangGraph itself needs a newer `langchain-core` than the version Day 1 is pinned to — hence the two phases have separate `requirements.txt` files and separate virtual environments.
- **The LangGraph workflow is linear**, not branching: `summarize → classify → prioritize → plan`, since the brief doesn't call for conditional routing.
- **Flask is intentionally minimal** — one route, one page, no styling or auth — since the Cybersecurity team owns deployment hardening and API protection testing per the brief.

### Setup & run
```bash
cd day2_agents_langgraph
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY=your-key-here
```

**Test the two agents directly:**
```bash
cd src
python3 -c "from agents.file_summarizer_agent import summarize_file; print(summarize_file('sample_files/project_notes.txt'))"
python3 -c "from agents.word_count_agent import count_word; print(count_word('sample_files/project_notes.txt', 'onboarding'))"
```

**Test the full graph directly:**
```bash
python3 -c "from graph.planner_graph import run_planner; print(run_planner('Finish the quarterly report by Friday'))"
```

**Run the Flask app:**
```bash
python3 app.py
```
Open `http://127.0.0.1:5000`, enter a task, and view the Original Task Input, Subtasks (Summary), Classification, Task Priority, and Smart Plan.

---

## Deployment

Per the project brief, this repository is handed off to the Cybersecurity team for deployment and API protection testing — no production hardening (auth, HTTPS, rate limiting) is included here by design.
