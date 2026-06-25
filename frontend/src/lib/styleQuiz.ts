export type StyleQuizOption = {
  value: string
  label: string
}

export type StyleQuizQuestion = {
  id: string
  question: string
  options: StyleQuizOption[]
}

export const styleQuizQuestions: StyleQuizQuestion[] = [
  {
    id: "aesthetic",
    question: "Which overall aesthetic feels most like you?",
    options: [
      { value: "minimalist", label: "Clean, pared-back silhouettes" },
      { value: "old_money", label: "Polished, heritage-inspired looks" },
      { value: "streetwear", label: "Bold, urban edge" },
      { value: "romantic_feminine", label: "Soft, expressive details" },
    ],
  },
  {
    id: "occasion",
    question: "What would you wear to your ideal day out?",
    options: [
      { value: "business_casual", label: "A crisp shirt and chinos for a polished city stroll" },
      { value: "athleisure", label: "A refined tracksuit and sneakers for effortless comfort" },
      { value: "dark_academia", label: "A wool coat with layered knits for a cultured afternoon" },
      { value: "romantic_feminine", label: "A flowy dress with soft textures for a dreamy cafe date" },
    ],
  },
  {
    id: "details",
    question: "Which detail do you care about most?",
    options: [
      { value: "quiet_luxury", label: "Understated quality and texture" },
      { value: "contemporary_trendy", label: "Fresh street-forward details" },
      { value: "edgy", label: "Contrast and attitude" },
      { value: "classic_menswear", label: "Tailoring with a polished finish" },
    ],
  },
  {
    id: "palette",
    question: "What palette or mood feels right?",
    options: [
      { value: "minimalist", label: "Soft neutrals and simple lines" },
      { value: "coastal", label: "Warm, breezy tones" },
      { value: "dark_academia", label: "Rich textures and deep tones" },
      { value: "streetwear", label: "High-contrast athleisure pieces" },
    ],
  },
]

export const initialQuizAnswers = styleQuizQuestions.reduce(
  (acc, question) => {
    acc[question.id] = ""
    return acc
  },
  {} as Record<string, string>,
)
