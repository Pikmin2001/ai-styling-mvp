import { createFileRoute } from "@tanstack/react-router"
import { useState } from "react"
import { StyleQuiz } from "@/components/StyleQuiz"
import { OutfitSwipeDeck } from "@/components/OutfitSwipeDeck"

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000"

type QuizProfile = {
  archetypes: string[]
  style_tags: string[]
  query_styles: string[]
}

export const Route = createFileRoute("/")({
  component: Home,
})

function Home() {
  const [outfit, setOutfit] = useState<any>(null)
  const [gender, setGender] = useState("")
  const [maxPrice, setMaxPrice] = useState("")
  const [shareUrl, setShareUrl] = useState("")
  const [styles, setStyles] = useState<string[]>([])
  const [quizProfile, setQuizProfile] = useState<QuizProfile | null>(null)
  const [likedOutfits, setLikedOutfits] = useState<any[]>([])
  const [selectedOutfit, setSelectedOutfit] = useState<any | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [swapping, setSwapping] = useState<string | null>(null)

  function handleQuizComplete(result: QuizProfile) {
    setQuizProfile(result)
    setStyles(result.style_tags || [])
  }

  function getOutfitExplanation() {
    if (!outfit || !quizProfile) {
      return "This outfit is generated from your selected style profile and budget preferences."
    }

    const primary = quizProfile.archetypes[0]
    const secondary = quizProfile.archetypes[1]
    const tags = quizProfile.style_tags.join(", ")

    return `This outfit was selected to reflect your ${primary} profile${secondary ? ` with a secondary ${secondary} influence` : ""}, using ${tags}.`
  }

  async function generateOutfit() {
    setLoading(true)
    setError(null)
    setShareUrl("")
    try {
      const params = new URLSearchParams()
      if (gender) params.append("gender", gender)
      if (maxPrice) params.append("max_price", maxPrice)
      if (styles.length) params.append("styles", styles.join(","))

      const res = await fetch(`${API_URL}/api/v1/outfits/generate?${params.toString()}`, {
        method: "POST",
      })
      const data = await res.json()
      setOutfit(data)
    } catch (e) {
      setError("Failed to generate outfit")
    } finally {
      setLoading(false)
    }
  }

  function onLikeOutfit() {
    if (!outfit) return
    setLikedOutfits((prev) => [...prev, { ...outfit, archetypes: quizProfile?.archetypes }])
    setSelectedOutfit(outfit)

    if (quizProfile) {
      const nextStyleTags = [...new Set([...(quizProfile.style_tags || []), ...(outfit.styles || [])])]
      setStyles(nextStyleTags)
      setQuizProfile({ ...quizProfile, style_tags: nextStyleTags })
    }

    generateOutfit()
  }

  function onDislikeOutfit() {
    if (!outfit) return
    setOutfit(null)
    generateOutfit()
  }

  function onChooseCurrentOutfit() {
    if (!outfit) return
    setSelectedOutfit(outfit)
  }

  function onSelectLikedOutfit(liked: any) {
    setSelectedOutfit(liked)
    setStyles(liked.styles || [])
  }

async function swapItem(itemType: string) {
  if (!outfit) return

  setSwapping(itemType)

  const res = await fetch(
    `${API_URL}/api/v1/outfits/swap?item_type=${itemType}`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(outfit),
    }
  )

  const data = await res.json()
  setOutfit(data)
  setSwapping(null)
}

async function saveOutfit() {
  if (!outfit) return

  const res = await fetch(`${API_URL}/api/v1/outfits/save`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(outfit),
  })

  const data = await res.json()
  setShareUrl(data.share_url)
}


  return (
    <div
      style={{
        minHeight: "100vh",
        padding: 40,
        background: "#0f172a",
        color: "white",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <div style={{ maxWidth: 900, margin: "0 auto" }}>
        <h1 style={{ fontSize: 36, marginBottom: 8 }}>AI Styling MVP</h1>
        <span
  style={{
    display: "inline-block",
    background: "#334155",
    color: "#cbd5e1",
    padding: "6px 12px",
    borderRadius: 999,
    fontSize: 13,
    marginBottom: 16,
  }}
>
  Personalized retail styling engine
</span>
        <p style={{ color: "#cbd5e1", marginBottom: 32 }}>
          Generate a personalized outfit based on gender, budget, and style preferences.
        </p>

        <div
          style={{
            background: "#1e293b",
            padding: 24,
            borderRadius: 16,
            marginBottom: 24,
          }}
        >
          <h2>Style Quiz</h2>

          <div style={{ marginTop: 16 }}>
            <label>Gender: </label>
            <select value={gender} onChange={(e) => setGender(e.target.value)}>
              <option value="">Any</option>
              <option value="male">Male</option>
              <option value="female">Female</option>
            </select>
          </div>

          <div style={{ marginTop: 16 }}>
            <label>Max Price: </label>
            <input
              type="number"
              value={maxPrice}
              onChange={(e) => setMaxPrice(e.target.value)}
              placeholder="150"
            />
          </div>

          <div style={{ marginTop: 24 }}>
            <StyleQuiz onQuizComplete={handleQuizComplete} selectedTags={styles} />
          </div>

          {quizProfile && (
            <div style={{ marginTop: 20, background: "#111827", padding: 20, borderRadius: 16, border: "1px solid #334155" }}>
              <h3 style={{ marginTop: 0, marginBottom: 10 }}>Aesthetic Profile</h3>
              <p style={{ margin: "8px 0" }}>
                <strong>Primary archetype:</strong> {quizProfile.archetypes[0]}
              </p>
              <p style={{ margin: "8px 0" }}>
                <strong>Secondary archetype:</strong> {quizProfile.archetypes[1] || quizProfile.archetypes[0]}
              </p>
              <p style={{ margin: "8px 0" }}>
                <strong>Style tags:</strong> {quizProfile.style_tags.join(", ")}
              </p>
            </div>
          )}

         <button
  type="button"
  onClick={generateOutfit}
  disabled={loading}
  style={{
    marginTop: 24,
    padding: "10px 18px",
    borderRadius: 8,
    border: "none",
    cursor: "pointer",
    fontWeight: "bold",
    background: "#22c55e",
    color: "black",
    opacity: loading ? 0.6 : 1,
  }}
>
  {loading ? "Generating..." : "Generate Outfit"}
</button>

          <div style={{ marginTop: 24 }}>
            <OutfitSwipeDeck
              outfit={outfit}
              selectedOutfit={selectedOutfit}
              likedOutfits={likedOutfits}
              loading={loading}
              onLike={onLikeOutfit}
              onDislike={onDislikeOutfit}
              onChooseCurrent={onChooseCurrentOutfit}
              onSelectLiked={onSelectLikedOutfit}
            />
          </div>

{error && (
  <p style={{ color: "#f87171", marginTop: 10 }}>
    {error}
  </p>
)}
            
        </div>
{!outfit && !loading && (
  <div style={{ marginTop: 20, color: "#94a3b8" }}>
    Pick your preferences and generate an outfit.
  </div>
)}
{outfit && outfit.styles && (
  <p style={{ marginTop: 10 }}>
    <strong>Styles:</strong> {outfit.styles.join(", ")}
  </p>
)}
        {outfit && (
          <div
            style={{
              background: "#1e293b",
              padding: 24,
              borderRadius: 16,
            }}
          >
            <h2>Your Outfit</h2>

            <div
              style={{
                background: "#111827",
                padding: 16,
                borderRadius: 12,
                marginBottom: 20,
                color: "#e2e8f0",
              }}
            >
              <p style={{ margin: 0, lineHeight: 1.7 }}>{getOutfitExplanation()}</p>
            </div>

            <div
              style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
                gap: 16,
                marginTop: 16,
              }}
            >
              {[
                ["Top", outfit.top],
                ["Bottom", outfit.bottom],
                ["Shoes", outfit.shoes],
              ].map(([label, item]: any) => (
                <div
                  key={label}
                  style={{
                    background: "#1f2937",
                    boxShadow: "0 4px 20px rgba(0,0,0,0.3)",
                    padding: 18,
                    borderRadius: 12,
                    transition: "transform 0.2s ease, box-shadow 0.2s ease",
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.transform = "translateY(-4px)"
                    e.currentTarget.style.boxShadow = "0 8px 30px rgba(0,0,0,0.45)"
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.transform = "translateY(0)"
                    e.currentTarget.style.boxShadow = "0 4px 20px rgba(0,0,0,0.3)"
}}
                >
                  <h3>{label}</h3>



<div
  style={{
    width: "100%",
    height: 150,
    borderRadius: 8,
    overflow: "hidden",
    background: "#111827",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    marginBottom: 10,
    padding: 8,
  }}
>
  <img
    src={item.image_url || "https://via.placeholder.com/300x200?text=No+Image"}
    alt={item.name}
    style={{
      width: "100%",
      height: "100%",
      objectFit: "contain",
      objectPosition: "center",
    }}
  />
</div>

<p style={{ fontSize: 18, fontWeight: "bold" }}>{item.name}</p>
                  <p>${item.price}</p>
                  <p>Color: {item.color ?? "N/A"}</p>

                  <div>
                    {item.style_tags?.map((tag: string) => (
                      <span
                        key={tag}
                        style={{
                          display: "inline-block",
                          background: "#475569",
                          padding: "4px 8px",
                          borderRadius: 999,
                          marginRight: 6,
                          marginTop: 6,
                          fontSize: 12,
                        }}
                      >
                        {tag}
                      </span>
                    ))}
                  </div>

                 <button
  type="button"
  onClick={() => swapItem(label.toLowerCase())}
  disabled={swapping === label.toLowerCase()}
  style={{
    marginTop: 14,
    padding: "8px 12px",
    borderRadius: 8,
    border: "none",
    cursor: "pointer",
    background: "#38bdf8",
    color: "#0f172a",
    fontWeight: "bold",
    opacity: swapping === label.toLowerCase() ? 0.6 : 1,
  }}
>
  {swapping === label.toLowerCase() ? "Swapping..." : `Swap ${label}`}
</button>
                </div>
              ))}
            </div>

            <h2 style={{ marginTop: 24 }}>Total: ${outfit.total_price}</h2>

            <button
              type="button"
              onClick={saveOutfit}
              style={{
                marginTop: 12,
                padding: "10px 18px",
                borderRadius: 8,
                border: "none",
                cursor: "pointer",
                fontWeight: "bold",
                background: "#22c55e",
                color: "black",
              }}
            >
              Save Outfit
            </button>
          </div>
        )}

        {shareUrl && (
          <div
            style={{
              background: "#064e3b",
              padding: 18,
              borderRadius: 12,
              marginTop: 24,
            }}
          >
            <strong>Share Link: </strong>
            <a href={shareUrl} target="_blank" rel="noreferrer" style={{ color: "#a7f3d0" }}>
              {shareUrl}
            </a>
          </div>
        )}
      </div>
    </div>
  )

    

  }



