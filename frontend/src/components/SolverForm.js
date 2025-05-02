import React, { useState } from 'react';

function sanitizeEquation(equation) {
  return equation
    .replace(/−/g, "-")    // signo menos Unicode
    .replace(/∗/g, "*")    // asterisco Unicode
    .replace(/[’‘]/g, "'") // comillas curvas a simples
    .replace(/[“”]/g, '"') // comillas dobles curvas
    .replace(/\s+/g, ' ')  // espacios múltiples a uno solo (opcional)
    .replace(/\^/g, '**')  // Reemplaza '^' por '**' para potencias
    .replace(/dy\/dx/g, "Derivative(y(x), x)")  // Asegúrate de que la derivada sea correcta
    .trim();               // quitar espacios iniciales/finales
}




export default function SolverForm({ onSolve, loading }) {
  const [equation, setEquation] = useState('');
  const [varX, setVarX] = useState('x');
  const [varY, setVarY] = useState('y');
  const [x0, setX0] = useState('');
  const [y0, setY0] = useState('');
  const [dy0, setDy0] = useState('');

  function parseDerivatives(equation, varY, varX) {
    return equation
      .replace(new RegExp(`${varY}''`, 'g'), `Derivative(${varY},${varX},2)`)
      .replace(new RegExp(`${varY}'`, 'g'), `Derivative(${varY},${varX})`);
  }
  

  const handleSubmit = (e) => {
    e.preventDefault();
  
    const sanitizedInput = sanitizeEquation(equation); // 👈 Limpieza aquí
    const parsedEquation = parseDerivatives(sanitizedInput, varY, varX);
    console.log("Ecuación procesada: ", parsedEquation);
  
    const payload = {
      equations: [parsedEquation],
      variables: [varX, varY],
      initial_conditions:
        x0 && y0
          ? {
              x0: Number(x0),
              y0: Number(y0),
              ...(sanitizedInput.includes(`${varY}''`) || sanitizedInput.includes(`${varY}'`)
                ? { dy0: Number(dy0) || 0 }
                : {}),
            }
          : {},
    };
  
    onSolve(payload);
  };
  

  return (
    <form onSubmit={handleSubmit} aria-labelledby="solve-form">
      <div>
        <label htmlFor="equation">Ecuación (p.ej. y'' - 3y' + 2y = 0)</label>
        <input
          id="equation"
          type="text"
          value={equation}
          onChange={(e) => setEquation(e.target.value)}
          required
          aria-required="true"
        />
      </div>

      <div>
        <label htmlFor="varX">Variable independiente</label>
        <input
          id="varX"
          type="text"
          value={varX}
          onChange={(e) => setVarX(e.target.value)}
          required
          aria-required="true"
        />
      </div>

      <div>
        <label htmlFor="varY">Función dependiente</label>
        <input
          id="varY"
          type="text"
          value={varY}
          onChange={(e) => setVarY(e.target.value)}
          required
          aria-required="true"
        />
      </div>

      <fieldset>
        <legend>Condiciones iniciales (opcionales)</legend>

        <label htmlFor="x0">x₀</label>
        <input
          id="x0"
          type="number"
          value={x0}
          onChange={(e) => setX0(e.target.value)}
        />

        <label htmlFor="y0">{varY}({x0 || 'x₀'})</label>
        <input
          id="y0"
          type="number"
          value={y0}
          onChange={(e) => setY0(e.target.value)}
        />

        {(equation.includes(`${varY}''`) || equation.includes(`${varY}'`)) && (
          <>
            <label htmlFor="dy0">{varY}'({x0 || 'x₀'})</label>
            <input
              id="dy0"
              type="number"
              value={dy0}
              onChange={(e) => setDy0(e.target.value)}
            />
          </>
        )}
      </fieldset>

      <button type="submit" disabled={loading} aria-busy={loading}>
        {loading ? 'Calculando…' : 'Resolver'}
      </button>
    </form>
  );
}
