import time
import json
import functools
from datetime import datetime

def log_tool_call(agent_name: str):
    """
    Decorator that logs a multi-agent tool call with agent_name included.
    Writes to agent_trace.log in JSON-lines format.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            status = "success"
            error_message = None
            result = None
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                status = "error"
                error_message = str(e)
                raise
            finally:
                duration = time.time() - start_time
                # Handle non-serializable arguments gracefully if needed
                # Here we assume simple args for tools
                log_entry = {
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "agent_name": agent_name,
                    "tool_name": func.__name__,
                    "args": [str(a) for a in args],
                    "kwargs": {k: str(v) for k, v in kwargs.items()},
                    "duration_seconds": round(duration, 4),
                    "status": status
                }
                if error_message:
                    log_entry["error"] = error_message
                
                with open("agent_trace.log", "a", encoding="utf-8") as f:
                    f.write(json.dumps(log_entry) + "\n")
        return wrapper
    return decorator
