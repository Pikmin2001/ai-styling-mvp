from app.data.kaggle_inventory import _classify_inventory_item


def test_classify_inventory_item_detects_top_bottom_and_shoes():
    top_row = {
        "masterCategory": "Apparel",
        "subCategory": "Topwear",
        "articleType": "Tshirts",
        "gender": "Men",
    }
    bottom_row = {
        "masterCategory": "Apparel",
        "subCategory": "Bottomwear",
        "articleType": "Jeans",
        "gender": "Women",
    }
    shoe_row = {
        "masterCategory": "Footwear",
        "subCategory": "Shoes",
        "articleType": "Casual Shoes",
        "gender": "Men",
    }

    assert _classify_inventory_item(top_row) == "top"
    assert _classify_inventory_item(bottom_row) == "bottom"
    assert _classify_inventory_item(shoe_row) == "shoes"


def test_classify_inventory_item_filters_accessories_and_non_wardrobe_items():
    belt_row = {
        "masterCategory": "Accessories",
        "subCategory": "Belts",
        "articleType": "Belts",
        "gender": "Women",
    }
    deodorant_row = {
        "masterCategory": "Personal Care",
        "subCategory": "Deodorants",
        "articleType": "Deodorant",
        "gender": "Men",
    }

    assert _classify_inventory_item(belt_row) is None
    assert _classify_inventory_item(deodorant_row) is None
