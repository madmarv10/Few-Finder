import React, { useState } from "react";
import SearchBar from "./components/SearchBar";
import ResultCard from "./components/ResultCard";
import "./App.css";

function App() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Use environment variable or fallback to localhost
  const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

  const handleSearch = async (query) => {
    setLoading(true);
    setError(null);
    setResults([]);

    try {
      const response = await fetch(`${API_BASE_URL}/api/search`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: query }), // Changed from 'query' to 'question' to match backend
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      // Handle the single result object from backend
      if (data) {
        setResults([{
          id: `${data.video_url}_${data.start_time}`,
          video_id: data.video_url.split('v=')[1]?.split('&')[0] || '',
          title: data.video_url.split('v=')[1]?.split('&')[0] || 'Video',
          text: data.transcript_text,
          start: data.start_time,
          video_url: data.video_url
        }]);
      } else {
        setResults([]);
      }
    } catch (error) {
      console.error("Error during search:", error);
      setError(error.message || "An error occurred while searching. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>🎯 Fewfinder</h1>
        <p>Ask a question like "How long do cats live?" and get the exact YouTube answer.</p>
      </header>
      
      <main className="app-main">
        <SearchBar onSearch={handleSearch} disabled={loading} />
        
        {loading && (
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <p>Searching for answers...</p>
          </div>
        )}
        
        {error && (
          <div className="error-container">
            <p className="error-message">⚠️ {error}</p>
            <button 
              className="retry-button"
              onClick={() => setError(null)}
            >
              Try Again
            </button>
          </div>
        )}
        
        {!loading && !error && results.length === 0 && (
          <div className="empty-state">
            <p>Enter a question above to find answers in YouTube videos</p>
          </div>
        )}
        
        {results.length > 0 && (
          <div className="results-container">
            {results.map((item) => (
              <ResultCard
                key={item.id}
                videoId={item.video_id}
                title={item.title}
                snippet={item.text}
                start={item.start}
                videoUrl={item.video_url}
              />
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
