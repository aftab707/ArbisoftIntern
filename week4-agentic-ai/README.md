# Week 4 — Agentic AI: Skills, Hooks, Memory & Plugins

A small standalone research agent built for Phase 2 / Week 4 of the Arbisoft
Internship Program. It is self-contained — it does not import anything from
`src/` or `backend/` in the rest of the repo.

## What it demonstrates

| Week 4 requirement | Where |
| --- | --- |
| Web-search skill | `skills/web_search.py` (Tavily Search API) |
| Memory (recalls facts from earlier in the session) | `memory.py` (in-context history + key-value fact store) |
| Hook that logs every tool call with timestamps | `hooks.py` -> `tool_calls.log` |
| File-read plugin (.txt / .pdf) | `skills/file_reader.py` |
| Multi-step / multi-hop reasoning | `agent.py` (planner -> executor -> memory loop, ReAct-style) |

## Setup

```bash
cd week4-agentic-ai
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

Then fill in `.env` (already gitignored — the repo's root `.gitignore` ignores
all `.env*` files) with your own keys:

```
GROQ_API_KEY=...
TAVILY_API_KEY=...
```

### Getting a free Groq API key

1. Go to https://console.groq.com and sign in (Google/GitHub login works).
2. Left sidebar -> **API Keys** -> **Create API Key**.
3. Name it (e.g. `week4-agent`), copy the key immediately (shown once).
4. Paste it into `.env` as `GROQ_API_KEY`.

Groq's free tier has generous rate limits and is OpenAI-compatible, which is
what `agent.py` uses for function/tool calling. Default model is
`llama-3.3-70b-versatile` (override with a `GROQ_MODEL` env var).

### Getting a free Tavily API key

1. Go to https://app.tavily.com and sign up (Google/GitHub login works).
2. The default **Researcher** plan is free — 1,000 search credits/month, no
   card required.
3. On the **Overview** page, find the **API Keys** section, click **+**, name
   it, copy the key.
4. Paste it into `.env` as `TAVILY_API_KEY`.

Tavily is purpose-built for AI agents (results come back pre-cleaned for LLM
consumption), which is why it's used here instead of a general search API.
If `TAVILY_API_KEY` is missing, `web_search` returns a clear error string
instead of crashing, so the rest of the agent still works.

## Run

```bash
python agent.py
```

Then chat with it, e.g.:

```
You: search the web for the current FastAPI version and remember it as fastapi_version
You: what did you save as fastapi_version?
You: read the file demo.txt and summarize it
```

Every tool call (name, args, duration, status) is appended as a JSON line to
`tool_calls.log` in this folder via the `log_tool_call` hook in `hooks.py`.

## Notes

- Memory here is intentionally simple: full conversation history (in-context)
  plus a `remember_fact` / `recall_fact` key-value store. A vector store
  (ChromaDB) is mentioned in the program topics as an alternative memory type
  but wasn't needed for this agent's scope.
- `tool_calls.log` is created on first run and is local/gitignored-by-pattern
  scope (safe to delete and regenerate).
