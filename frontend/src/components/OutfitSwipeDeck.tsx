type OutfitSwipeDeckProps = {
  outfit: any | null
  selectedOutfit: any | null
  likedOutfits: any[]
  loading: boolean
  onLike: () => void
  onDislike: () => void
  onChooseCurrent: () => void
  onSelectLiked: (outfit: any) => void
}

export function OutfitSwipeDeck({
  outfit,
  selectedOutfit,
  likedOutfits,
  loading,
  onLike,
  onDislike,
  onChooseCurrent,
  onSelectLiked,
}: OutfitSwipeDeckProps) {
  if (!outfit) {
    return (
      <div style={{ color: "#cbd5e1", padding: 20, borderRadius: 16, background: "#0f172a" }}>
        Generate your first outfit from the quiz to begin swiping.
      </div>
    )
  }

  return (
    <div style={{ display: "grid", gap: 24 }}>
      <div
        style={{
          position: "relative",
          background: "#1f2937",
          borderRadius: 24,
          padding: 24,
          boxShadow: "0 16px 40px rgba(0,0,0,0.35)",
          overflow: "hidden",
        }}
      >
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: 16, marginBottom: 18 }}>
          <div>
            <p style={{ margin: 0, color: "#94a3b8" }}>Swipe outfits</p>
            <h3 style={{ margin: 0 }}>Current look</h3>
          </div>
          <div style={{ display: "flex", gap: 10 }}>
            <button
              type="button"
              onClick={onDislike}
              disabled={loading}
              style={{
                padding: "10px 16px",
                borderRadius: 999,
                border: "1px solid #64748b",
                background: "transparent",
                color: "#cbd5e1",
                cursor: "pointer",
              }}
            >
              Dislike
            </button>
            <button
              type="button"
              onClick={onLike}
              disabled={loading}
              style={{
                padding: "10px 16px",
                borderRadius: 999,
                border: "none",
                background: "#22c55e",
                color: "black",
                cursor: "pointer",
              }}
            >
              {loading ? "Loading…" : "Like"}
            </button>
          </div>
        </div>

        <div style={{ display: "grid", gap: 14 }}>
          <div
            style={{
              width: "100%",
              minHeight: 320,
              borderRadius: 20,
              overflow: "hidden",
              background: "linear-gradient(135deg, #334155 0%, #0f172a 100%)",
              padding: 12,
            }}
          >
            <div style={{ display: "grid", gap: 12, gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))" }}>
              {[{ label: "Top", item: outfit.top }, { label: "Bottom", item: outfit.bottom }, { label: "Shoes", item: outfit.shoes }].map(({ label, item }) => (
                <div key={label} style={{ display: "grid", gap: 8 }}>
                  <div
                    style={{
                      height: 180,
                      borderRadius: 16,
                      overflow: "hidden",
                      background: "#fff",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      padding: 8,
                    }}
                  >
                    <img
                      src={item?.image_url || "https://via.placeholder.com/320x220?text=No+Image"}
                      alt={item?.name || `${label} preview`}
                      style={{
                        width: "100%",
                        height: "100%",
                        objectFit: "contain",
                        objectPosition: "center",
                      }}
                    />
                  </div>
                  <div>
                    <h4 style={{ margin: 0, fontSize: 14 }}>{item?.name || `${label} placeholder`}</h4>
                    <p style={{ margin: "4px 0 0", color: "#94a3b8", fontSize: 12 }}>{label}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div style={{ display: "grid", gap: 10 }}>
            <div>
              <h4 style={{ margin: 0 }}>{outfit.top?.name}</h4>
              <p style={{ margin: "4px 0 0", color: "#94a3b8" }}>Top</p>
            </div>
            <div>
              <h4 style={{ margin: 0 }}>{outfit.bottom?.name}</h4>
              <p style={{ margin: "4px 0 0", color: "#94a3b8" }}>Bottom</p>
            </div>
            <div>
              <h4 style={{ margin: 0 }}>{outfit.shoes?.name}</h4>
              <p style={{ margin: "4px 0 0", color: "#94a3b8" }}>Shoes</p>
            </div>
            <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
              {(outfit.styles || outfit.top?.style_tags || []).map((tag: string) => (
                <span
                  key={tag}
                  style={{
                    display: "inline-block",
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
            <button
              type="button"
              onClick={onChooseCurrent}
              style={{
                marginTop: 10,
                padding: "10px 18px",
                borderRadius: 8,
                border: "none",
                background: "#2563eb",
                color: "white",
                cursor: "pointer",
              }}
            >
              Choose this outfit
            </button>
          </div>
        </div>
      </div>

      {likedOutfits.length > 0 && (
        <div style={{ background: "#0f172a", borderRadius: 20, padding: 20 }}>
          <h4 style={{ marginTop: 0, marginBottom: 14 }}>Liked outfits</h4>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))", gap: 14 }}>
            {likedOutfits.map((liked) => (
              <div key={liked.total_price + liked.top?.id} style={{ background: "#111827", borderRadius: 16, padding: 14 }}>
                <div
                  style={{
                    height: 120,
                    marginBottom: 10,
                    overflow: "hidden",
                    borderRadius: 12,
                    background: "#1f2937",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    padding: 8,
                  }}
                >
                  <img
                    src={liked.top?.image_url || "https://via.placeholder.com/300x200?text=No+Image"}
                    alt={liked.top?.name}
                    style={{ width: "100%", height: "100%", objectFit: "contain", objectPosition: "center" }}
                  />
                </div>
                <p style={{ margin: 0, fontSize: 13 }}>{liked.archetypes?.join(" / ") ?? "Liked outfit"}</p>
                <button
                  type="button"
                  onClick={() => onSelectLiked(liked)}
                  style={{
                    marginTop: 10,
                    width: "100%",
                    padding: "8px 12px",
                    borderRadius: 8,
                    border: "none",
                    background: "#22c55e",
                    color: "black",
                    cursor: "pointer",
                  }}
                >
                  Use this outfit
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {selectedOutfit && (
        <div style={{ background: "#111827", borderRadius: 20, padding: 20, border: "1px solid #334155" }}>
          <h4 style={{ marginTop: 0, marginBottom: 14 }}>Selected outfit</h4>
          <div style={{ display: "grid", gap: 10 }}>
            <p style={{ margin: 0, color: "#94a3b8" }}>You have selected this outfit as your preferred look.</p>
            <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
              {selectedOutfit.styles?.map((tag: string) => (
                <span
                  key={tag}
                  style={{
                    display: "inline-block",
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
        </div>
      )}
    </div>
  )
}
