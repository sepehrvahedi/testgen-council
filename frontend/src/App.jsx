import { useApp } from '@/contexts/AppContext';
import Hero from '@/components/Hero/Hero';
import CodeInput from '@/components/CodeInput/CodeInput';
import GenerationView from '@/components/Generation/GenerationView';
import NotificationContainer from '@/components/shared/NotificationContainer';
import { APP_PHASES } from '@/utils/constants';
import LoadingSpinner from '@/components/shared/LoadingSpinner';
import './App.css';

function App() {
    const { currentPhase, configLoading, configError, config } = useApp();

    console.log('🎯 App render - Phase:', currentPhase, 'Loading:', configLoading, 'Error:', configError);

    // Show loading spinner while config loads
    if (configLoading) {
        return (
            <div className="app-loading">
                <LoadingSpinner />
                <p style={{ marginTop: '1rem', color: '#666' }}>
                    Loading configuration...
                </p>
            </div>
        );
    }

    // Show error if config failed to load
    if (configError) {
        return (
            <div className="app-error">
                <h2>⚠️ Configuration Error</h2>
                <p>{configError}</p>
                <p style={{ marginTop: '1rem', fontSize: '0.9rem', color: '#666' }}>
                    Using fallback configuration. Some features may be limited.
                </p>
                <button
                    onClick={() => window.location.reload()}
                    style={{ marginTop: '1rem', padding: '0.5rem 1rem' }}
                >
                    Retry
                </button>
            </div>
        );
    }

    // Render based on phase
    return (
        <div className="app">
            <NotificationContainer />
            {currentPhase === APP_PHASES.HERO && <Hero />}
            {currentPhase === APP_PHASES.INPUT && <CodeInput />}
            {currentPhase === APP_PHASES.GENERATING && <GenerationView />}
        </div>
    );
}

export default App;
