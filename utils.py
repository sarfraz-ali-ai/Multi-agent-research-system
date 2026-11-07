import re
from typing import Any, List


def _flatten(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict):
                parts.append(str(block.get("text", "")))
            elif hasattr(block, "text"):
                parts.append(str(block.text))
        return "\n".join(p for p in parts if p)
    return str(content)


def extract_text(response: Any) -> str:
    if isinstance(response, str):
        return response
    if isinstance(response, dict) and "messages" in response:
        last = response["messages"][-1]
        return _flatten(getattr(last, "content", last))
    if hasattr(response, "content"):
        return _flatten(response.content)
    return _flatten(response)


def extract_urls(text: str) -> List[str]:
    urls = re.findall(r"https?://[^\s\)\]\"<>]+", text)
    urls = [u.rstrip(".,;:") for u in urls]
    seen, out = set(), []
    for u in urls:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out