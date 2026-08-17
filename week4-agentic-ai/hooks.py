"""Pre/post hooks that wrap every tool call with a timestamped log line."""

import functools
import json
import time
from datetime import datetime
from pathlib import Path

LOG_FILE = Path(__file__).parent / "tool_calls.log"


def log_tool_call(func):
    """Decorator: logs tool name, args, duration, and result to tool_calls.log."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        started_at = datetime.now().isoformat(timespec="seconds")
        start = time.perf_counter()
        status = "ok"
        result_preview = None
        try:
            result = func(*args, **kwargs)
            result_preview = str(result)[:200]
            return result
        except Exception as exc:  # log failures too, then re-raise
            status = "error"
            result_preview = str(exc)[:200]
            raise
        finally:
            duration_ms = round((time.perf_counter() - start) * 1000, 2)
            entry = {
                "timestamp": started_at,
                "tool": func.__name__,
                "args": kwargs or (args if args else {}),
                "duration_ms": duration_ms,
                "status": status,
                "result_preview": result_preview,
            }
            with LOG_FILE.open("a", encoding="utf-8") as f:
                f.write(json.dumps(entry, default=str) + "\n")
            print(f"[hook] {func.__name__} called ({status}, {duration_ms}ms)")

    return wrapper
