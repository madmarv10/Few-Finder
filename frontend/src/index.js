import React, { useState } from "react";
import SearchBar from "./components/SearchBar";
import ResultCard from "./components/ResultCard";

function App() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (query) => {
    setLoading(true);
    setResults([]);

    try {
      const response = await fetch("http://localhost:8000/search", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query }),
      });

      const data = await response.json();
      setResults(data.results || []);
    } catch (error) {
      console.error("Error during search:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: "720px", margin: "2rem auto", padding: "0 1rem" }}>
      <h1>🎯 Fewfinder</h1>
      <p>Ask a question like “How long do cats live?” and get the exact YouTube answer.</p>
      <SearchBar onSearch={handleSearch} />
      {loading && <p>Loading...</p>}
      {results.length > 0 &&
        results.map((item) => (
          <ResultCard
            key={item.id}
            videoId={item.video_id}
            title={item.title}
            snippet={item.text}
            start={item.start}
          />
        ))}
    </div>
  );
}

export default App;
