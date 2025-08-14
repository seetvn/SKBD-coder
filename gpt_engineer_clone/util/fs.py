from pathlib import Path

def safe_write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    content = content.replace("\r\n", "\n")
    path.write_text(content, encoding="utf-8")