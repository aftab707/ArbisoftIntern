import os
import json
import sys
from groq import Groq
from dotenv import load_dotenv

# Add paths for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from orchestrator.workers.task_worker import run_task_worker
from orchestrator.workers.search_worker import run_search_worker
from tracing import log_tool_call

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY")) if os.getenv("GROQ_API_KEY") else None

@log_tool_call(agent_name="Supervisor")
def route_request(user_prompt: str) -> str:
    """Uses LLM to decide which worker to call and with what arguments."""
    if not groq_client:
        return "Error: GROQ_API_KEY not set."
        
    system_prompt = """You are a Supervisor Agent. Your job is to route the user's request to one of two workers:
1. SearchWorker: For finding information on the internet.
2. TaskWorker: For listing tasks or creating tasks in the backend system.

You must output a JSON object with the following structure:
{
    "worker": "SearchWorker" | "TaskWorker",
    "instruction": "action_name_or_query",
    "kwargs": { ... any arguments needed ... }
}

For SearchWorker, "instruction" should be the search query, and kwargs should be empty.
For TaskWorker, "instruction" should be either "list_tasks" or "create_task". 
If "create_task", kwargs should include "title", and optionally "description" and "status".
"""
    
    try:
        response = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="qwen/qwen3.8-27b",
            response_format={"type": "json_object"},
            temperature=0
        )
        
        decision_str = response.choices[0].message.content
        print(f"Raw model response: {decision_str}")
        
        # Extract JSON if it's wrapped in markdown code blocks
        import re
        json_match = re.search(r'```(?:json)?(.*?)```', decision_str, re.DOTALL)
        if json_match:
            decision_str = json_match.group(1).strip()
            
        decision = json.loads(decision_str)
        print(f"[Supervisor] Decision: {decision}")
        
        worker = decision.get("worker")
        instruction = decision.get("instruction")
        kwargs = decision.get("kwargs", {})
        
        if worker == "SearchWorker":
            return run_search_worker(instruction)
        elif worker == "TaskWorker":
            return run_task_worker(instruction, **kwargs)
        else:
            return f"Unknown worker selected: {worker}"
            
    except Exception as e:
        return f"Supervisor encountered an error: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    else:
        prompt = "Create a task to finish week 5 assignment"
    
    print(f"User Request: {prompt}")
    result = route_request(prompt)
    print("\n--- Final Result ---")
    print(result)
