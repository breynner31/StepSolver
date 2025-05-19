import React, { useState, useEffect } from 'react';
import Tooltip from './Tooltip'; // Asegúrate que la ruta es correcta

// Limpia y normaliza la ecuación
function sanitizeEquation(equation) {
  return equation
    .replace(/−/g, "-")
    .replace(/∗/g, "*")
    .replace(/[""]/g, '"')
    .replace(/\s+/g, ' ')
    .replace(/\^/g, '**')
    .replace(/dy\/dx/g, "Derivative(y(x), x)")
    .trim();
}

// Determina el orden de la ecuación diferencial
function determineOrder(equation) {
  let order = 0;
  const primeMatches = equation.match(/y[']+/g);

  if (primeMatches) {
    primeMatches.forEach(match => {
      const currentOrder = match.split("'").length - 1;
      order = Math.max(order, currentOrder);
    });
  }

  const derivative = equation.match(/d(\d*)y\s*\/\s*dx(\d*)/g);
  if (derivative) {
    derivative.forEach(match => {
      const numerator = match.match(/d(\d*)y/);
      const denominator = match.match(/dx(\d*)/);

      let derivOrder = 1;
      if (numerator && numerator[1]) {
        derivOrder = parseInt(numerator[1]) || 1;
      } else if (denominator && denominator[1]) {
        derivOrder = parseInt(denominator[1]) || 1;
      }

      order = Math.max(order, derivOrder);
    });
  }

  return order;
}

// Reemplaza las derivadas por la notación de SymPy
function parseDerivatives(equation, varY, varX) {
  const maxOrder = 10;
  for (let i = maxOrder; i >= 1; i--) {
    const regex = new RegExp(`${varY}${"'".repeat(i)}`, 'g');
    equation = equation.replace(regex, `Derivative(${varY}(${varX}),${varX},${i})`);
  }
  return equation;
}

export default function SolverForm({ onSolve, loading }) {
  const [equation, setEquation] = useState('');
  const [varX, setVarX] = useState('x');
  const [varY, setVarY] = useState('y');
  const [x0, setX0] = useState('');
  const [y0, setY0] = useState('');
  const [order, setOrder] = useState(0);
  const [conditionValues, setConditionValues] = useState({});

  useEffect(() => {
    if (equation.trim()) {
      const detectedOrder = determineOrder(equation);
      setOrder(detectedOrder);

      const initialValues = {};
      for (let i = 1; i < detectedOrder; i++) {
        initialValues[`d${i}y0`] = '';
      }
      setConditionValues(initialValues);
    } else {
      setOrder(0);
      setConditionValues({});
    }
  }, [equation]);

  const handleConditionChange = (key, value) => {
    setConditionValues(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    const sanitizedInput = sanitizeEquation(equation);
    const parsedEquation = parseDerivatives(sanitizedInput, varY, varX);

    const initial_conditions = {
      x0: parseFloat(x0) || 0,
      y0: parseFloat(y0) || 0
    };

    for (let i = 1; i < order; i++) {
      const value = parseFloat(conditionValues[`d${i}y0`]);
      if (!isNaN(value)) {
        initial_conditions[`d${i}y0`] = value;
      }
    }

    const payload = {
      equations: [parsedEquation],
      variables: [varX, varY],
      initial_conditions,
    };

    onSolve(payload);
  };

  const renderInitialConditions = () => {
    const conditions = [];

    conditions.push(
      <div className="input-tooltip-wrapper" key="y0">
        <label htmlFor="y0">{varY}({x0 || 'x₀'})</label>
        <div className="input-tooltip-wrapper">
          <input
            id="y0"
            type="number"
            value={y0}
            onChange={(e) => setY0(e.target.value)}
          />
          <div className="tooltip-container">
            <span className="question-icon">?</span>
            <span className="tooltip-text">{`Valor inicial de ${varY} en ${x0 || 'x₀'}`}</span>
          </div>
        </div>
      </div>
    );

    for (let i = 1; i < order; i++) {
      const derivativeLabel = i === 1
        ? `${varY}'(${x0 || 'x₀'})`
        : `${varY}${'\''.repeat(i)}(${x0 || 'x₀'})`;

      conditions.push(
        <div className="input-tooltip-wrapper" key={`d${i}y0`}>
          <label htmlFor={`d${i}y0`}>{derivativeLabel}</label>
          <div className="input-tooltip-wrapper">
            <input
              id={`d${i}y0`}
              name={`d${i}y0`}
              type="number"
              value={conditionValues[`d${i}y0`] || ''}
              onChange={(e) => handleConditionChange(`d${i}y0`, e.target.value)}
            />
            <div className="tooltip-container">
              <span className="question-icon">?</span>
              <span className="tooltip-text">{`Valor inicial de la derivada ${derivativeLabel}`}</span>
            </div>
          </div>
        </div>
      );
    }

    return conditions;
  };

  return (
    <form onSubmit={handleSubmit} aria-labelledby="solve-form" className="solver-form">
      <div className="input-tooltip-wrapper">
        <label htmlFor="equation">Ecuación (p.ej. y'' + 3y' - 4y = 0)</label>
        <div className="input-tooltip-wrapper">
          <input
            id="equation"
            type="text"
            value={equation}
            onChange={(e) => setEquation(e.target.value)}
            required
            placeholder="Ejemplo: y'' + 3y' - 4y = 0"
          />
          <div className="tooltip-container">
            <span className="question-icon">?</span>
            <span className="tooltip-text">Escribe la ecuación diferencial aquí</span>
          </div>
        </div>
      </div>

      <div className="input-tooltip-wrapper">
        <label htmlFor="varX">Variable independiente</label>
        <div className="input-tooltip-wrapper">
          <input
            id="varX"
            type="text"
            value={varX}
            onChange={(e) => setVarX(e.target.value)}
            required
          />
          <div className="tooltip-container">
            <span className="question-icon">?</span>
            <span className="tooltip-text">Variable independiente, típicamente 'x'</span>
          </div>
        </div>
      </div>

      <div className="input-tooltip-wrapper">
        <label htmlFor="varY">Función dependiente</label>
        <div className="input-tooltip-wrapper">
          <input
            id="varY"
            type="text"
            value={varY}
            onChange={(e) => setVarY(e.target.value)}
            required
          />
          <div className="tooltip-container">
            <span className="question-icon">?</span>
            <span className="tooltip-text">Función dependiente, típicamente 'y'</span>
          </div>
        </div>
      </div>

      <fieldset>
        <legend>Condiciones iniciales {order > 0 ? `(Ecuación de orden ${order})` : ''}</legend>

        <div className="input-tooltip-wrapper">
          <label htmlFor="x0">x₀</label>
          <div className="input-tooltip-wrapper">
            <input
              id="x0"
              type="number"
              value={x0}
              onChange={(e) => setX0(e.target.value)}
            />
            <div className="tooltip-container">
              <span className="question-icon">?</span>
              <span className="tooltip-text">Punto inicial para la variable independiente</span>
            </div>
          </div>
        </div>

        {renderInitialConditions()}
      </fieldset>

      <button type="submit" disabled={loading}>
        {loading ? 'Calculando…' : 'Resolver'}
      </button>
    </form>
  );
}