/**
 * AppContext - Global State Management (FIXED)
 */

import { createContext, useContext, useReducer, useCallback } from 'react';
import { useConfig } from '@/hooks/useConfig';
import { APP_PHASES } from '@/utils/constants';

const AppContext = createContext(null);

// Initial state
const initialState = {
    // UI Phase
    currentPhase: APP_PHASES.HERO,

    // Input state
    input: {
        code: '',
        language: 'python',
        selectedModels: [],
        selectedRoles: [],
        isValid: false,
        errors: [],
    },

    // Generation state
    generation: {
        isGenerating: false,
        currentStage: null,
        progress: 0,
        startTime: null,
        endTime: null,
    },

    // Real-time outputs
    modelOutputs: {},

    // Clustering results
    clusters: [],

    // Synthesis
    synthesis: {
        thinking: '',
        deduplicatedTests: [],
        coverage: null,
    },

    // Notifications
    notifications: [],

    // Errors
    error: null,
};

// Action types
const ACTIONS = {
    SET_PHASE: 'SET_PHASE',
    SET_INPUT_CODE: 'SET_INPUT_CODE',
    SET_INPUT_LANGUAGE: 'SET_INPUT_LANGUAGE',
    SET_SELECTED_MODELS: 'SET_SELECTED_MODELS',
    SET_SELECTED_ROLES: 'SET_SELECTED_ROLES',
    VALIDATE_INPUT: 'VALIDATE_INPUT',
    RESET_INPUT: 'RESET_INPUT',
    START_GENERATION: 'START_GENERATION',
    UPDATE_STAGE: 'UPDATE_STAGE',
    UPDATE_PROGRESS: 'UPDATE_PROGRESS',
    COMPLETE_GENERATION: 'COMPLETE_GENERATION',
    CANCEL_GENERATION: 'CANCEL_GENERATION',
    UPDATE_MODEL_THINKING: 'UPDATE_MODEL_THINKING',
    ADD_MODEL_TEST: 'ADD_MODEL_TEST',
    COMPLETE_MODEL_ROLE: 'COMPLETE_MODEL_ROLE',
    UPDATE_CLUSTERS: 'UPDATE_CLUSTERS',
    ADD_CLUSTER: 'ADD_CLUSTER', // ✅ NEW
    UPDATE_CLUSTER: 'UPDATE_CLUSTER', // ✅ NEW
    UPDATE_SYNTHESIS_THINKING: 'UPDATE_SYNTHESIS_THINKING',
    UPDATE_DEDUPLICATED_TESTS: 'UPDATE_DEDUPLICATED_TESTS',
    UPDATE_COVERAGE: 'UPDATE_COVERAGE',
    ADD_NOTIFICATION: 'ADD_NOTIFICATION',
    REMOVE_NOTIFICATION: 'REMOVE_NOTIFICATION',
    CLEAR_NOTIFICATIONS: 'CLEAR_NOTIFICATIONS',
    SET_ERROR: 'SET_ERROR',
    CLEAR_ERROR: 'CLEAR_ERROR',
    RESET_STATE: 'RESET_STATE',
};

// Reducer
function appReducer(state, action) {
    switch (action.type) {
        case ACTIONS.SET_PHASE:
            return {
                ...state,
                currentPhase: action.payload,
            };

        case ACTIONS.SET_INPUT_CODE:
            return {
                ...state,
                input: {
                    ...state.input,
                    code: action.payload,
                },
            };

        case ACTIONS.SET_INPUT_LANGUAGE:
            return {
                ...state,
                input: {
                    ...state.input,
                    language: action.payload,
                },
            };

        case ACTIONS.SET_SELECTED_MODELS:
            return {
                ...state,
                input: {
                    ...state.input,
                    selectedModels: action.payload,
                },
            };

        case ACTIONS.SET_SELECTED_ROLES:
            return {
                ...state,
                input: {
                    ...state.input,
                    selectedRoles: action.payload,
                },
            };

        case ACTIONS.VALIDATE_INPUT: {
            const errors = [];
            const { code, selectedModels, selectedRoles } = state.input;

            if (!code.trim()) {
                errors.push('Code is required');
            }
            if (code.trim().length < 10) {
                errors.push('Code is too short');
            }
            if (selectedModels.length === 0) {
                errors.push('At least one model must be selected');
            }
            if (selectedRoles.length === 0) {
                errors.push('At least one role must be selected');
            }

            return {
                ...state,
                input: {
                    ...state.input,
                    isValid: errors.length === 0,
                    errors,
                },
            };
        }

        case ACTIONS.RESET_INPUT:
            return {
                ...state,
                input: initialState.input,
            };

        case ACTIONS.START_GENERATION:
            return {
                ...state,
                generation: {
                    isGenerating: true,
                    currentStage: 'initialization',
                    progress: 0,
                    startTime: Date.now(),
                    endTime: null,
                },
                modelOutputs: {},
                clusters: [],
                synthesis: initialState.synthesis,
                error: null,
            };

        case ACTIONS.UPDATE_STAGE:
            return {
                ...state,
                generation: {
                    ...state.generation,
                    currentStage: action.payload,
                },
            };

        case ACTIONS.UPDATE_PROGRESS:
            return {
                ...state,
                generation: {
                    ...state.generation,
                    progress: action.payload,
                },
            };

        case ACTIONS.COMPLETE_GENERATION:
            return {
                ...state,
                generation: {
                    ...state.generation,
                    isGenerating: false,
                    currentStage: 'complete',
                    progress: 100,
                    endTime: Date.now(),
                },
            };

        case ACTIONS.CANCEL_GENERATION:
            return {
                ...state,
                generation: {
                    ...initialState.generation,
                    currentStage: 'cancelled',
                },
            };

        case ACTIONS.UPDATE_MODEL_THINKING: {
            const { model, role, thinking } = action.payload;
            const normalizedRole = role || 'default';

            const currentThinking = state.modelOutputs[model]?.[normalizedRole]?.thinking || '';
            const currentTests = state.modelOutputs[model]?.[normalizedRole]?.tests || [];

            return {
                ...state,
                modelOutputs: {
                    ...state.modelOutputs,
                    [model]: {
                        ...state.modelOutputs[model],
                        [normalizedRole]: {
                            thinking: currentThinking + thinking,
                            tests: currentTests,
                            completed: false,
                        },
                    },
                },
            };
        }

        case ACTIONS.ADD_MODEL_TEST: {
            const { model, role, test } = action.payload;
            const currentTests = state.modelOutputs[model]?.[role]?.tests || [];
            return {
                ...state,
                modelOutputs: {
                    ...state.modelOutputs,
                    [model]: {
                        ...state.modelOutputs[model],
                        [role]: {
                            ...state.modelOutputs[model]?.[role],
                            tests: [...currentTests, test],
                        },
                    },
                },
            };
        }

        case ACTIONS.COMPLETE_MODEL_ROLE: {
            const { model, role } = action.payload;
            return {
                ...state,
                modelOutputs: {
                    ...state.modelOutputs,
                    [model]: {
                        ...state.modelOutputs[model],
                        [role]: {
                            ...state.modelOutputs[model]?.[role],
                            completed: true,
                        },
                    },
                },
            };
        }

        case ACTIONS.UPDATE_CLUSTERS:
            return {
                ...state,
                clusters: action.payload,
            };

        // ✅ NEW: Add single cluster
        case ACTIONS.ADD_CLUSTER: {
            const existingCluster = state.clusters.find(c => c.id === action.payload.id);
            if (existingCluster) {
                return state; // Already exists
            }
            return {
                ...state,
                clusters: [...state.clusters, action.payload],
            };
        }

        // ✅ NEW: Update specific cluster
        case ACTIONS.UPDATE_CLUSTER: {
            return {
                ...state,
                clusters: state.clusters.map(cluster =>
                    cluster.id === action.payload.id
                        ? { ...cluster, ...action.payload.updates }
                        : cluster
                ),
            };
        }

        case ACTIONS.UPDATE_SYNTHESIS_THINKING:
            return {
                ...state,
                synthesis: {
                    ...state.synthesis,
                    thinking: (state.synthesis.thinking || '') + action.payload,
                },
            };

        case ACTIONS.UPDATE_DEDUPLICATED_TESTS:
            return {
                ...state,
                synthesis: {
                    ...state.synthesis,
                    deduplicatedTests: action.payload,
                },
            };

        case ACTIONS.UPDATE_COVERAGE:
            return {
                ...state,
                synthesis: {
                    ...state.synthesis,
                    coverage: action.payload,
                },
            };

        case ACTIONS.ADD_NOTIFICATION:
            return {
                ...state,
                notifications: [...state.notifications, action.payload],
            };

        case ACTIONS.REMOVE_NOTIFICATION:
            return {
                ...state,
                notifications: state.notifications.filter(
                    (n) => n.id !== action.payload
                ),
            };

        case ACTIONS.CLEAR_NOTIFICATIONS:
            return {
                ...state,
                notifications: [],
            };

        case ACTIONS.SET_ERROR:
            return {
                ...state,
                error: action.payload,
                generation: {
                    ...state.generation,
                    isGenerating: false,
                },
            };

        case ACTIONS.CLEAR_ERROR:
            return {
                ...state,
                error: null,
            };

        case ACTIONS.RESET_STATE:
            return {
                ...initialState,
                currentPhase: state.currentPhase,
            };

        default:
            return state;
    }
}

// Provider component
export function AppProvider({ children }) {
    const [state, dispatch] = useReducer(appReducer, initialState);
    const { config, loading: configLoading, error: configError } = useConfig();

    const setPhase = useCallback((phase) => {
        dispatch({ type: ACTIONS.SET_PHASE, payload: phase });
    }, []);

    const setInputCode = useCallback((code) => {
        dispatch({ type: ACTIONS.SET_INPUT_CODE, payload: code });
    }, []);

    const setInputLanguage = useCallback((language) => {
        dispatch({ type: ACTIONS.SET_INPUT_LANGUAGE, payload: language });
    }, []);

    const setSelectedModels = useCallback((models) => {
        dispatch({ type: ACTIONS.SET_SELECTED_MODELS, payload: models });
    }, []);

    const setSelectedRoles = useCallback((roles) => {
        dispatch({ type: ACTIONS.SET_SELECTED_ROLES, payload: roles });
    }, []);

    const validateInput = useCallback(() => {
        dispatch({ type: ACTIONS.VALIDATE_INPUT });
    }, []);

    const resetInput = useCallback(() => {
        dispatch({ type: ACTIONS.RESET_INPUT });
    }, []);

    const addNotification = useCallback((notification) => {
        const id = Date.now() + Math.random();
        dispatch({
            type: ACTIONS.ADD_NOTIFICATION,
            payload: { id, ...notification },
        });
        return id;
    }, []);

    const removeNotification = useCallback((id) => {
        dispatch({ type: ACTIONS.REMOVE_NOTIFICATION, payload: id });
    }, []);

    const setError = useCallback((error) => {
        dispatch({ type: ACTIONS.SET_ERROR, payload: error });
    }, []);

    const clearError = useCallback(() => {
        dispatch({ type: ACTIONS.CLEAR_ERROR });
    }, []);

    const value = {
        // Direct state access
        currentPhase: state.currentPhase,
        input: state.input,
        generation: state.generation,
        modelOutputs: state.modelOutputs,
        clusters: state.clusters,
        synthesis: state.synthesis,
        notifications: state.notifications,
        error: state.error,

        // Config
        config,
        configLoading,
        configError,

        // Actions
        setPhase,
        setInputCode,
        setInputLanguage,
        setSelectedModels,
        setSelectedRoles,
        validateInput,
        resetInput,
        addNotification,
        removeNotification,
        setError,
        clearError,

        // Direct dispatch access
        dispatch,
        ACTIONS,
    };

    return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}

export function useApp() {
    const context = useContext(AppContext);
    if (!context) {
        throw new Error('useApp must be used within AppProvider');
    }
    return context;
}
