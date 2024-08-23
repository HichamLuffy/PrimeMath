import React from 'react';
import '../styles/LoadingIndicator.css';

function LoadingIndicator() {
  return (
    <div className="spinner-container">
      <div className="loading-spinner"></div>
      <p>Loading...</p>
    </div>
  );
}

export default LoadingIndicator;
