// frontend/prompt-optimizer/src/App.js
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Register from './components/Register';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import { jwtDecode } from 'jwt-decode'; // Updated import

function App() {
  const [auth, setAuth] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        const decoded = jwtDecode(token);
        const currentTime = Date.now() / 1000;
        if (decoded.exp < currentTime) {
          localStorage.removeItem('token');
          setAuth(false);
        } else {
          setAuth(true);
        }
      } catch (e) {
        localStorage.removeItem('token');
        setAuth(false);
      }
    }
  }, []);

  return (
    <Router>
      <div>
        <h1>Prompt Optimization App</h1>
        <Routes>
          <Route path="/register" element={!auth ? <Register /> : <Navigate to="/dashboard" />} />
          <Route path="/login" element={!auth ? <Login setAuth={setAuth} /> : <Navigate to="/dashboard" />} />
          <Route path="/dashboard" element={auth ? <Dashboard token={localStorage.getItem('token')} /> : <Navigate to="/login" />} />
          <Route path="*" element={<Navigate to="/login" />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
