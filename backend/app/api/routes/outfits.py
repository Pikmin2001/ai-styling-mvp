from fastapi import APIRouter
from typing import Optional
from app.services.outfit_service import generate_outfit
from app.data.fake_inventory import fake_items
from uuid import uuid4

router = APIRouter(prefix="/outfits", tags=["outfits"])
saved_outfits = {}

@router.post("/generate")
def generate(
    gender: Optional[str] = None,
    max_price: Optional[float] = None,
    style: Optional[str] = None,
):
    outfit = generate_outfit(fake_items, gender, max_price, style)

    if not outfit:
        return {"error": "Not enough items to build outfit"}

    return outfit

@router.post("/swap")
def swap_item(
    current_outfit: dict,
    item_type: str
):
    # Get current item
    current_item = current_outfit.get(item_type)

    if not current_item:
        return {"error": "No item to swap"}

    # Normalize current item
    if isinstance(current_item, dict):
        current_id = current_item.get("id")
        current_price = current_item.get("price")
        current_gender = current_item.get("gender")
    else:
        current_id = current_item.id
        current_price = current_item.price
        current_gender = current_item.gender
        
    if current_price is None:
        return {"error": "Current item is missing price"}
    # Step 1: same category + in stock
    candidates = [
        item for item in fake_items
        if item.category == item_type and item.in_stock
    ]

    # Step 2: remove current item FIRST
    candidates = [i for i in candidates if i.id != current_id]

    if not candidates:
        return {"error": "No items available to swap"}

    # Step 3: try same gender
    same_gender = [i for i in candidates if i.gender == current_gender]
    if same_gender:
        candidates = same_gender

    # Step 4: try similar price (but don’t force it)
    similar_price = [
        i for i in candidates
        if abs(i.price - current_price) <= 20
    ]
    if similar_price:
        candidates = similar_price

    # Step 5: pick closest price
    best_item = min(candidates, key=lambda x: abs(x.price - current_price))

    # Replace with dict
    current_outfit[item_type] = best_item.model_dump()

    # Recalculate total price
    total_price = sum([
        item["price"]
        for key, item in current_outfit.items()
        if key != "total_price" and item
    ])

    current_outfit["total_price"] = total_price

    return current_outfit

@router.post("/save")
def save_outfit(current_outfit: dict):
    outfit_id = str(uuid4())

    saved_outfits[outfit_id] = current_outfit

    return {
        "outfit_id": outfit_id,
        "share_url": f"/outfits/{outfit_id}",
        "outfit": current_outfit
    }


@router.get("/{outfit_id}")
def get_outfit(outfit_id: str):
    outfit = saved_outfits.get(outfit_id)

    if not outfit:
        return {"error": "Outfit not found"}

    return {
        "outfit_id": outfit_id,
        "outfit": outfit
    }