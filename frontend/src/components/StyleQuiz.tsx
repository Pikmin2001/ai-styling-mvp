import { useState } from "react"
import { styleQuizQuestions, initialQuizAnswers } from "@/lib/styleQuiz"

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000"

type QuizResult = {
  archetypes: string[]
  style_tags: string[]
  query_styles: string[]
}

type StyleQuizProps = {
  onQuizComplete: (result: QuizResult) => void
  selectedTags: string[]
}

export function StyleQuiz({ onQuizComplete, selectedTags }: StyleQuizProps) {
  const [answers, setAnswers] = useState({ ...initialQuizAnswers })
  const [currentStep, setCurrentStep] = useState(0)
  const [result, setResult] = useState<QuizResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  function handleSelect(questionId: string, value: string) {
    setAnswers((prev) => ({ ...prev, [questionId]: value }))
    setError(null)
  }

  async function handleSubmit() {
    if (Object.values(answers).some((value) => !value)) {
      setError("Please answer all quiz questions before submitting.")
      return
    }

    setLoading(true)
    setError(null)

    try {
      const response = await fetch(`${API_URL}/api/v1/quiz/score`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ answers }),
      })

      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.message || "Failed to score quiz")
      }

      setResult(data)
      onQuizComplete(data)
    } catch (err) {
      setError("Unable to score quiz. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <div style={{ marginBottom: 16 }}>
        <h3 style={{ marginBottom: 12 }}>Style Quiz</h3>
        <p style={{ color: "#cbd5e1", fontSize: 14, lineHeight: 1.6 }}>
          Answer a few quick questions and we’ll match your look to a style archetype.
        </p>
      </div>

      {styleQuizQuestions.map((questionItem, index) => (
        <div
          key={questionItem.id}
          style={{
            background: index === currentStep ? "#334155" : "#1e293b",
            padding: 18,
            borderRadius: 16,
            marginBottom: 16,
            opacity: index === currentStep ? 1 : 0.65,
          }}
        >
          <p style={{ margin: 0, marginBottom: 10, fontWeight: 600 }}>
            {questionItem.question}
          </p>

          <div style={{ display: "grid", gap: 10 }}>
            {questionItem.options.map((option) => (
              <label key={option.value} style={{ display: "block", cursor: "pointer" }}>
                <input
                  type="radio"
                  name={questionItem.id}
                  value={option.value}
                  checked={answers[questionItem.id] === option.value}
                  onChange={() => handleSelect(questionItem.id, option.value)}
                  style={{ marginRight: 10 }}
                />
                {option.label}
              </label>
            ))}
          </div>

          {index === currentStep && (
            <div style={{ marginTop: 14, display: "flex", gap: 10 }}>
              {currentStep > 0 && (
                <button
                  type="button"
                  onClick={() => setCurrentStep((prev) => prev - 1)}
                  style={{
                    padding: "10px 16px",
                    borderRadius: 8,
                    border: "none",
                    background: "#475569",
                    color: "white",
                    cursor: "pointer",
                  }}
                >
                  Back
                </button>
              )}

              <button
                type="button"
                onClick={() => {
                  if (!answers[questionItem.id]) {
                    setError("Please choose an option before moving on.")
                    return
                  }
                  if (currentStep < styleQuizQuestions.length - 1) {
                    setCurrentStep((prev) => prev + 1)
                  } else {
                    handleSubmit()
                  }
                }}
                style={{
                  padding: "10px 16px",
                  borderRadius: 8,
                  border: "none",
                  background: "#22c55e",
                  color: "black",
                  cursor: "pointer",
                }}
              >
                {currentStep < styleQuizQuestions.length - 1 ? "Next" : loading ? "Submitting..." : "Submit Quiz"}
              </button>
            </div>
          )}
        </div>
      ))}

      {error && (
        <p style={{ color: "#f87171", marginTop: 0, marginBottom: 16 }}>{error}</p>
      )}

      {result && (
        <div style={{ background: "#0f172a", padding: 20, borderRadius: 16, border: "1px solid #334155" }}>
          <h4 style={{ marginTop: 0 }}>Your Style Profile</h4>
          <p style={{ margin: "8px 0" }}>
            <strong>Archetypes:</strong> {result.archetypes.join(" / ")}
          </p>
          <p style={{ margin: "8px 0" }}>
            <strong>Style tags:</strong> {result.style_tags.join(", ")}
          </p>
          <p style={{ margin: "8px 0", color: "#94a3b8" }}>
            The quiz result is now ready to generate your outfit.
          </p>
        </div>
      )}

      {selectedTags.length > 0 && (
        <div style={{ marginTop: 16 }}>
          <p style={{ margin: 0, color: "#94a3b8" }}>Current active style tags:</p>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginTop: 8 }}>
            {selectedTags.map((tag) => (
              <span
                key={tag}
                style={{
                  background: "#334155",
                  padding: "6px 10px",
                  borderRadius: 999,
                  fontSize: 12,
                }}
              >
                {tag}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
