import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App.jsx';

test('renders Fewfinder app', () => {
  render(<App />);
  // Check that at least one element with the text 'fewfinder' is present
  const matches = screen.getAllByText(/fewfinder/i);
  expect(matches.length).toBeGreaterThan(0);
}); 