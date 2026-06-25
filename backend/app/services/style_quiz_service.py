from typing import Any

STYLE_ARCHETYPES = {
    "Minimalist": ["minimalist", "formal"],
    "Old Money": ["old money", "classic menswear"],
    "Quiet Luxury": ["quiet luxury", "minimalist"],
    "Streetwear": ["streetwear", "casual"],
    "Business Casual": ["business casual", "formal"],
    "Classic Menswear": ["classic menswear", "formal"],
    "Athleisure": ["athleisure", "casual"],
    "Dark Academia": ["dark academia", "classic"],
    "Coastal": ["coastal", "casual"],
    "Contemporary Trendy": ["contemporary trendy", "streetwear"],
    "Edgy": ["edgy", "streetwear"],
    "Romantic/Feminine": ["romantic", "feminine", "classic"],
}

QUIZ_OPTIONS = {
    "minimalist": {"Minimalist": 2, "Quiet Luxury": 1},
    "old_money": {"Old Money": 2, "Classic Menswear": 1},
    "quiet_luxury": {"Quiet Luxury": 2, "Old Money": 1},
    "streetwear": {"Streetwear": 2, "Contemporary Trendy": 1},
    "business_casual": {"Business Casual": 2, "Quiet Luxury": 1},
    "classic_menswear": {"Classic Menswear": 2, "Old Money": 1},
    "athleisure": {"Athleisure": 2, "Streetwear": 1},
    "dark_academia": {"Dark Academia": 2, "Classic Menswear": 1},
    "coastal": {"Coastal": 2, "Contemporary Trendy": 1},
    "contemporary_trendy": {"Contemporary Trendy": 2, "Streetwear": 1},
    "edgy": {"Edgy": 2, "Streetwear": 1},
    "romantic_feminine": {"Romantic/Feminine": 2, "Coastal": 1},
}

QUIZ_QUESTIONS = [
    {
        "id": "aesthetic",
        "question": "Which overall aesthetic feels most like you?",
        "options": [
            {"value": "minimalist", "label": "Clean, pared-back silhouettes"},
            {"value": "old_money", "label": "Polished, heritage-inspired looks"},
            {"value": "streetwear", "label": "Bold, urban edge"},
            {"value": "romantic_feminine", "label": "Soft, expressive details"},
        ],
    },
    {
        "id": "occasion",
        "question": "What would you wear to your ideal day out?",
        "options": [
            {"value": "business_casual", "label": "A crisp shirt and chinos for a polished city stroll"},
            {"value": "athleisure", "label": "A refined tracksuit and sneakers for effortless comfort"},
            {"value": "dark_academia", "label": "A wool coat with layered knits for a cultured afternoon"},
            {"value": "romantic_feminine", "label": "A flowy dress with soft textures for a dreamy cafe date"},
        ],
    },
    {
        "id": "details",
        "question": "Which detail do you care about most?",
        "options": [
            {"value": "quiet_luxury", "label": "Understated quality and texture"},
            {"value": "contemporary_trendy", "label": "Fresh street-forward details"},
            {"value": "edgy", "label": "Contrast and attitude"},
            {"value": "classic_menswear", "label": "Tailoring with a polished finish"},
        ],
    },
    {
        "id": "palette",
        "question": "What palette or mood do you prefer?",
        "options": [
            {"value": "minimalist", "label": "Soft neutrals and simple lines"},
            {"value": "coastal", "label": "Warm, breezy tones"},
            {"value": "dark_academia", "label": "Rich textures and deep tones"},
            {"value": "streetwear", "label": "High-contrast athleisure pieces"},
        ],
    },
]


def get_quiz_questions() -> list[dict[str, Any]]:
    return [
        {
            "id": question["id"],
            "question": question["question"],
            "options": [
                {"value": option["value"], "label": option["label"]}
                for option in question["options"]
            ],
        }
        for question in QUIZ_QUESTIONS
    ]


def score_quiz_answers(answers: dict[str, str]) -> dict[str, Any]:
    scores = {key: 0 for key in STYLE_ARCHETYPES}

    for answer_value in answers.values():
        weights = QUIZ_OPTIONS.get(answer_value)
        if not weights:
            continue
        for archetype, weight in weights.items():
            scores[archetype] += weight

    ranked = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    primary = ranked[0][0] if ranked else "Minimalist"
    secondary = ranked[1][0] if len(ranked) > 1 else primary

    selected = []
    for archetype in [primary, secondary]:
        selected.extend(STYLE_ARCHETYPES.get(archetype, []))

    style_tags = sorted({tag for tag in selected})
    if not style_tags:
        style_tags = ["casual"]

    return {
        "archetypes": [primary, secondary],
        "style_tags": style_tags,
        "query_styles": style_tags,
    }
