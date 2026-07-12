from fastapi import APIRouter, Depends, File, UploadFile
from pydantic.networks import EmailStr

from app.api.deps import get_current_active_superuser
from app.models import Message
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
