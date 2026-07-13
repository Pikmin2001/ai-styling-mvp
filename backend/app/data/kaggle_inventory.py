from __future__ import annotations

import csv
import os
import shutil
from pathlib import Path
from typing import Iterable

try:
    from PIL import Image, ImageEnhance, ImageFilter, ImageOps
except ImportError:  # pragma: no cover - optional dependency
    Image = None
    ImageEnhance = None
    ImageFilter = None
    ImageOps = None

from app.models import ClothItem


def _prepare_public_image(source_path: Path, destination_path: Path, max_side: int = 1600) -> None:
    if not source_path.exists():
        return

    destination_path.parent.mkdir(parents=True, exist_ok=True)
    if destination_path.exists():
        destination_path.unlink()

    if Image is None or ImageEnhance is None or ImageFilter is None or ImageOps is None:
        shutil.copy2(source_path, destination_path)
        return

    try:
        with Image.open(source_path) as image:
            image = ImageOps.exif_transpose(image)
            if image.mode in {"RGBA", "LA", "P"}:
                background = Image.new("RGB", image.size, (255, 255, 255))
                background.paste(image.convert("RGBA"), mask=image.convert("RGBA").split()[-1])
                image = background
            else:
                image = image.convert("RGB")

            width, height = image.size
            scale = max_side / max(width, height)
            resampling_module = getattr(Image, "Resampling", None)
            resize_filter = getattr(resampling_module, "LANCZOS", None)
            if resize_filter is None:
                resize_filter = getattr(Image, "LANCZOS", None)
            if resize_filter is None:
                resize_filter = 3

            if scale < 1:
                image = image.resize((max(1, int(width * scale)), max(1, int(height * scale))), resize_filter)
            elif max(width, height) < max_side:
                image = image.resize((max(1, int(width * 1.25)), max(1, int(height * 1.25))), resize_filter)

            image = image.filter(ImageFilter.UnsharpMask(radius=1, percent=120, threshold=3))
            image = ImageEnhance.Sharpness(image).enhance(1.2)
            image.save(destination_path, format="JPEG", quality=95, optimize=True, progressive=True)
    except Exception:
        shutil.copy2(source_path, destination_path)


def _normalize_text(value: str | None) -> str:
    return (value or "").strip()


def _classify_inventory_item(row: dict[str, str]) -> str | None:
    master = (_normalize_text(row.get("masterCategory"))).lower()
    sub = (_normalize_text(row.get("subCategory"))).lower()
    article = (_normalize_text(row.get("articleType"))).lower()
    text = " ".join(filter(None, [master, sub, article]))

    if any(token in text for token in ["accessory", "watch", "belt", "socks", "wallet", "bag", "jewelry", "perfume", "deodorant", "cosmetic", "beauty"]):
        return None

    if any(token in text for token in ["footwear", "shoe", "heels", "flats", "boots", "sandal", "loafer", "sneaker"]):
        return "shoes"

    if any(token in text for token in ["jeans", "trouser", "pants", "skirt", "shorts", "legging", "bottomwear", "track pant", "trouser"]):
        return "bottom"

    if any(token in text for token in ["topwear", "shirt", "tshirt", "tee", "blouse", "top", "coat", "jacket", "blazer", "sweater", "kurta", "dress"]):
        return "top"

    return None


def _infer_category(master_category: str | None, sub_category: str | None) -> str:
    return _classify_inventory_item({
        "masterCategory": master_category or "",
        "subCategory": sub_category or "",
    }) or "top"


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

    repo_root = Path(__file__).resolve().parents[3]
    public_dir = repo_root / "frontend" / "public" / "kaggle-images"
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
            if copy_images and image_path and image_path.exists():
                _prepare_public_image(image_path, public_image_path)

            image_url = f"/kaggle-images/{image_name}" if public_image_path.exists() else None
            category = _classify_inventory_item(row)
            if not category or not image_url:
                continue

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
