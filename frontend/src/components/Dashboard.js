// frontend/prompt-optimizer/src/components/Dashboard.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import OptimizePrompt from './OptimizePrompt';

function Dashboard({ token }) {
  const [prompts, setPrompts] = useState([]);
  const [message, setMessage] = useState('');

  const fetchPrompts = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/prompts/', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      setPrompts(response.data);
    } catch (error) {
      setMessage('Failed to fetch prompts');
    }
  };

  useEffect(() => {
    fetchPrompts();
    // eslint-disable-next-line
  }, []);

  return (
    <div>
      <h2>Your Prompts</h2>
      <OptimizePrompt token={token} onPromptCreated={fetchPrompts} />
      {message && <p>{message}</p>}
      <ul>
        {prompts.map((prompt) => (
          <li key={prompt.id}>
            <strong>Original:</strong> {prompt.original_text}
            <br />
            <strong>Optimized:</strong> {prompt.optimized_text}
            <br />
            <em>Created at: {new Date(prompt.created_at).toLocaleString()}</em>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Dashboard;
