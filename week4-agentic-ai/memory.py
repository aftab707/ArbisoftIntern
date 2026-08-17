"""Agent memory: in-context conversation history + a key-value fact store."""

from datetime import datetime


class AgentMemory:
    def __init__(self):
        self.history = []
        self.facts = {}

    def add_message(
        self,
        role: str,
        content,
        tool_call_id: str | None = None,
        name: str | None = None,
        tool_calls: list | None = None,
    ):
        message = {"role": role, "content": content}
        if tool_call_id:
            message["tool_call_id"] = tool_call_id
        if name:
            message["name"] = name
        if tool_calls:
            message["tool_calls"] = tool_calls
        self.history.append(message)

    def remember_fact(self, key: str, value: str) -> str:
        self.facts[key] = {"value": value, "saved_at": datetime.now().isoformat(timespec="seconds")}
        return f"Remembered '{key}' = '{value}'."

    def recall_fact(self, key: str) -> str:
        entry = self.facts.get(key)
        if not entry:
            return f"No fact remembered under '{key}'."
        return f"{key} = {entry['value']} (saved at {entry['saved_at']})"

    def all_facts(self) -> dict:
        return self.facts
