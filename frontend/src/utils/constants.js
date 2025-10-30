/**
 * Application Constants
 * Centralized configuration values for the LLM Council Test Generator
 */

// ============================================================================
// APPLICATION PHASES
// ============================================================================

export const APP_PHASES = {
    HERO: 'hero',
    INPUT: 'input',
    GENERATING: 'generating',
};


// Legacy alias for backward compatibility
export const PHASES = APP_PHASES;

// ============================================================================
// PIPELINE STAGES
// ============================================================================

export const PIPELINE_STAGES = [
    { id: 'parsing', label: 'Code Analysis', icon: '🔍' },
    { id: 'generation', label: 'Test Generation', icon: '🤖' },
    { id: 'clustering', label: 'Clustering', icon: '🎯' },
    { id: 'synthesis', label: 'Synthesis', icon: '⚡' },
    { id: 'validation', label: 'Validation', icon: '✅' },
    { id: 'finalization', label: 'Finalization', icon: '🎉' },
];

// Generation stages (for progress tracking)
export const GENERATION_STAGES = {
    INITIALIZATION: 'initialization',
    MODEL_GENERATION: 'model_generation',
    CLUSTERING: 'clustering',
    SYNTHESIS: 'synthesis',
    COMPLETE: 'complete',
};

// Stage status types
export const STAGE_STATUS = {
    PENDING: 'pending',
    ACTIVE: 'active',
    COMPLETE: 'complete',
    ERROR: 'error',
};

// ============================================================================
// SSE EVENTS
// ============================================================================

export const SSE_EVENTS = {
    STAGE: 'stage',
    LLM_OUTPUT: 'llm_output',
    SYNTHESIS_THINKING: 'synthesis_thinking',
    TEST_CASE: 'test_case',
    STATISTICS: 'statistics',
    COVERAGE: 'coverage',
    PROGRESS: 'progress',
    COMPLETE: 'complete',
    ERROR: 'error',
    MESSAGE: 'message',
};

// ============================================================================
// NOTIFICATIONS
// ============================================================================

export const NOTIFICATION_TYPES = {
    SUCCESS: 'success',
    ERROR: 'error',
    WARNING: 'warning',
    INFO: 'info',
};

export const NOTIFICATION_DURATION = {
    SHORT: 2000,
    MEDIUM: 3000,
    LONG: 5000,
    PERSIST: 0, // Don't auto-dismiss
};

// ============================================================================
// CODE EDITOR
// ============================================================================

export const EDITOR_SETTINGS = {
    tabSize: 4,
    lineNumbers: true,
    theme: 'vs-dark',
    minimap: { enabled: false },
    scrollBeyondLastLine: false,
    fontSize: 14,
    fontFamily: "'Fira Code', 'Courier New', monospace",
    automaticLayout: true,
    formatOnPaste: true,
    formatOnType: true,
    wordWrap: 'on',
    renderLineHighlight: 'all',
    scrollbar: {
        vertical: 'visible',
        horizontal: 'visible',
        useShadows: false,
        verticalScrollbarSize: 10,
        horizontalScrollbarSize: 10,
    },
};

export const SUPPORTED_LANGUAGES = {
    PYTHON: 'python',
};

export const CODE_EXAMPLES = {
    python: {
        simple: `def add(a, b):
    """Add two numbers"""
    return a + b

def multiply(a, b):
    """Multiply two numbers"""
    return a * b`,

        medium: `class Calculator:
    """A simple calculator class"""
    
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b
    
    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b`,
    },
};

// ============================================================================
// ANIMATIONS
// ============================================================================

export const ANIMATION_VARIANTS = {
    fadeIn: {
        initial: { opacity: 0 },
        animate: { opacity: 1 },
        exit: { opacity: 0 },
    },
    slideUp: {
        initial: { opacity: 0, y: 20 },
        animate: { opacity: 1, y: 0 },
        exit: { opacity: 0, y: -20 },
    },
    slideDown: {
        initial: { opacity: 0, y: -20 },
        animate: { opacity: 1, y: 0 },
        exit: { opacity: 0, y: 20 },
    },
    scaleIn: {
        initial: { opacity: 0, scale: 0.9 },
        animate: { opacity: 1, scale: 1 },
        exit: { opacity: 0, scale: 0.9 },
    },
    slideInRight: {
        initial: { opacity: 0, x: 100 },
        animate: { opacity: 1, x: 0 },
        exit: { opacity: 0, x: -100 },
    },
    slideInLeft: {
        initial: { opacity: 0, x: -100 },
        animate: { opacity: 1, x: 0 },
        exit: { opacity: 0, x: 100 },
    },
};

export const TRANSITIONS = {
    spring: {
        type: 'spring',
        stiffness: 300,
        damping: 30,
    },
    smooth: {
        duration: 0.3,
        ease: 'easeInOut',
    },
    fast: {
        duration: 0.15,
        ease: 'easeOut',
    },
    slow: {
        duration: 0.5,
        ease: 'easeInOut',
    },
};

export const ANIMATION_DURATION = {
    FAST: 200,
    NORMAL: 300,
    SLOW: 500,
};

// ============================================================================
// TIMEOUTS & DELAYS
// ============================================================================

export const TIMEOUTS = {
    NOTIFICATION_AUTO_DISMISS: 5000,
    SSE_RECONNECT_DELAY: 3000,
    API_DEFAULT_TIMEOUT: 30000,
    DEBOUNCE_DELAY: 300,
};

// ============================================================================
// API
// ============================================================================

export const API_ENDPOINTS = {
    CONFIG: '/api/config',
    GENERATE: '/api/generate',
    HEALTH: '/api/health',
};

// ============================================================================
// STORAGE
// ============================================================================

export const STORAGE_KEYS = {
    LAST_CODE: 'llm_council_last_code',
    LAST_LANGUAGE: 'llm_council_last_language',
    SELECTED_MODELS: 'llm_council_selected_models',
    SELECTED_ROLES: 'llm_council_selected_roles',
    THEME: 'llm_council_theme',
};

// ============================================================================
// MESSAGES
// ============================================================================

export const ERROR_MESSAGES = {
    NETWORK_ERROR: 'Network error. Please check your connection.',
    SERVER_ERROR: 'Server error. Please try again later.',
    VALIDATION_ERROR: 'Please check your input and try again.',
    TIMEOUT_ERROR: 'Request timed out. Please try again.',
    UNKNOWN_ERROR: 'An unexpected error occurred.',
};

export const SUCCESS_MESSAGES = {
    GENERATION_COMPLETE: 'Test suite generated successfully!',
    CONFIG_LOADED: 'Configuration loaded successfully.',
    CODE_SAVED: 'Code saved to local storage.',
};

// ============================================================================
// RESPONSIVE BREAKPOINTS
// ============================================================================

export const BREAKPOINTS = {
    MOBILE: 640,
    TABLET: 768,
    DESKTOP: 1024,
    WIDE: 1280,
};

// ============================================================================
// FEATURE FLAGS
// ============================================================================

export const FEATURES = {
    ENABLE_EXAMPLES: true,
    ENABLE_CODE_HINTS: true,
    ENABLE_EXPORT: true,
    ENABLE_THEME_TOGGLE: false, // Coming soon
};

// ============================================================================
// DEFAULT EXPORT (for convenience)
// ============================================================================

export default {
    APP_PHASES,
    PHASES,
    PIPELINE_STAGES,
    GENERATION_STAGES,
    STAGE_STATUS,
    SSE_EVENTS,
    NOTIFICATION_TYPES,
    NOTIFICATION_DURATION,
    EDITOR_SETTINGS,
    SUPPORTED_LANGUAGES,
    CODE_EXAMPLES,
    ANIMATION_VARIANTS,
    TRANSITIONS,
    ANIMATION_DURATION,
    TIMEOUTS,
    API_ENDPOINTS,
    STORAGE_KEYS,
    ERROR_MESSAGES,
    SUCCESS_MESSAGES,
    BREAKPOINTS,
    FEATURES,
};
