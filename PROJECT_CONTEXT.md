# AI Styling MVP - Project Context

## Project Overview

AI Styling MVP is a full-stack fashion recommendation platform.

Current stack:

Frontend:

* React
* TypeScript
* Vite
* TanStack Router

Backend:

* FastAPI
* Python
* Pydantic
* SQLModel

## Current Features

* Outfit generation
* Budget filtering
* Gender filtering
* Style preference selection
* Outfit swapping
* Outfit saving
* Clothing item image display
* Responsive UI

## Current Recommendation Logic

Inventory items contain:

* category
* gender
* price
* style_tags
* color
* formality
* image_url

Outfit generation:

1. Filter inventory
2. Generate outfit candidates
3. Score candidates using:

   * style overlap
   * requested styles
   * color coordination
4. Return highest-scoring outfit

## Long-Term Product Vision

The platform is moving toward:

User → Aesthetic Profile → Outfit Recommendation → Store Inventory Match

Rather than:

User → Individual Clothing Items

## Planned Style Taxonomy

Core archetypes:

* Minimalist
* Old Money
* Quiet Luxury
* Streetwear
* Business Casual
* Classic Menswear
* Athleisure
* Dark Academia
* Coastal
* Contemporary Trendy
* Edgy
* Romantic/Feminine

## Future Roadmap

Phase 1:

* Style Quiz
* Aesthetic scoring
* Outfit explanations

Phase 2:

* Outfit swipe system
* User taste profiling
* Saved user profiles

Phase 3:

* Automated image tagging
* Computer vision embeddings
* Similar outfit search

Phase 4:

* Retail inventory integrations
* Personalized in-store recommendations

## Design Philosophy

Fashion recommendations should be driven by aesthetics and identity rather than individual clothing attributes.

Users generally think:

"I want an Old Money look."

not:

"I want a navy Oxford shirt."

The recommendation system should optimize for aesthetic alignment first and item selection second.
