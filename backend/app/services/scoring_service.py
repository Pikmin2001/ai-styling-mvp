from typing import List, Optional


def score_item(item, styles: Optional[List[str]]) -> int:
    if not styles:
        return 0

    return sum(1 for style in styles if style in item.style_tags)


def combo_score(top, bottom, shoes, styles: Optional[List[str]]) -> int:
    style_overlap = (
        len(set(top.style_tags) & set(bottom.style_tags))
        + len(set(top.style_tags) & set(shoes.style_tags))
        + len(set(bottom.style_tags) & set(shoes.style_tags))
    )

    requested = set(styles or [])

    requested_bonus = 1 if (
        requested
        and (requested & set(top.style_tags))
        and (requested & set(bottom.style_tags))
        and (requested & set(shoes.style_tags))
    ) else 0

    neutrals = {"black", "white", "gray", "khaki", "navy"}
    colors = [top.color, bottom.color, shoes.color]
    neutral_count = sum(1 for color in colors if color in neutrals)
    color_bonus = 1 if neutral_count >= 2 else 0

    return style_overlap + requested_bonus + color_bonus