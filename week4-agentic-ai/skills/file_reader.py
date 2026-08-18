"""File-read plugin: lets the agent read .txt and .pdf files from disk."""

from pathlib import Path

from pypdf import PdfReader

MAX_CHARS = 4000


def read_file(path: str) -> str:
    """Read a .txt or .pdf file and return its text content (truncated for the LLM context)."""
    file_path = Path(path)
    if not file_path.exists():
        return f"File not found: {path}"

    if file_path.suffix.lower() == ".txt":
        text = file_path.read_text(encoding="utf-8", errors="ignore")
    elif file_path.suffix.lower() == ".pdf":
        reader = PdfReader(str(file_path))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    else:
        return f"Unsupported file type '{file_path.suffix}'. Only .txt and .pdf are supported."

    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS] + f"\n...[truncated, {len(text) - MAX_CHARS} more characters]"

    return text or "(file was empty or text could not be extracted)"
