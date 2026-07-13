from pathlib import Path

from app.models import ClothItem
from app.data.kaggle_inventory import _prepare_public_image, load_kaggle_items
from app.services.tagging_service import enrich_tags


def _item_has_public_image(item: ClothItem) -> bool:
    if not item.image_url:
        return False

    asset_path = Path(__file__).resolve().parents[2] / "frontend" / "public" / item.image_url.lstrip("/")
    return asset_path.exists()


def _refresh_public_image(item: ClothItem) -> None:
    if not item.image_url:
        return

    asset_path = Path(__file__).resolve().parents[2] / "frontend" / "public" / item.image_url.lstrip("/")
    if not asset_path.exists() or asset_path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
        return

    _prepare_public_image(asset_path, asset_path)


def _infer_category_from_name(name: str) -> str:
    lowered = name.lower()
    if any(token in lowered for token in ["shoe", "boot", "sneaker", "loafer", "heel"]):
        return "shoes"
    if any(token in lowered for token in ["pant", "jean", "trouser", "skirt", "short", "legging"]):
        return "bottom"
    return "top"


def _infer_gender_from_name(name: str) -> str:
    lowered = name.lower()
    if any(token in lowered for token in ["male", "men", "mens", "man"]):
        return "male"
    if any(token in lowered for token in ["female", "women", "womens", "woman"]):
        return "female"
    return "unisex"


def _infer_tags_from_name(name: str) -> list[str]:
    lowered = name.lower()
    tags: set[str] = set()
    if any(token in lowered for token in ["streetwear", "urban", "oversized"]):
        tags.add("streetwear")
    if any(token in lowered for token in ["formal", "tailored", "blazer", "suit"]):
        tags.add("formal")
    if any(token in lowered for token in ["jean", "denim"]):
        tags.add("denim")
    if any(token in lowered for token in ["leather", "black"]):
        tags.add("minimalist")
    return sorted(tags)


def _load_public_folder_items(existing_items: list[ClothItem]) -> list[ClothItem]:
    repo_root = Path(__file__).resolve().parents[2]
    public_root = repo_root / "frontend" / "public"
    existing_urls = {item.image_url for item in existing_items if item.image_url}
    discovered: list[ClothItem] = []

    for folder_name in ["images", "lookbook-imports"]:
        folder = public_root / folder_name
        if not folder.exists():
            continue

        for image_path in sorted(folder.iterdir()):
            if not image_path.is_file():
                continue
            if image_path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp", ".gif"}:
                continue

            relative_url = f"/{folder_name}/{image_path.name}"
            if relative_url in existing_urls:
                continue

            base_name = image_path.stem.replace("_", " ").replace("-", " ").strip()
            category = _infer_category_from_name(base_name)
            gender = _infer_gender_from_name(base_name)
            metadata_item = ClothItem(
                id=100000 + len(discovered) + len(existing_items),
                name=base_name or image_path.name,
                category=category,
                gender=gender,
                price=55.0,
                in_stock=True,
                style_tags=[],
                color="neutral",
                formality="casual",
                image_url=relative_url,
            )
            tags = enrich_tags(metadata_item)
            metadata_item.style_tags = sorted(set(tags) | set(_infer_tags_from_name(base_name)))
            discovered.append(metadata_item)
            existing_urls.add(relative_url)

    return discovered


starter_items = [
    ClothItem(
        id=1,
        name="Black_Oversized_Tee",
        category="top",
        gender="male",
        price=25,
        in_stock=True,
        style_tags=["streetwear", "casual"],
        color="black",
        formality="casual",
        image_url="/images/Black_Oversized_Tee.jpg",
    ),
    ClothItem(
        id=2,
        name="Blue Straight Jeans",
        category="bottom",
        gender="male",
        price=50,
        in_stock=True,
        style_tags=["casual", "minimalist"],
        color="blue",
        formality="casual",
        image_url="/images/Blue_Straight_Jeans.jpg",
    ),
    ClothItem(
        id=3,
        name="White Sneakers",
        category="shoes",
        gender="male",
        price=70,
        in_stock=True,
        style_tags=["streetwear", "casual"],
        color="white",
        formality="casual",
        image_url="/images/White_Sneakers.jpg",
    ),
    ClothItem(
        id=4,
        name="Oxford Button Down",
        category="top",
        gender="male",
        price=45,
        in_stock=True,
        style_tags=["formal", "minimalist"],
        color="white",
        formality="smart casual",
        image_url="/images/Oxford_Button_Down.jpg",
    ),
    ClothItem(
        id=5,
        name="Slim Chino Pants",
        category="bottom",
        gender="male",
        price=60,
        in_stock=True,
        style_tags=["formal", "minimalist"],
        color="khaki",
        formality="smart casual",
        image_url="/images/Slim_Chino_Pants.jpg",
    ),
    ClothItem(
        id=6,
        name="Brown Loafers",
        category="shoes",
        gender="male",
        price=85,
        in_stock=True,
        style_tags=["formal", "minimalist"],
        color="brown",
        formality="smart casual",
        image_url="/images/Brown_Loafers.jpg",
    ),
    ClothItem(
        id=7,
        name="Cropped Knit Top",
        category="top",
        gender="female",
        price=35,
        in_stock=True,
        style_tags=["casual", "minimalist"],
        color="cream",
        formality="casual",
        image_url="/images/Cropped_Knit_Top.jpg",
    ),
    ClothItem(
        id=8,
        name="Black Midi Skirt",
        category="bottom",
        gender="female",
        price=55,
        in_stock=True,
        style_tags=["minimalist", "formal"],
        color="black",
        formality="smart casual",
        image_url="/images/Black_Midi_Skirt.png",
    ),
    ClothItem(
        id=9,
        name="White Platform Sneakers",
        category="shoes",
        gender="female",
        price=65,
        in_stock=True,
        style_tags=["streetwear", "casual"],
        color="white",
        formality="casual",
        image_url="/images/White_Platform_Sneakers.jpg",
    ),
]

for item in starter_items:
    _refresh_public_image(item)

starter_items = [item for item in starter_items if _item_has_public_image(item)]

kaggle_items = load_kaggle_items(limit=40, copy_images=True)
folder_items = _load_public_folder_items(starter_items + [item for item in kaggle_items if _item_has_public_image(item)])
fake_items = starter_items + [item for item in kaggle_items if _item_has_public_image(item)] + folder_items