from typing import Optional


from typing import Optional, List

def score_item(item, styles: Optional[List[str]]) -> int:
    if not styles:
        return 0
    # count overlaps
    return sum(1 for s in styles if s in item.style_tags)

def pick_best_item(items, styles: Optional[List[str]]):
    # break ties by price (cheaper wins) or randomize if you prefer
    return max(items, key=lambda item: (score_item(item, styles), -item.price))


def generate_outfit(
    items,
    gender: Optional[str] = None,
    max_price: Optional[float] = None,
    style: Optional[str] = None,
):
    filtered_items = [
        item for item in items
        if item.in_stock
        and (gender is None or item.gender == gender)
        and (max_price is None or item.price <= max_price)
    ]

    tops = [i for i in filtered_items if i.category == "top"]
    bottoms = [i for i in filtered_items if i.category == "bottom"]
    shoes = [i for i in filtered_items if i.category == "shoes"]

    if not tops or not bottoms or not shoes:
        return None

    top = pick_best_item(tops, style)
    bottom = pick_best_item(bottoms, style)
    shoe = pick_best_item(shoes, style)

    total_price = top.price + bottom.price + shoe.price

    return {
        "top": top.model_dump(),
        "bottom": bottom.model_dump(),
        "shoes": shoe.model_dump(),
        "total_price": total_price,
        "style": style,
    }