// frontend/prompt-optimizer/src/components/OptimizePrompt.js
import React, { useState } from 'react';
import axios from 'axios';

function OptimizePrompt({ token, onPromptCreated }) {
  const [originalText, setOriginalText] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        'http://localhost:5000/api/prompts/',
        { original_text: originalText },
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );
      setOriginalText('');
      setMessage('Prompt optimized successfully!');
      onPromptCreated();
    } catch (error) {
      setMessage(error.response?.data?.msg || 'Failed to optimize prompt');
    }
  };

  return (
    <div>
      <h3>Create & Optimize Prompt</h3>
      <form onSubmit={handleSubmit}>
        <textarea
          value={originalText}
          onChange={(e) => setOriginalText(e.target.value)}
          placeholder="Enter your prompt here..."
          rows="4"
          cols="50"
          required
        />
        <br />
        <button type="submit">Optimize Prompt</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
}

export default OptimizePrompt;
