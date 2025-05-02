// Componente principal de la aplicación
import React, { useState } from 'react';
import SolverForm from './components/SolverForm';
import StepsDisplay from './components/StepsDisplay';
import AudioPlayer from './components/AudioPlayer';
import './App.css';

export default function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSolve = async (payload) => {
    setLoading(true);
    console.log("Payload enviado:", payload); // Imprime el payload
    try {
      const res = await fetch('/api/solve', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      // Verifica si la respuesta es exitosa
      if (!res.ok) {
        const errorText = await res.text();  // Obtiene HTML o lo que sea
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
      <h1>StepSolver</h1>
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