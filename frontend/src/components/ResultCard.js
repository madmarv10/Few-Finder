// frontend/src/components/ResultCard.js
import React, { useState } from "react";

export default function ResultCard({ videoId, title, snippet, start, videoUrl }) {
  const [imageError, setImageError] = useState(false);
  const thumbnailUrl = `https://img.youtube.com/vi/${videoId}/hqdefault.jpg`;

  const formatTime = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);
    
    if (hours > 0) {
      return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    return `${minutes}:${secs.toString().padStart(2, '0')}`;
  };

  const handleCardClick = () => {
    if (videoUrl) {
      window.open(videoUrl, "_blank", "noopener,noreferrer");
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      handleCardClick();
    }
  };

  return (
    <div
      className="result-card"
      onClick={handleCardClick}
      onKeyDown={handleKeyDown}
      tabIndex={0}
      role="button"
      aria-label={`Watch video starting at ${formatTime(start)}`}
    >
      <div className="result-thumbnail">
        {!imageError ? (
          <img
            src={thumbnailUrl}
            alt={`Thumbnail for ${title}`}
            onError={() => setImageError(true)}
            className="thumbnail-image"
          />
        ) : (
          <div className="thumbnail-placeholder">
            <span>📺</span>
          </div>
        )}
        <div className="timestamp-overlay">
          {formatTime(start)}
        </div>
      </div>
      
      <div className="result-content">
        <h3 className="result-title">{title}</h3>
        <p className="result-snippet">{snippet}</p>
        <div className="result-meta">
          <span className="result-time">
            Starts at {formatTime(start)}
          </span>
          <span className="result-action">
            Click to watch →
          </span>
        </div>
      </div>
    </div>
  );
}
