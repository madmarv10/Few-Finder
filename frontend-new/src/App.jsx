import React from 'react';
import { useState } from 'react';
import './App.css';
import SearchBar from './components/SearchBar.jsx';
import ResultCard from './components/ResultCard.jsx';

function App() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Helper: Try dynamic_search on each video until one works
  const findBestAnswer = async (q, videoResults) => {
    for (const video of videoResults) {
      try {
        const res = await fetch('/api/dynamic_search', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ question: q, videoId: video.videoId })
        });
        if (res.ok) {
          const data = await res.json();
          return {
            ...data,
            title: video.title,
            videoId: video.videoId,
            description: video.description
          };
        }
      } catch (err) {
        // Try next video
      }
    }
    return null;
  };

  // User submits a question
  const handleSearch = async (q) => {
    setQuestion(q);
    setAnswer(null);
    setError('');
    setLoading(true);
    try {
      const res = await fetch('/api/youtube_search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: q, max_results: 5 })
      });
      if (!res.ok) throw new Error('Failed to search YouTube videos');
      const videoResults = await res.json();
      if (!videoResults.length) throw new Error('No relevant YouTube videos found.');
      const bestAnswer = await findBestAnswer(q, videoResults);
      if (bestAnswer) {
        setAnswer(bestAnswer);
      } else {
        setError('No answer found in the top YouTube videos. Try rephrasing your question!');
      }
    } catch (err) {
      setError('Error: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>Fewfinder</h1>
        <p>Ask a question and Fewfinder will find and play the answer in a YouTube video—instantly.</p>
      </header>
      <main className="app-main">
        <SearchBar onSearch={handleSearch} disabled={loading} />
        {loading && (
          <div className="loading-container">
            <div className="loading-spinner" />
            <span>Loading...</span>
          </div>
        )}
        {error && (
          <div className="error-container">
            <span className="error-message">{error}</span>
            <button className="retry-button" onClick={() => window.location.reload()}>Retry</button>
          </div>
        )}
        {!loading && !error && answer && (
          <div className="results-container">
            <h2>Best Answer Found</h2>
            <ResultCard
              videoId={answer.videoId}
              title={answer.title}
              snippet={answer.transcript_text}
              start={answer.start_time}
              videoUrl={answer.video_url}
            />
            <div style={{ marginTop: '1.5rem' }}>
              <iframe
                width="100%"
                height="360"
                src={`https://www.youtube.com/embed/${answer.videoId}?start=${Math.floor(answer.start_time)}`}
                title={answer.title}
                frameBorder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
              />
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
