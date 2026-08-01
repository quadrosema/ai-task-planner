# AI Task Planner

An AI-powered task planner built across two phases: LangChain chains (Day 1), then Agents + LangGraph + a Flask frontend (Day 2), plus four Additional Engineering Challenges extending Day 2 with conversation memory, tool-calling, RAG, and human-in-the-loop review. Uses OpenAI's `gpt-4o-mini`.

## Project structure

```
ai-task-planner/
├── day1_chains/              # Phase 1: LangChain chains
└── day2_agents_langgraph/    # Phase 2: Agents, LangGraph, Flask + Additional Engineering Challenges
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
│   ├── nodes_summarize.py        # Node 1: breaks the task into concrete Subtasks
│   ├── nodes_classify.py         # Node 2: classifies the subtasks into Work / Study / Personal
│   ├── nodes_prioritize.py       # Node 3: the real Agent — reasons about urgency/importance
│   ├── nodes_plan.py             # Node 4: generates the Smart Plan
│   └── planner_graph.py          # wires all 4 nodes into the compiled graph
├── memory/
│   ├── persistent_memory.py       # JSON file storage - memory that survives across separate runs
│   ├── memory_chain.py            # conversation memory using LangChain's Memory module
│   ├── session1.py                # demo: first session, mentions a task/deadline
│   └── session2.py                # demo: second (separate) session, references it back
├── tools_agent/
│   ├── tools.py                   # 5 @tool-decorated functions: Calculator, Date/Time, Weather, Wikipedia, Google Search (Tavily)
│   ├── agent.py                   # create_react_agent bound to all 5 tools, picks which to use automatically
│   └── demo.py                    # demo matching the brief's "days until my exam" example
├── rag/
│   ├── document_store.py          # load PDF/DOCX/txt, chunk, embed, store in a vector store
│   ├── qa_chain.py                # retrieve relevant chunks, answer using ONLY that context
│   ├── demo.py                    # demo matching the brief's "Summarize Chapter 2" example
│   ├── app.py                     # separate minimal Flask app (port 5001): upload a doc, ask questions
│   ├── templates/rag_index.html
│   └── sample_docs/               # sample lecture notes (txt/pdf/docx) for testing
├── templates/
│   └── index.html                # form + review loop (proposed plan / approve / feedback) + final result
└── app.py                        # Flask app (single route) - now includes the human-in-the-loop review flow
```

### Key design decisions
- **Both file-processing agents are built as literal LangChain/LangGraph `Agent` objects** (via `create_react_agent` + a `@tool`-decorated function), even though word-counting doesn't require reasoning — per instructor requirement to use real Agents for both tasks.
- **The prioritize node is the one genuine agent inside the graph.** Unlike summarize/classify/plan (fixed-order LCEL chains), deciding task priority benefits from actual reasoning, so it's given a `get_today_date` tool and reasons about urgency relative to any deadline mentioned in the task.
- **Modern LangChain/LCEL is used throughout** (not `LLMChain`), since this phase's brief doesn't require `LLMChain` and LangGraph itself needs a newer `langchain-core` than the version Day 1 is pinned to — hence the two phases have separate `requirements.txt` files and separate virtual environments.
- **The LangGraph workflow is linear**, not branching: `subtasks → classify → prioritize → plan`, since the brief doesn't call for conditional routing. The first node generates a real breakdown into concrete subtasks (not just a one-sentence summary), matching the brief's required "Subtasks generated by the Graph" field.
- **Conversation memory** (Additional Engineering Challenge, Task 1) uses LangChain's current Memory module (`InMemoryChatMessageHistory` + `RunnableWithMessageHistory`) rather than the deprecated `ConversationBufferMemory`, since the deprecated class's dependency requirements directly conflict with LangGraph's — confirmed by testing, downgrading to get `ConversationBufferMemory` breaks `StateGraph` and `create_react_agent` entirely. Short-term memory lives in RAM for the session; persistent memory is a JSON file that's loaded at the start of each session and updated after every turn, so the AI can reference earlier conversations even across separate runs.
- **AI Tool Calling** (Task 2) uses `create_react_agent` bound to all 5 tools (Calculator, Current Date/Time, Weather, Wikipedia Search, Google Search via Tavily), rather than the legacy `AgentExecutor` named in the brief — same removal/conflict reasoning as `ConversationBufferMemory`. The agent decides which tool(s) to call automatically based on the request; verified across all 5 tools individually, including a multi-tool case (date + calculator together for "days until my exam").
- **RAG** (Task 3) uses a manual retrieve → stuff-into-prompt → answer chain built with LCEL, rather than the legacy `RetrievalQA` class (also removed in current LangChain). Storage uses `InMemoryVectorStore` (ships with `langchain_core`, no extra install) rather than FAISS. The answer prompt explicitly instructs the model to use ONLY the retrieved context — verified by testing a question about a nonexistent "Chapter 5," which the model correctly refused to answer rather than hallucinating.
- **Human-in-the-Loop review** (Task 4) extends the existing planner rather than being a standalone feature: `app.py` now generates an initial subtask list, shows it with Approve/Feedback options, and only runs the rest of the pipeline (classify → prioritize → smart plan) once the user approves. Feedback is handled by `graph/refine_plan.py`, which regenerates the subtask list based on natural-language feedback (e.g. "move X to first priority") while preserving everything else in the plan.
- **Flask is intentionally minimal** — one route, one page, no styling or auth — since the Cybersecurity team owns deployment hardening and API protection testing per the brief.

### Setup & run
```bash
cd day2_agents_langgraph
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY=your-key-here
```
For the Weather and Google Search tools (Task 2), also add `OPENWEATHER_API_KEY` (from openweathermap.org) and `TAVILY_API_KEY` (from tavily.com) to a `.env` file in `src/` — both have free tiers. Everything else needs only `OPENAI_API_KEY`.

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

**Run the planner Flask app** (now includes the human-in-the-loop review flow):
```bash
python3 app.py
```
Open `http://127.0.0.1:5000`, enter a task, and you'll see a **Proposed Plan** with **Approve** and **feedback** options. Send feedback (e.g. "move X to first priority") to have the plan regenerated, or click **Approve** to run the rest of the pipeline (Classification of Subtasks, Task Priority, Smart Plan).

**Test conversation memory** (run as two separate processes to prove persistence across runs):
```bash
python3 -m memory.session1
python3 -m memory.session2
```
The second run should reference what was mentioned in the first, even though it's a completely separate process — proof the JSON-backed persistent memory actually works, not just in-RAM short-term memory within one script.

**Test the tool-calling agent** (needs `OPENWEATHER_API_KEY` and `TAVILY_API_KEY` in `.env` for the Weather and Google Search tools — Calculator, Date/Time, and Wikipedia need no extra keys):
```bash
python3 -m tools_agent.demo
```
Matches the brief's exact example: "How many days are left until my exam on August 15?" — the agent retrieves today's date and calculates the answer.

**Test RAG directly:**
```bash
python3 -m rag.demo
```
Builds a vector store from the sample lecture notes and answers "Summarize Chapter 2," a factual question, and a deliberately out-of-document question (to confirm it correctly says it doesn't know rather than hallucinating).

**Run the RAG upload UI** (a separate Flask app, port 5001):
```bash
python3 -m rag.app
```
Open `http://127.0.0.1:5001`, upload a PDF/DOCX/txt file, and ask questions about it.

---

## Deployment

Per the project brief, this repository is handed off to the Cybersecurity team for deployment and API protection testing — no production hardening (auth, HTTPS, rate limiting) is included here by design.
