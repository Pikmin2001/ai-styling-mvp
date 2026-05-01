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

function toggleStyle(e: React.ChangeEvent<HTMLInputElement>) {
  const val = e.target.value
  setStyles((prev) =>
    prev.includes(val) ? prev.filter((s) => s !== val) : [...prev, val],
  )
}

  async function generateOutfit() {
    const params = new URLSearchParams()

    if (gender) params.append("gender", gender)
    if (maxPrice) params.append("max_price", maxPrice)
    if (styles.length) params.append("styles", styles.join(","))
   const res = await fetch(`${API_URL}/api/v1/outfits/generate?${params.toString()}`, {
  method: "POST",
})

    const data = await res.json()
    setOutfit(data)
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
    
    <div style={{ padding: 40 }}>
      <h1>AI Styling MVP</h1>

      <div>
        <label>Gender: </label>
        <select value={gender} onChange={(e) => setGender(e.target.value)}>
          <option value="">Any</option>
          <option value="male">Male</option>
          <option value="female">Female</option>
        </select>
      </div>

      <div style={{ marginTop: 12 }}>
        <label>Max Price: </label>
        <input
          type="number"
          value={maxPrice}
          onChange={(e) => setMaxPrice(e.target.value)}
          placeholder="150"
        />
      </div>

      <div style={{ marginTop: 12 }}>
  <p>Style Preferences:</p>

  <label>
    <input type="checkbox" value="casual" onChange={toggleStyle} /> Casual
  </label>

  <label>
    <input type="checkbox" value="streetwear" onChange={toggleStyle} /> Streetwear
  </label>

  <label>
    <input type="checkbox" value="minimalist" onChange={toggleStyle} /> Minimalist
  </label>

  <label>
    <input type="checkbox" value="formal" onChange={toggleStyle} /> Formal
  </label>
</div>

      <button type="button" onClick={generateOutfit} style={{ marginTop: 16 }}>
        Generate Outfit
      </button>

      {outfit && (
  <div style={{ marginTop: 20 }}>
    <pre>{JSON.stringify(outfit, null, 2)}</pre>

    <div style={{ marginTop: 10 }}>
      <button onClick={() => swapItem("top")}>Swap Top</button>
      <button onClick={() => swapItem("bottom")}>Swap Bottom</button>
      <button onClick={() => swapItem("shoes")}>Swap Shoes</button>
    </div>

    <div style={{ marginTop: 10 }}>
      <button onClick={saveOutfit}>Save Outfit</button>
    </div>
  </div>
)}

  {shareUrl && (
  <p style={{ marginTop: 20 }}>
    Share Link:{" "}
    <a href={shareUrl} target="_blank" rel="noreferrer">
      {shareUrl}
    </a>
  </p>
)}
    </div>
  )

  

}



