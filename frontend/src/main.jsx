/**
 * Application Entry Point
 */

import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import { AppProvider } from './contexts/AppContext.jsx'; // ADDED

// Global styles
import './styles/variables.css';
import './styles/global.css';
import './styles/animations.css';

// FIXED: Wrap App with AppProvider
ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <AppProvider>
            <App />
        </AppProvider>
    </React.StrictMode>
);
