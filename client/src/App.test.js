import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from './App';

test('renders send button', () => {
  render(<App />);
  const sendButton = screen.getByText(/send/i);
  expect(sendButton).toBeInTheDocument();
});
