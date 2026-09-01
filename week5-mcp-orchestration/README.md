# Week 5: MCP, Multi-Agent Orchestration & Tool Design

Self-contained module for week 5 demonstrating:
1. Custom MCP Server exposing backend resources and tools.
2. Multi-Agent Orchestration with a Supervisor routing to specific workers.
3. Tracing layer to log multi-agent tool calls.

## Setup
1. `python -m venv .venv`
2. `source .venv/Scripts/activate` (Windows)
3. `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and fill in credentials.

## Components
- **mcp_server/server.py**: Exposes the `tasks://list` resource and `create_task` tool via MCP stdio.
- **orchestrator/supervisor.py**: ReAct based supervisor that routes queries to either `task_worker` or `search_worker`.
- **orchestrator/workers/task_worker.py**: Worker capable of interacting with the MCP server.
- **orchestrator/workers/search_worker.py**: Worker capable of doing web searches.
- **tracing.py**: A decorator-based tracing mechanism logging the execution graph of tool calls.
