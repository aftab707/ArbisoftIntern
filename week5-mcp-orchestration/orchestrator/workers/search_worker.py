import os
from tavily import TavilyClient
from dotenv import load_dotenv
import sys
import os

# Add parent directory to path to import tracing
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from tracing import log_tool_call

load_dotenv()

# Initialize Tavily
api_key = os.getenv("TAVILY_API_KEY")
tavily_client = TavilyClient(api_key=api_key) if api_key else None

@log_tool_call(agent_name="SearchWorker")
def perform_web_search(query: str) -> str:
    """
    Search the web for information using Tavily API.
    """
    if not tavily_client:
        return "Error: TAVILY_API_KEY not configured."
    
    print(f"[SearchWorker] Searching web for: {query}")
    try:
        response = tavily_client.search(query, search_depth="basic")
        results = response.get("results", [])
        if not results:
            return "No results found."
        
        output = "Search Results:\n"
        for i, res in enumerate(results[:3], 1):
            output += f"{i}. {res.get('title')} - {res.get('url')}\n   {res.get('content')}\n"
        return output
    except Exception as e:
        return f"Web search failed: {str(e)}"

def run_search_worker(query: str) -> str:
    """Entry point for the search worker."""
    return perform_web_search(query)
