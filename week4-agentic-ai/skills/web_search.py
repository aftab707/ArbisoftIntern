"""Web-search skill backed by the Tavily Search API (built for AI agents)."""

import os

from tavily import TavilyClient


def clean_text(value) -> str:
    """Keep tool output safe for Windows terminals with legacy encodings."""
    return str(value or "").encode("ascii", errors="replace").decode("ascii")


def web_search(query: str, max_results: int = 5) -> str:
    """Search the web via Tavily and return a readable summary of top results."""
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        return "TAVILY_API_KEY is not set in .env — cannot perform web search."

    client = TavilyClient(api_key=api_key)
    try:
        response = client.search(
            query=query,
            max_results=max_results,
            search_depth="advanced",
            include_answer=True,
        )
    except Exception as exc:
        return f"Tavily search failed: {exc}"

    results = response.get("results", [])
    if not results:
        return f"No web results found for '{query}'."

    lines = [f"Top web results for '{query}':"]
    answer = response.get("answer")
    if answer:
        lines.append(f"Direct answer: {clean_text(answer)}")
    for i, result in enumerate(results[:max_results], start=1):
        title = clean_text(result.get("title", ""))
        url = clean_text(result.get("url", ""))
        content = clean_text(result.get("content", ""))[:200]
        lines.append(f"{i}. {title} — {content} ({url})")

    return "\n".join(lines)
