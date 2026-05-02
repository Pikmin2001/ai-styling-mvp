def enrich_tags(item):
    tags = set(getattr(item, "style_tags", []) or [])

    if item.category in ["hoodie", "sneakers", "shoes"]:
        tags.add("streetwear")

    if item.color in ["black", "white", "gray", "navy", "khaki"]:
        tags.add("minimalist")

    if item.formality in ["formal", "smart casual"]:
        tags.add("formal")

    if item.formality == "casual":
        tags.add("casual")

    return list(tags)