from __future__ import annotations

import csv
import os
import shutil
from pathlib import Path
from typing import Iterable

from app.models import ClothItem


def _normalize_text(value: str | None) -> str:
    return (value or "").strip()


def _infer_category(master_category: str | None, sub_category: str | None) -> str:
    master = (master_category or "").lower()
    sub = (sub_category or "").lower()

    if "footwear" in master or any(word in sub for word in ["shoe", "heels", "flats", "boots", "sandal"]):
        return "shoes"
    if any(word in sub for word in ["jeans", "trouser", "pants", "skirt", "shorts", "legging"]):
        return "bottom"
    return "top"


def _infer_formality(article_type: str | None, usage: str | None) -> str:
    text = " ".join(filter(None, [article_type, usage])).lower()
    if any(word in text for word in ["shirt", "blazer", "suit", "formal", "dress"]):
        return "formal"
    if any(word in text for word in ["jeans", "tshirt", "top", "sweat", "hoodie"]):
        return "casual"
    return "smart casual"


def _infer_tags(row: dict[str, str]) -> list[str]:
    tags: set[str] = set()
    gender = _normalize_text(row.get("gender")).lower() or "unisex"
    master = _normalize_text(row.get("masterCategory")).lower()
    sub = _normalize_text(row.get("subCategory")).lower()
    article = _normalize_text(row.get("articleType")).lower()
    color = _normalize_text(row.get("baseColour")).lower()
    usage = _normalize_text(row.get("usage")).lower()

    if gender in {"men", "male"}:
        tags.add("men")
    elif gender in {"women", "female"}:
        tags.add("women")
    else:
        tags.add("unisex")

    if master:
        tags.add(master.replace(" ", "_"))
    if sub:
        tags.add(sub.replace(" ", "_"))
    if article:
        tags.add(article.replace(" ", "_"))
    if color:
        tags.add(color.replace(" ", "_"))
    if usage:
        tags.add(usage.replace(" ", "_"))

    if any(word in article for word in ["shirt", "blazer", "dress", "suit"]):
        tags.add("formal")
    if any(word in article for word in ["tee", "tshirt", "jeans", "hoodie", "sweat"]):
        tags.add("casual")

    return sorted(tags)


def _discover_dataset_files() -> tuple[Path | None, Path | None]:
    candidates: Iterable[Path] = [
        Path(os.getenv("KAGGLE_STYLES_CSV", "")) if os.getenv("KAGGLE_STYLES_CSV") else None,
        Path(os.getenv("KAGGLE_IMAGES_DIR", "")) if os.getenv("KAGGLE_IMAGES_DIR") else None,
    ]
    explicit_csv = next((c for c in candidates if isinstance(c, Path) and str(c) and c.exists()), None)
    explicit_images_dir = None

    search_roots = [
        Path(__file__).resolve().parents[2],
        Path(__file__).resolve().parents[3],
        Path.cwd(),
    ]

    for root in search_roots:
        for candidate_csv in [
            root / "styles.csv",
            root / "fashion-product-images-small" / "styles.csv",
            root / "data" / "styles.csv",
            root / "data" / "fashion-product-images-small" / "styles.csv",
        ]:
            if candidate_csv.exists():
                csv_path = candidate_csv
                images_dir = next((p for p in [
                    root / "images",
                    root / "fashion-product-images-small" / "images",
                    root / "data" / "images",
                    root / "data" / "fashion-product-images-small" / "images",
                ] if p.exists()), None)
                return csv_path, images_dir

    return None, None


def load_kaggle_items(limit: int = 40, copy_images: bool = True) -> list[ClothItem]:
    csv_path, images_dir = _discover_dataset_files()
    if not csv_path:
        return []

    public_dir = Path(__file__).resolve().parents[2] / "frontend" / "public" / "kaggle-images"
    public_dir.mkdir(parents=True, exist_ok=True)

    items: list[ClothItem] = []
    with csv_path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for index, row in enumerate(reader):
            if index >= limit:
                break

            item_id = _normalize_text(row.get("id")) or str(index + 1)
            image_name = f"{item_id}.jpg"
            image_path = images_dir / image_name if images_dir else None

            public_image_path = public_dir / image_name
            if copy_images and image_path and image_path.exists() and not public_image_path.exists():
                shutil.copy2(image_path, public_image_path)

            image_url = f"/kaggle-images/{image_name}" if public_image_path.exists() else None
            category = _infer_category(row.get("masterCategory"), row.get("subCategory"))
            price = 30 + ((index % 7) * 8)
            if category == "shoes":
                price += 20
            elif category == "bottom":
                price += 10

            item = ClothItem(
                id=int(item_id),
                name=_normalize_text(row.get("productDisplayName")) or f"Kaggle item {item_id}",
                category=category,
                gender=(_normalize_text(row.get("gender")).lower() or "unisex"),
                price=float(price),
                in_stock=True,
                style_tags=_infer_tags(row),
                color=_normalize_text(row.get("baseColour")) or "neutral",
                formality=_infer_formality(row.get("articleType"), row.get("usage")),
                image_url=image_url,
            )
            items.append(item)

    return items
