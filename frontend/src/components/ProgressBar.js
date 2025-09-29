import React from 'react';
import './ProgressBar.css';

const ProgressBar = ({ progress, message, isVisible }) => {
  if (!isVisible) return null;

  return (
    <div className="progress-container">
      <div className="progress-header">
        <h3>Procesando ecuación...</h3>
        <span className="progress-percentage">{progress}%</span>
      </div>
      

      
      <div className="progress-message">
        <p>{message}</p>
      </div>
      
      <div className="progress-dots">
        <div className={`dot ${progress >= 25 ? 'active' : ''}`}></div>
        <div className={`dot ${progress >= 50 ? 'active' : ''}`}></div>
        <div className={`dot ${progress >= 75 ? 'active' : ''}`}></div>
        <div className={`dot ${progress >= 100 ? 'active' : ''}`}></div>
      </div>
    </div>
  );
};

export default ProgressBar;
