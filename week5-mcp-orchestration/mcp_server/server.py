import os
import requests
from dotenv import load_dotenv
from mcp.server.mcpserver import MCPServer
import json

# Load environment variables
load_dotenv()

BASE_URL = "http://127.0.0.1:8000"
USER_EMAIL = os.getenv("USER_EMAIL", "aftab@example.com")
USER_PASSWORD = os.getenv("USER_PASSWORD", "secret123")

# Create the MCP server
mcp = MCPServer("TaskBackend")

# Globals for token
AUTH_TOKEN = None

def get_headers():
    global AUTH_TOKEN
    if not AUTH_TOKEN:
        # Perform login
        login_data = {
            "email": USER_EMAIL,
            "password": USER_PASSWORD
        }
        response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
        if response.status_code == 200:
            AUTH_TOKEN = response.json().get("access_token")
        else:
            raise Exception(f"Failed to authenticate: {response.text}")
    
    return {"Authorization": f"Bearer {AUTH_TOKEN}"}

@mcp.resource("tasks://list")
def list_tasks() -> str:
    """Returns a list of tasks from the backend as read-only data."""
    headers = get_headers()
    response = requests.get(f"{BASE_URL}/api/v1/tasks/", headers=headers)
    if response.status_code == 200:
        return json.dumps(response.json(), indent=2)
    return f"Error fetching tasks: {response.status_code} - {response.text}"

@mcp.tool()
def create_task(title: str, description: str = "", status: str = "pending") -> str:
    """Creates a new task in the backend."""
    headers = get_headers()
    payload = {
        "title": title,
        "description": description,
        "status": status
    }
    response = requests.post(f"{BASE_URL}/api/v1/tasks/", json=payload, headers=headers)
    if response.status_code in (200, 201):
        return f"Task created successfully: {json.dumps(response.json(), indent=2)}"
    return f"Error creating task: {response.status_code} - {response.text}"

if __name__ == "__main__":
    mcp.run()
