from typing import Optional, List
import random


def score_item(item, styles: Optional[List[str]]) -> int:
    if not styles:
        return 0
    return sum(1 for s in styles if s in item.style_tags)


def combo_score(top, bottom, shoes, styles):
    style_overlap = len(set(top.style_tags) & set(bottom.style_tags)) \
                  + len(set(top.style_tags) & set(shoes.style_tags)) \
                  + len(set(bottom.style_tags) & set(shoes.style_tags))

    
    requested = set(styles or [])

    requested_bonus = 1 if (
        requested
        and (requested & set(top.style_tags))
        and (requested & set(bottom.style_tags))
        and (requested & set(shoes.style_tags))
    ) else 0

    neutrals = {"black", "white", "gray", "khaki", "navy"}
    colors = [top.color, bottom.color, shoes.color]
    neutral_count = sum(1 for c in colors if c in neutrals)
    color_bonus = 1 if neutral_count >= 2 else 0

    return style_overlap + requested_bonus + color_bonus


def generate_outfit(items, gender=None, max_price=None, styles=None):
    filtered = [
        i for i in items
        if i.in_stock
        and (gender is None or i.gender == gender)
        and (max_price is None or i.price <= max_price)
    ]

    tops = [i for i in filtered if i.category == "top"]
    bottoms = [i for i in filtered if i.category == "bottom"]
    shoes = [i for i in filtered if i.category == "shoes"]

    if not tops or not bottoms or not shoes:
        return None

    candidates = []

    for _ in range(10):
        t = random.choice(tops)
        b = random.choice(bottoms)
        s = random.choice(shoes)
        candidates.append((t, b, s))

    best = max(candidates, key=lambda c: combo_score(c[0], c[1], c[2], styles))

    top, bottom, shoe = best
    total = top.price + bottom.price + shoe.price

    return {
        "top": top.model_dump(),
        "bottom": bottom.model_dump(),
        "shoes": shoe.model_dump(),
        "total_price": total,
        "styles": styles,
    }