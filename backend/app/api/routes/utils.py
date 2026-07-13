import base64
import os
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends, File, UploadFile
from fastapi import Body
from pydantic.networks import EmailStr

from app.api.deps import get_current_active_superuser
from app.data.fake_inventory import fake_items
from app.models import ClothItem, Message
from app.services.tagging_service import enrich_tags, suggest_tags_from_image
from app.utils import generate_test_email, send_email

router = APIRouter(prefix="/utils", tags=["utils"])


@router.post(
    "/test-email/",
    dependencies=[Depends(get_current_active_superuser)],
    status_code=201,
)
def test_email(email_to: EmailStr) -> Message:
    """
    Test emails.
    """
    email_data = generate_test_email(email_to=email_to)
    send_email(
        email_to=email_to,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return Message(message="Test email sent")


@router.get("/health-check/")
async def health_check() -> bool:
    return True


@router.post("/tag-image/")
async def tag_image(
    file: UploadFile | None = File(None),
    name: str | None = None,
    category: str | None = None,
    color: str | None = None,
    formality: str | None = None,
) -> dict[str, object]:
    image_bytes = await file.read() if file else None
    prompt = (
        f"Item: {name or 'unknown'}; category: {category or 'unknown'}; "
        f"color: {color or 'unknown'}; formality: {formality or 'unknown'}"
    )

    from types import SimpleNamespace

    metadata_item = SimpleNamespace(
        name=name or "",
        category=category or "",
        color=color or "",
        formality=formality or "",
        style_tags=[],
    )

    metadata_tags = enrich_tags(metadata_item)
    image_tags = suggest_tags_from_image(image_bytes, prompt=prompt)
    tags = sorted(set(metadata_tags) | set(image_tags))

    return {
        "tags": tags,
        "source": "image" if image_tags else "metadata",
    }


@router.post("/import-lookbook-images/")
async def import_lookbook_images(
    files: list[UploadFile] | None = None,
    file_path: str | None = None,
    file_paths: str | None = None,
    category: str | None = None,
    gender: str | None = None,
    color: str | None = None,
    formality: str | None = None,
    request: Any | None = None,
) -> dict[str, Any]:
    if request is not None and hasattr(request, "form"):
        form_data = await request.form()
        if not files:
            files = []
        for key, value in form_data.items():
            if key == "files" and value != "":
                if isinstance(value, UploadFile):
                    files.append(value)
            elif key == "file_path" and value not in {None, ""}:
                file_path = str(value)
            elif key == "file_paths" and value not in {None, ""}:
                file_paths = str(value)
            elif key == "category" and value not in {None, ""}:
                category = str(value)
            elif key == "gender" and value not in {None, ""}:
                gender = str(value)
            elif key == "color" and value not in {None, ""}:
                color = str(value)
            elif key == "formality" and value not in {None, ""}:
                formality = str(value)

    repo_root = Path(__file__).resolve().parents[3]
    public_dir = repo_root / "frontend" / "public" / "lookbook-imports"
    public_dir.mkdir(parents=True, exist_ok=True)

    path_inputs: list[str] = []
    if file_path:
        path_inputs.extend([segment.strip() for segment in file_path.split(",") if segment.strip()])
    if file_paths:
        path_inputs.extend([segment.strip() for segment in file_paths.split(",") if segment.strip()])

    imported: list[dict[str, Any]] = []
    next_id = max((item.id for item in fake_items if isinstance(item.id, int)), default=1000) + 1

    async def _add_image_from_bytes(name: str, contents: bytes, *, source_path: str | None = None) -> None:
        nonlocal next_id
        safe_name = "".join(ch if ch.isalnum() or ch in {".", "-", "_"} else "_" for ch in Path(name).name)
        if not safe_name:
            safe_name = f"image_{next_id}"
        destination_path = public_dir / safe_name
        destination_path.write_bytes(contents)

        image_bytes = contents
        prompt = (
            f"Item: {name}; category: {category or 'unknown'}; "
            f"color: {color or 'unknown'}; formality: {formality or 'unknown'}"
        )
        metadata_item = ClothItem(
            id=next_id,
            name=name,
            category=category or "top",
            gender=gender or "unisex",
            price=30.0,
            in_stock=True,
            style_tags=[],
            color=color or "neutral",
            formality=formality or "casual",
            image_url=f"/lookbook-imports/{safe_name}",
        )
        tags = sorted(set(enrich_tags(metadata_item)) | set(suggest_tags_from_image(image_bytes, prompt=prompt)))
        fake_items.append(metadata_item)
        imported.append(
            {
                "name": name,
                "image_url": metadata_item.image_url,
                "tags": tags,
                "category": metadata_item.category,
                "source": source_path or "upload",
            }
        )
        next_id += 1

    if files:
        for upload in files:
            if not upload.filename:
                continue
            contents = await upload.read()
            await _add_image_from_bytes(upload.filename, contents, source_path=upload.filename)

    for path_value in path_inputs:
        resolved_path = Path(path_value).expanduser()
        if not resolved_path.is_absolute():
            resolved_path = repo_root / resolved_path

        if resolved_path.is_file():
            contents = resolved_path.read_bytes()
            await _add_image_from_bytes(resolved_path.name, contents, source_path=str(resolved_path))
        elif resolved_path.is_dir():
            for image_path in sorted(resolved_path.iterdir()):
                if image_path.is_file() and image_path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".gif"}:
                    contents = image_path.read_bytes()
                    await _add_image_from_bytes(image_path.name, contents, source_path=str(image_path))

    return {"items": imported, "count": len(imported)}
