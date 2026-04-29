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

      {outfit && <pre>{JSON.stringify(outfit, null, 2)}</pre>}
    </div>
  )
}