from pathlib import Path


def load_markdown_files(notes_dir: str) -> list[tuple[str, str]]:
    root = Path(notes_dir)
    results = []
    for path in root.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        if text.strip():
            results.append((str(path.relative_to(root)), text))
    return results
