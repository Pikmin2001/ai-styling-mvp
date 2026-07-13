from __future__ import annotations

import ast
import base64
from typing import Any, cast

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover - optional dependency
    OpenAI = None


def _normalize_tag(tag: str) -> str:
    return tag.strip().lower().replace(" ", "_")


def enrich_tags(item: Any) -> list[str]:
    tags = {_normalize_tag(tag) for tag in (getattr(item, "style_tags", []) or [])}

    category = (getattr(item, "category", "") or "").lower()
    color = (getattr(item, "color", "") or "").lower()
    formality = (getattr(item, "formality", "") or "").lower()
    name = (getattr(item, "name", "") or "").lower()

    if category in {"hoodie", "sneaker", "sneakers", "shoe", "shoes", "jacket"}:
        tags.add("streetwear")

    if category in {"skirt", "dress", "blouse", "shirt", "top", "button_down"}:
        tags.add("smart_casual")

    if color in {"black", "white", "gray", "navy", "khaki", "cream"}:
        tags.add("minimalist")

    if formality in {"formal", "smart casual", "smart_casual"}:
        tags.add("formal")

    if formality in {"casual", "streetwear"}:
        tags.add("casual")

    if any(keyword in name for keyword in ["oversized", "relaxed", "loose", "cropped"]):
        tags.add("relaxed")

    if any(keyword in name for keyword in ["slim", "tailored", "straight", "structured"]):
        tags.add("structured")

    if any(keyword in name for keyword in ["denim", "jeans", "cargo", "chinos"]):
        tags.add("denim")

    return sorted(tags)


def _extract_response_text(response: Any) -> str:
    if response is None:
        return ""

    output_text = getattr(response, "output_text", None)
    if isinstance(output_text, str) and output_text.strip():
        return output_text

    output = getattr(response, "output", None)
    if isinstance(output, list):
        pieces: list[str] = []
        for item in output:
            if isinstance(item, dict):
                content = item.get("content")
                if isinstance(content, list):
                    for entry in content:
                        if isinstance(entry, dict):
                            text = entry.get("text")
                            if isinstance(text, str) and text.strip():
                                pieces.append(text)
                elif isinstance(content, str) and content.strip():
                    pieces.append(content)
            elif hasattr(item, "text"):
                text = getattr(item, "text")
                if isinstance(text, str) and text.strip():
                    pieces.append(text)

        if pieces:
            return "\n".join(pieces)

    return ""


def suggest_tags_from_image(image_bytes: bytes | None = None, *, prompt: str | None = None) -> list[str]:
    """Best-effort image tagging using OpenAI vision when credentials are available.

    Falls back to an empty list when no image is supplied or the SDK is unavailable.
    """
    if not image_bytes:
        return []

    if OpenAI is None:
        return []

    try:
        client = OpenAI()
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=cast(
                Any,
                [
                    {
                        "role": "system",
                        "content": "You are a fashion tagging assistant. Return a compact JSON array of style tags for the clothing in the image.",
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "input_text",
                                "text": prompt or "Describe the clothing style, formality, and color palette in a compact list of tags.",
                            },
                            {
                                "type": "input_image",
                                "image_url": f"data:image/jpeg;base64,{base64.b64encode(image_bytes).decode('ascii')}",
                            },
                        ],
                    },
                ],
            ),
        )
        content = _extract_response_text(response).strip()
        if content.startswith("["):
            parsed = ast.literal_eval(content)
            if isinstance(parsed, list):
                return [_normalize_tag(str(tag)) for tag in parsed]
    except Exception:
        return []

    return []

