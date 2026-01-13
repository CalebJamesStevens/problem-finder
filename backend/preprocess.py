from __future__ import annotations

import re


CODE_BLOCK_RE = re.compile(r"<code>.*?</code>", re.DOTALL | re.IGNORECASE)
HTML_TAG_RE = re.compile(r"<[^>]+>")
URL_RE = re.compile(r"https?://\S+|www\.\S+")
WHITESPACE_RE = re.compile(r"\s+")


def clean_text(text: str) -> str:
    if not text:
        return ""
    text = CODE_BLOCK_RE.sub(" ", text)
    text = URL_RE.sub(" ", text)
    text = HTML_TAG_RE.sub(" ", text)
    text = text.lower()
    text = WHITESPACE_RE.sub(" ", text).strip()
    return text


def prepare_documents(records: list[dict]) -> list[str]:
    documents = []
    for record in records:
        title = clean_text(record.get("title", ""))
        body = clean_text(record.get("body", ""))
        combined = f"{title} {body}".strip()
        documents.append(combined)
    return documents
