import React from 'react';
import { InlineMath, BlockMath } from 'react-katex';
import 'katex/dist/katex.min.css';

export default function StepsDisplay({ steps }) {
  return (
    <section aria-labelledby="steps-heading" className="steps-section">
      <h2 id="steps-heading" className="heading">Pasos de la solución</h2>

      {steps.map((step, i) => (
        <article key={i} className="step">
          <h3 className="step-title">{step.title}</h3>
          {step.latex_description && <BlockMath>{step.latex_description}</BlockMath>}
        </article>
      ))}
    </section>
  );
}
