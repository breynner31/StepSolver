import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import SolverForm from './components/SolverForm';
import StepsDisplay from './components/StepsDisplay';
import AudioPlayer from './components/AudioPlayer';
import Tooltip from './components/Tooltip';
import ProgressBar from './components/ProgressBar';
import './App.css';

export default function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [theme, setTheme] = useState('');
  const [progress, setProgress] = useState({ percentage: 0, message: '', isVisible: false });
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    document.body.className = '';
    if (theme) {
      document.body.classList.add(theme);
    }
  }, [theme]);

  // Configurar WebSocket
  useEffect(() => {
    const newSocket = io('http://localhost:5000');
    
    newSocket.on('connect', () => {
      console.log('Conectado al servidor de progreso');
    });

    newSocket.on('progress', (data) => {
      setProgress({
        percentage: data.percentage,
        message: data.message,
        isVisible: true
      });
    });

    newSocket.on('status', (data) => {
      console.log('Estado del servidor:', data.message);
    });

    setSocket(newSocket);

    return () => {
      newSocket.close();
    };
  }, []);

  const handleSolve = async (payload) => {
    setLoading(true);
    setProgress({ percentage: 0, message: 'Iniciando...', isVisible: true });
    setResult(null); // Limpiar resultado anterior
    
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
      // Ocultar barra de progreso después de un breve delay
      setTimeout(() => {
        setProgress(prev => ({ ...prev, isVisible: false }));
      }, 1000);
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

      <ProgressBar 
        progress={progress.percentage} 
        message={progress.message} 
        isVisible={progress.isVisible} 
      />

      {result && (
        <>
          <StepsDisplay steps={result.steps} />
          <AudioPlayer src={result.audio_url} />
        </>
      )}
    </main>
  );
}
