// frontend/src/components/ResultCard.js
import React from "react";

export default function ResultCard({ videoId, title, snippet, start }) {
  const videoUrl = `https://www.youtube.com/watch?v=${videoId}&t=${Math.floor(start)}s`;
  const thumbnailUrl = `https://img.youtube.com/vi/${videoId}/hqdefault.jpg`;

  return (
    <div
      style={{
        border: "1px solid #ddd",
        borderRadius: "8px",
        padding: "1rem",
        marginBottom: "1rem",
        display: "flex",
        cursor: "pointer",
        maxWidth: "600px",
      }}
      onClick={() => window.open(videoUrl, "_blank")}
    >
      <img
        src={thumbnailUrl}
        alt={title}
        style={{ width: "120px", height: "90px", borderRadius: "4px", marginRight: "1rem" }}
      />
      <div>
        <h3 style={{ margin: "0 0 0.5rem 0" }}>{title}</h3>
        <p style={{ margin: 0, color: "#555" }}>{snippet}</p>
        <small style={{ color: "#999" }}>
          Starts at {new Date(start * 1000).toISOString().substr(11, 8)}
        </small>
      </div>
    </div>
  );
}
