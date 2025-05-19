import React, { useState, useEffect } from 'react';
import SolverForm from './components/SolverForm';
import StepsDisplay from './components/StepsDisplay';
import AudioPlayer from './components/AudioPlayer';
import Tooltip from './components/Tooltip';
import './App.css';

export default function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [theme, setTheme] = useState('');

  useEffect(() => {
    document.body.className = '';
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
        <div className="theme-selector-container">
          <label htmlFor="theme-select" className="theme-label">Modo accesible:</label>
          <div className="theme-select-wrapper">
            <select
              id="theme-select"
              onChange={(e) => setTheme(e.target.value)}
              value={theme}
              className="theme-select"
            >
              <option value="">Normal</option>
              <option value="theme-yellow-on-black">Amarillo sobre negro (Alto contraste)</option>
              <option value="theme-blue-on-white">Azul oscuro sobre blanco</option>
              <option value="theme-pink-on-gray">Rosa sobre gris oscuro</option>
              <option value="theme-green-on-black">Verde sobre negro</option>
            </select>

            <Tooltip text="Selecciona un modo de contraste para mejorar la accesibilidad visual." label="Información sobre el modo accesible" />

          </div>
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
