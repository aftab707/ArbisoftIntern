"""Week 4 — a small research agent: planner -> executor -> memory loop (ReAct-style).

Run: python agent.py
Requires GROQ_API_KEY (and TAVILY_API_KEY for web search) in .env.
"""

import json
import os

from dotenv import load_dotenv
from groq import BadRequestError, Groq

from hooks import log_tool_call
from memory import AgentMemory
from skills.file_reader import read_file
from skills.web_search import web_search

MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")

SYSTEM_PROMPT = (
    "You are a research agent with three tools: web_search, read_file, and a "
    "small memory (remember_fact / recall_fact). Use web_search for questions "
    "about current or external information, use read_file when the user "
    "mentions a local .txt or .pdf file, and use remember_fact to save facts "
    "the user tells you or that you look up, so you can recall_fact them "
    "later in the same session instead of re-searching. Keep answers concise."
)

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the live web for current information via Tavily.",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string", "description": "The search query."}},
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the text content of a local .txt or .pdf file.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string", "description": "Path to the .txt or .pdf file."}},
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "remember_fact",
            "description": "Save a short fact under a key so it can be recalled later in this session.",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {"type": "string", "description": "Short label for the fact."},
                    "value": {"type": "string", "description": "The fact to remember."},
                },
                "required": ["key", "value"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "recall_fact",
            "description": "Recall a previously remembered fact by its key.",
            "parameters": {
                "type": "object",
                "properties": {"key": {"type": "string", "description": "The key used when the fact was saved."}},
                "required": ["key"],
            },
        },
    },
]


def build_tool_dispatch(memory: AgentMemory) -> dict:
    return {
        "web_search": log_tool_call(web_search),
        "read_file": log_tool_call(read_file),
        "remember_fact": log_tool_call(memory.remember_fact),
        "recall_fact": log_tool_call(memory.recall_fact),
    }


def asks_for_web_search(user_input: str) -> bool:
    """Catch obvious live-info prompts before the model tries malformed tool calls."""
    text = user_input.lower()
    search_words = ("search", "web", "current", "latest", "today", "version", "look up")
    live_entities = ( "prime minister", "president", "ceo", "mayor", "governor", "minister", "price", "weather",)
    question_starts = ("who is", "who's", "what is", "what's")
    return (
        any(word in text for word in search_words)
        or any(entity in text for entity in live_entities)
        or (text.startswith(question_starts) and any(entity in text for entity in live_entities))
    )


def answer_with_context(client: Groq, memory: AgentMemory, context: str) -> str:
    messages = memory.history + [
        {
            "role": "user",
            "content": (
                "Answer my previous request using this tool result. "
                "Keep it concise and mention uncertainty if the result is incomplete.\n\n"
                f"{context}"
            ),
        }
    ]
    response = client.chat.completions.create(model=MODEL, messages=messages)
    return response.choices[0].message.content or "(no answer returned)"


def run_agent():
    load_dotenv()
    if not os.environ.get("GROQ_API_KEY"):
        raise SystemExit("GROQ_API_KEY is not set. Add it to week4-agentic-ai/.env first.")
    if not os.environ.get("TAVILY_API_KEY"):
        print("Warning: TAVILY_API_KEY is not set — web_search will return an error until it is.")

    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    memory = AgentMemory()
    tool_dispatch = build_tool_dispatch(memory)

    memory.add_message("system", SYSTEM_PROMPT)

    print("Week 4 research agent ready (Groq). Type 'exit' to quit.\n")
    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit"}:
            break

        memory.add_message("user", user_input)

        if asks_for_web_search(user_input):
            result = tool_dispatch["web_search"](query=user_input)
            context = f"web_search result for {user_input!r}:\n{result}"
            memory.add_message("assistant", context)
            answer = answer_with_context(client, memory, context)
            memory.add_message("assistant", answer)
            print(f"Agent: {answer}\n")
            continue

        # Planner/executor loop: keep letting the model call tools until it
        # answers directly, so multi-hop questions (search -> remember ->
        # answer) resolve in one turn without the user re-prompting.
        while True:
            try:
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=memory.history,
                    tools=TOOLS,
                    tool_choice="auto",
                )
            except BadRequestError as exc:
                result = tool_dispatch["web_search"](query=user_input)
                context = f"web_search fallback after tool-call error:\n{result}"
                memory.add_message("assistant", context)
                answer = answer_with_context(client, memory, context)
                memory.add_message("assistant", answer)
                print(f"[fallback] Groq tool-call error handled: {exc.__class__.__name__}")
                print(f"Agent: {answer}\n")
                break
            choice = response.choices[0].message

            if not choice.tool_calls:
                memory.add_message("assistant", choice.content)
                print(f"Agent: {choice.content}\n")
                break

            memory.add_message(
                "assistant",
                choice.content,
                tool_calls=[tc.model_dump() for tc in choice.tool_calls],
            )

            for tool_call in choice.tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments or "{}")
                impl = tool_dispatch.get(name)
                result = impl(**args) if impl else f"Unknown tool: {name}"
                memory.add_message("tool", str(result), tool_call_id=tool_call.id, name=name)


if __name__ == "__main__":
    run_agent()
