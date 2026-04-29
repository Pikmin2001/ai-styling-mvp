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

  async function generateOutfit() {
    const params = new URLSearchParams()

    if (gender) params.append("gender", gender)
    if (maxPrice) params.append("max_price", maxPrice)

   const res = await fetch(`${API_URL}/api/v1/outfits/generate?${params.toString()}`, {
  method: "POST",
})

    const data = await res.json()
    setOutfit(data)
  }

  async function swapItem(itemType: string) {
  if (!outfit) return

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
    </div>
  )

  

}



