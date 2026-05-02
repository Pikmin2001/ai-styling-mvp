import { createFileRoute } from "@tanstack/react-router"
import { useState } from "react"

const API_URL = import.meta.env.VITE_API_URL

export const Route = createFileRoute("/")({
  component: Home,
})

function Home() {
  const [outfit, setOutfit] = useState<any>(null)
  const [gender, setGender] = useState("")
  const [maxPrice, setMaxPrice] = useState("")
  const [shareUrl, setShareUrl] = useState("")
  const [styles, setStyles] = useState<string[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

function toggleStyle(e: React.ChangeEvent<HTMLInputElement>) {
  const val = e.target.value
  setStyles((prev) =>
    prev.includes(val) ? prev.filter((s) => s !== val) : [...prev, val],
  )
}

  async function generateOutfit() {
  setLoading(true)
  setError(null)
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

  async function swapItem(itemType: string) {
  if (!outfit) return

  console.log("Swapping:", itemType)
  console.log("Current outfit:", outfit)

  const res = await fetch(
    `${API_URL}/api/v1/outfits/swap?item_type=${itemType}`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(outfit),
    },
  )

  console.log("Swap status:", res.status)

  const data = await res.json()
  console.log("Swap response:", data)

  setOutfit(data)
  setShareUrl("")
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

          <div style={{ marginTop: 16 }}>
            <p>Style Preferences:</p>

            <div style={{ marginTop: 8 }}>
  {styles.map((s) => (
    <span
      key={s}
      style={{
        background: "#334155",
        padding: "4px 10px",
        borderRadius: 999,
        marginRight: 6,
        fontSize: 12,
      }}
    >
      {s}
    </span>
  ))}
</div>

            {["casual", "streetwear", "minimalist", "formal"].map((style) => (
              <label key={style} style={{ marginRight: 16 }}>
                <input type="checkbox" value={style} onChange={toggleStyle} />{" "}
                {style}
              </label>
            ))}
          </div>

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
                    background: "#334155",
                    padding: 18,
                    borderRadius: 12,
                  }}
                >
                  <h3>{label}</h3>
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
                    style={{
                      marginTop: 14,
                      padding: "8px 12px",
                      borderRadius: 8,
                      border: "none",
                      cursor: "pointer",
                    }}
                  >
                    Swap {label}
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



