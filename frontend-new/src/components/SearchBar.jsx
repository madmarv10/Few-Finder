// frontend/src/components/SearchBar.js
import React, { useState, useCallback } from "react";
import { debounce } from "lodash";

export default function SearchBar({ onSearch, disabled = false }) {
  const [query, setQuery] = useState("");
  const [isValid, setIsValid] = useState(true);

  // Debounced search to prevent excessive API calls
  const debouncedSearch = useCallback(
    debounce((searchQuery) => {
      if (searchQuery.trim().length >= 3) {
        onSearch(searchQuery.trim());
      }
    }, 500),
    [onSearch]
  );

  const handleInputChange = (e) => {
    const value = e.target.value;
    setQuery(value);
    
    // Validate input
    const isValidInput = value.trim().length >= 3 || value.length === 0;
    setIsValid(isValidInput);
    
    // Clear previous debounced call and set new one
    debouncedSearch.cancel();
    if (value.trim().length >= 3) {
      debouncedSearch(value);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim().length >= 3 && !disabled) {
      onSearch(query.trim());
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && query.trim().length < 3) {
      e.preventDefault();
      setIsValid(false);
    }
  };

  return (
    <div className="search-container">
      <form onSubmit={handleSubmit} className="search-form">
        <div className="search-input-wrapper">
          <input
            type="text"
            placeholder="Ask a question (minimum 3 characters)..."
            value={query}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            disabled={disabled}
            aria-label="Search for answers in YouTube videos"
            aria-describedby={!isValid ? "search-error" : undefined}
            className={`search-input ${!isValid ? 'search-input-error' : ''}`}
          />
          <button
            type="submit"
            disabled={disabled || query.trim().length < 3}
            className="search-button"
            aria-label="Search"
          >
            🔍
          </button>
        </div>
        {!isValid && (
          <p id="search-error" className="search-error">
            Please enter at least 3 characters to search
          </p>
        )}
        {query.trim().length > 0 && query.trim().length < 3 && (
          <p className="search-hint">
            Type at least {3 - query.trim().length} more character{3 - query.trim().length !== 1 ? 's' : ''}
          </p>
        )}
      </form>
    </div>
  );
}
