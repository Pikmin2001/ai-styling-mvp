from pathlib import Path

from app.data.fake_inventory import fake_items
from app.models import ClothItem
from app.services.tagging_service import enrich_tags, suggest_tags_from_image


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


def test_fake_inventory_only_keeps_items_with_real_image_assets():
    repo_root = Path(__file__).resolve().parents[2]
    public_dir = repo_root / "frontend" / "public"

    for item in fake_items:
        if item.image_url:
            asset_path = public_dir / item.image_url.lstrip("/")
            assert asset_path.exists(), f"{item.name} should have a real image asset"


def test_suggest_tags_from_image_parses_output_payload(monkeypatch):
    class _FakeResponse:
        pass

    class _FakeClient:
        class _Responses:
            def create(self, *args, **kwargs):
                return _FakeResponse()

        responses = _Responses()

    monkeypatch.setattr("app.services.tagging_service.OpenAI", lambda: _FakeClient())

    tags = suggest_tags_from_image(b"image-bytes", prompt="test")

    assert tags == []
