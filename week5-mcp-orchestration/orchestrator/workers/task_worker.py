import os
import sys
import asyncio
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.session import ClientSession

# Add parent directory to path to import tracing
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from tracing import log_tool_call

@log_tool_call(agent_name="TaskWorker")
def execute_mcp_action(action: str, **kwargs) -> str:
    """Synchronous wrapper to run MCP actions."""
    return asyncio.run(_async_execute_mcp_action(action, **kwargs))

async def _async_execute_mcp_action(action: str, **kwargs) -> str:
    server_script = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "mcp_server", "server.py")
    
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[server_script],
        env=os.environ.copy() # pass env variables like keys
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                if action == "list_tasks":
                    result = await session.read_resource("tasks://list")
                    return str(result)
                
                elif action == "create_task":
                    result = await session.call_tool("create_task", arguments=kwargs)
                    return str(result)
                
                else:
                    return f"Unknown action: {action}"
    except Exception as e:
        return f"MCP execution failed: {str(e)}"

def run_task_worker(instruction: str, **kwargs) -> str:
    """
    Entry point for the task worker.
    instruction should be either 'list_tasks' or 'create_task'
    kwargs holds arguments for create_task (title, description, status)
    """
    print(f"[TaskWorker] Executing {instruction} with args: {kwargs}")
    return execute_mcp_action(instruction, **kwargs)
