import React, { useState, useEffect } from 'react';
import SolverForm from './components/SolverForm';
import StepsDisplay from './components/StepsDisplay';
import AudioPlayer from './components/AudioPlayer';
import './App.css';

export default function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [theme, setTheme] = useState('');

  useEffect(() => {
    document.body.className = ''; // Limpia cualquier clase previa
    if (theme) {
      document.body.classList.add(theme);
    }
  }, [theme]);

  const handleSolve = async (payload) => {
    setLoading(true);
    try {
      const res = await fetch('/api/solve', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (!res.ok) {
        const errorText = await res.text();
        console.error("Respuesta no válida del servidor:", errorText);
        throw new Error("Error del servidor");
      }
      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      alert('Error al resolver la ecuación');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="container">
      <div className="top-bar" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1>StepSolver</h1>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <label htmlFor="theme-select" style={{ fontWeight: 'bold' }}>Modo accesible:</label>
          <select
            id="theme-select"
            onChange={(e) => setTheme(e.target.value)}
            value={theme}
          >
            <option value="">Normal</option>
            <option value="theme-yellow-on-black">Amarillo sobre negro (Alto contraste)</option>
            <option value="theme-blue-on-white">Azul oscuro sobre blanco</option>
            <option value="theme-pink-on-gray">Rosa sobre gris oscuro</option>
            <option value="theme-green-on-black">Verde sobre negro</option>
          </select>
        </div>
      </div>

      <SolverForm onSolve={handleSolve} loading={loading} />

      {result && (
        <>
          <StepsDisplay steps={result.steps} />
          <AudioPlayer src={result.audio_url} />
        </>
      )}
    </main>
  );
}
