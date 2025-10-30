/**
 * useTestGeneration Hook
 * Orchestrates the entire test generation pipeline with SSE streaming
 */

import { useCallback, useRef } from 'react';
import { useApp } from '@/contexts/AppContext';
import { useSSEStream } from '@/hooks/useSSEStream';
import { api } from '@/services/api';

// Helper functions
const extractTestName = (code) => {
    const match = code.match(/def (test_\w+)/);
    return match ? match[1] : 'Unnamed Test';
};

const extractTestDescription = (code) => {
    const match = code.match(/"""(.*?)"""/s) || code.match(/'''(.*?)'''/s);
    return match ? match[1].trim() : 'No description';
};

const getCategoryColor = (category) => {
    const colors = {
        positive: '#10b981',
        negative: '#ef4444',
        boundary: '#f59e0b',
        edge_case: '#6366f1',
        security: '#8b5cf6',
        performance: '#06b6d4',
    };
    return colors[category] || '#6b7280';
};

export function useTestGeneration() {
    const {
        generation,
        input,
        dispatch,
        ACTIONS,
        addNotification,
    } = useApp();

    const { connect, disconnect, SSE_EVENTS } = useSSEStream();
    const unsubscribeRef = useRef(null);
    const abortControllerRef = useRef(null);

    /**
     * Parse and handle SSE events
     */
    const handleSSEEvent = useCallback(
        (event) => {
            console.log('📨 SSE Event received:', event);

            const event_type = event.event_type || event.type;
            const data = event.data;

            if (!event_type) {
                console.error('❌ Invalid SSE event - missing event_type:', event);
                return;
            }

            console.log('📋 Processing event:', { event_type, data });

            switch (event_type) {
                // ========== Pipeline Events ==========
                case 'pipeline_start':
                    console.log('🚀 Pipeline started:', data);
                    dispatch({
                        type: ACTIONS.UPDATE_STAGE,
                        payload: 'generation',
                    });
                    dispatch({
                        type: ACTIONS.UPDATE_PROGRESS,
                        payload: 5,
                    });
                    // addNotification({
                    //     type: 'info',
                    //     message: data.message || `Starting generation for ${data.function_name}`,
                    //     duration: 3000,
                    // });
                    break;

                case 'pipeline_complete':
                    console.log('✅ Pipeline completed:', data);
                    dispatch({ type: ACTIONS.COMPLETE_GENERATION });

                    // addNotification({
                    //     type: 'success',
                    //     message: data.message || 'Test generation completed!',
                    //     duration: 5000,
                    // });

                    setTimeout(() => disconnect(), 100);
                    break;

                // ========== LLM Events ==========
                case 'llm_start':
                    console.log('🤖 LLM started:', data);
                    dispatch({
                        type: ACTIONS.UPDATE_STAGE,
                        payload: 'model_generation',
                    });

                    const progress = ((data.model_index - 1) / data.total_models) * 40 + 10;
                    dispatch({
                        type: ACTIONS.UPDATE_PROGRESS,
                        payload: Math.round(progress),
                    });

                    // addNotification({
                    //     type: 'info',
                    //     message: data.message || `[${data.model_index}/${data.total_models}] ${data.model} as ${data.role || 'default'}`,
                    //     duration: 2000,
                    // });
                    break;

                case 'llm_chunk':
                    if (data.chunk && data.chunk.trim()) {
                        const normalizedRole = data.role || 'default';

                        dispatch({
                            type: ACTIONS.UPDATE_MODEL_THINKING,
                            payload: {
                                model: data.model,
                                role: normalizedRole,
                                thinking: data.chunk,
                            },
                        });
                    }
                    break;

                case 'llm_complete':
                    console.log('✅ LLM completed:', data);

                    const completedRole = data.role || 'default';

                    dispatch({
                        type: ACTIONS.COMPLETE_MODEL_ROLE,
                        payload: {
                            model: data.model,
                            role: completedRole,
                        },
                    });

                    // addNotification({
                    //     type: 'success',
                    //     message: data.message || `${data.model} completed (${data.tests_generated} tests, ${data.duration_seconds}s)`,
                    //     duration: 3000,
                    // });
                    break;

                case 'llm_error':
                    console.error('❌ LLM error:', data);
                    addNotification({
                        type: 'error',
                        message: data.message || 'Model generation failed',
                        duration: 5000,
                    });
                    break;

                // ========== Clustering Events ==========
                case 'clustering_start':
                    console.log('🧩 Clustering started:', data);
                    dispatch({
                        type: ACTIONS.UPDATE_STAGE,
                        payload: 'clustering',
                    });
                    dispatch({
                        type: ACTIONS.UPDATE_PROGRESS,
                        payload: 60,
                    });
                    // addNotification({
                    //     type: 'info',
                    //     message: data.message || 'Clustering tests...',
                    //     duration: 2000,
                    // });
                    break;

                case 'cluster_formed': {
                    console.log('📊 Cluster formed:', data);
                    console.log('📊 Raw tests data:', data.tests);

                    // ✅ Validate and parse each test in the cluster
                    if (!data.tests || !Array.isArray(data.tests)) {
                        console.warn('⚠️ Invalid tests data in cluster:', data);
                        break;
                    }

                    // ✅ Parse each test individually
                    const parsedTests = data.tests.map((testCode, idx) => {
                        const testName = extractTestName(testCode);
                        const testDesc = extractTestDescription(testCode);

                        console.log(`  Test ${idx}: ${testName}`);

                        return {
                            id: `cluster-${data.cluster_id}-test-${idx}`,
                            name: testName,
                            code: testCode.trim(),
                            description: testDesc,
                            category: data.category || 'general',
                            source: `Cluster ${data.cluster_id}`,
                        };
                    });

                    const newCluster = {
                        id: data.cluster_id,
                        theme: data.category
                            ? `${data.category.charAt(0).toUpperCase()}${data.category.slice(1)} Test Cases`
                            : `Cluster ${data.cluster_id}`,
                        description: `Contains ${data.size} test case${data.size > 1 ? 's' : ''} of type: ${data.category || 'general'}`,
                        category: data.category,
                        tests: parsedTests,
                        contributors: [],
                        color: getCategoryColor(data.category),
                    };

                    console.log('✅ Dispatching cluster with tests:', {
                        clusterId: newCluster.id,
                        testCount: parsedTests.length,
                        testNames: parsedTests.map(t => t.name),
                    });

                    dispatch({
                        type: ACTIONS.ADD_CLUSTER,
                        payload: newCluster,
                    });
                    break;
                }

                case 'cluster_update': {
                    console.log('🔄 Cluster update:', data);

                    // ✅ Parse updated tests if present
                    const updatedTests = data.tests?.map((testCode, idx) => ({
                        id: `cluster-${data.cluster_id}-test-${idx}`,
                        name: extractTestName(testCode),
                        code: testCode.trim(),
                        description: extractTestDescription(testCode),
                        category: data.category,
                        source: `Cluster ${data.cluster_id}`,
                    }));

                    dispatch({
                        type: ACTIONS.UPDATE_CLUSTER,
                        payload: {
                            id: data.cluster_id,
                            updates: {
                                tests: updatedTests || data.tests,
                                contributors: data.contributors,
                            },
                        },
                    });
                    break;
                }

                case 'clustering_complete':
                    console.log('✅ Clustering completed:', data);
                    dispatch({
                        type: ACTIONS.UPDATE_PROGRESS,
                        payload: 70,
                    });
                    // addNotification({
                    //     type: 'success',
                    //     message: data.message || `Created ${data.total_clusters} clusters`,
                    //     duration: 3000,
                    // });
                    break;


                // ========== Synthesis Events ==========
                case 'synthesis_start':
                    console.log('🧬 Synthesis started:', data);
                    dispatch({
                        type: ACTIONS.UPDATE_STAGE,
                        payload: 'synthesis',
                    });
                    dispatch({
                        type: ACTIONS.UPDATE_PROGRESS,
                        payload: 80,
                    });
                    // addNotification({
                    //     type: 'info',
                    //     message: data.message || 'Synthesizing tests...',
                    //     duration: 2000,
                    // });
                    break;

                case 'synthesis_chunk':
                    console.log('📝 Synthesis chunk:', data);
                    if (data.chunk && data.chunk.trim()) {
                        dispatch({
                            type: ACTIONS.UPDATE_SYNTHESIS_THINKING,
                            payload: data.chunk,
                        });
                    }
                    break;

                case 'synthesis_thinking':
                    console.log('💭 Synthesis thinking:', data);
                    if (data.thinking || data.chunk) {
                        dispatch({
                            type: ACTIONS.UPDATE_SYNTHESIS_THINKING,
                            payload: data.thinking || data.chunk || '',
                        });
                    }
                    break;

                case 'synthesis_complete':
                    console.log('✅ Synthesis completed:', data);

                    if (data.tests) {
                        dispatch({
                            type: ACTIONS.UPDATE_DEDUPLICATED_TESTS,
                            payload: data.tests.map((test, index) => ({
                                id: test.id || `test-${index}`,
                                name: test.name,
                                code: test.code,
                                category: test.category,
                                description: test.description,
                                sources: test.sources || [],
                                confidence: test.confidence || 1.0,
                            })),
                        });
                    }

                    dispatch({
                        type: ACTIONS.UPDATE_PROGRESS,
                        payload: 90,
                    });

                    // addNotification({
                    //     type: 'success',
                    //     message: data.message || `Synthesized ${data.total_tests} tests`,
                    //     duration: 3000,
                    // });
                    break;

                // ========== Coverage Events ==========
                case 'coverage_start':
                    console.log('🎯 Coverage analysis started:', data);
                    dispatch({
                        type: ACTIONS.UPDATE_STAGE,
                        payload: 'coverage',
                    });
                    // addNotification({
                    //     type: 'info',
                    //     message: data.message || 'Analyzing coverage...',
                    //     duration: 2000,
                    // });
                    break;

                case 'coverage_complete':
                    console.log('✅ Coverage completed:', data);
                    dispatch({
                        type: ACTIONS.UPDATE_COVERAGE,
                        payload: {
                            overall: data.coverage_percentage,
                            categories: data.category_coverage,
                            gaps: data.missing_lines || [],
                        },
                    });
                    // addNotification({
                    //     type: 'success',
                    //     message: data.message || `Coverage: ${data.coverage_percentage}%`,
                    //     duration: 3000,
                    // });
                    break;

                // ========== System Events ==========
                case 'heartbeat':
                    console.log('💓 Heartbeat received');
                    break;

                case 'error':
                    console.error('❌ Pipeline error:', data);
                    dispatch({
                        type: ACTIONS.SET_ERROR,
                        payload: data.message || 'An error occurred during generation',
                    });
                    addNotification({
                        type: 'error',
                        message: data.message || 'Generation failed',
                        duration: 5000,
                    });
                    disconnect();
                    break;

                default:
                    console.warn('⚠️ Unknown SSE event type:', event_type, event);
            }
        },
        [dispatch, ACTIONS, addNotification, disconnect]
    );

    /**
     * Start test generation
     */
    const startGeneration = useCallback(
        async (payload) => {
            console.log('🎬 useTestGeneration.startGeneration called');

            try {
                if (!payload.code || !payload.models || !payload.roles) {
                    throw new Error('Invalid generation parameters');
                }

                dispatch({ type: ACTIONS.START_GENERATION });
                dispatch({
                    type: ACTIONS.SET_PHASE,
                    payload: 'generating',
                });

                abortControllerRef.current = new AbortController();

                const response = await api.generateTests(payload, {
                    signal: abortControllerRef.current.signal,
                });

                unsubscribeRef.current = await connect(response, handleSSEEvent);

                // addNotification({
                //     type: 'info',
                //     message: 'Test generation started',
                //     duration: 3000,
                // });
            } catch (error) {
                console.error('❌ startGeneration error:', error);

                if (error.name === 'AbortError') {
                    dispatch({ type: ACTIONS.CANCEL_GENERATION });
                    addNotification({
                        type: 'warning',
                        message: 'Generation cancelled',
                        duration: 3000,
                    });
                } else {
                    dispatch({
                        type: ACTIONS.SET_ERROR,
                        payload: error.message || 'Failed to start generation',
                    });
                    addNotification({
                        type: 'error',
                        message: error.message || 'Failed to start generation',
                        duration: 5000,
                    });
                }
            }
        },
        [connect, handleSSEEvent, dispatch, ACTIONS, addNotification]
    );

    /**
     * Cancel ongoing generation
     */
    const cancelGeneration = useCallback(() => {
        if (abortControllerRef.current) {
            abortControllerRef.current.abort();
            abortControllerRef.current = null;
        }

        if (unsubscribeRef.current) {
            unsubscribeRef.current();
            unsubscribeRef.current = null;
        }

        disconnect();
        dispatch({ type: ACTIONS.CANCEL_GENERATION });

        addNotification({
            type: 'warning',
            message: 'Generation cancelled',
            duration: 3000,
        });
    }, [disconnect, dispatch, ACTIONS, addNotification]);

    /**
     * Retry generation with same parameters
     */
    const retryGeneration = useCallback(() => {
        const { code, language, selectedModels, selectedRoles } = input;

        if (!code || selectedModels.length === 0 || selectedRoles.length === 0) {
            addNotification({
                type: 'error',
                message: 'Invalid input parameters for retry',
                duration: 3000,
            });
            return;
        }

        startGeneration({
            code,
            language,
            models: selectedModels,
            roles: selectedRoles,
        });
    }, [input, startGeneration, addNotification]);

    return {
        startGeneration,
        cancelGeneration,
        retryGeneration,
        isGenerating: generation.isGenerating,
        currentStage: generation.currentStage,
        progress: generation.progress,
    };
}
