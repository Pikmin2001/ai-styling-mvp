from app.services.tagging_service import enrich_tags
from app.models import ClothItem


def test_enrich_tags_adds_expected_labels_for_common_items():
    item = ClothItem(
        id=101,
        name="Oversized Black Hoodie",
        category="hoodie",
        gender="male",
        price=40,
        in_stock=True,
        style_tags=[],
        color="black",
        formality="casual",
    )

    tags = enrich_tags(item)

    assert "streetwear" in tags
    assert "minimalist" in tags
    assert "casual" in tags


def test_enrich_tags_keeps_existing_tags_and_avoids_duplicates():
    item = ClothItem(
        id=102,
        name="Minimal Shirt",
        category="top",
        gender="female",
        price=30,
        in_stock=True,
        style_tags=["minimalist", "casual"],
        color="white",
        formality="smart casual",
    )

    tags = enrich_tags(item)

    assert tags.count("minimalist") == 1
    assert tags.count("casual") == 1
    assert "formal" in tags
