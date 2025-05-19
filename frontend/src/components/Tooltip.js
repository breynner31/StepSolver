import React from 'react';

export default function Tooltip({ text, label = "Información" }) {
  return (
    <div className="tooltip-container" aria-label={label} style={{ position: 'relative', display: 'inline-block' }}>
      <span className="question-icon">?</span>
      <div className="tooltip-text">{text}</div>
    </div>
  );
}
