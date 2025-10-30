/**
 * useConfig Hook
 * Fetches and manages application configuration
 */

import { useState, useEffect } from 'react';
import { api } from '@/services/api';

export const useConfig = () => {
    const [config, setConfig] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchConfig = async () => {
            console.log('🔄 Fetching config...');
            try {
                setLoading(true);
                const data = await api.getConfig();
                console.log('✅ Config loaded:', data);
                setConfig(data);
                setError(null);
            } catch (err) {
                console.error('❌ Failed to fetch config:', err);
                setError(err.message || 'Failed to load configuration');

                // Fallback config for development
                console.warn('⚠️ Using fallback config');
                setConfig({
                    models: [
                        {
                            id: 'gemini-2.0-flash',
                            name: 'Gemini 2.0 Flash',
                            icon: '✨',
                            color: '#4285f4',
                            roles: ['qa_engineer', 'abstract_thinker', 'agent_of_chaos']
                        },
                        {
                            id: 'deepseek-chat',
                            name: 'Deepseek Chat',
                            icon: '🤖',
                            color: '#000000',
                            roles: ['qa_engineer', 'agent_of_chaos']
                        },
                    ],
                    roles: [
                        {
                            id: 'qa_engineer',
                            name: 'By-the-Book QA Engineer',
                            icon: '🎯',
                            color: '#52c41a',
                            philosophy: 'Meticulous and systematic.'
                        },
                        {
                            id: 'agent_of_chaos',
                            name: 'Agent of Chaos',
                            icon: '💥',
                            color: '#f5222d',
                            philosophy: 'If it can break, I will find a way.'
                        },
                        {
                            id: 'abstract_thinker',
                            name: 'Abstract Thinker',
                            icon: '🧩',
                            color: '#722ed1',
                            philosophy: 'Test the underlying properties.'
                        },
                    ],
                    clustering_methods: [
                        { id: 'semantic', name: 'Semantic Clustering' },
                        { id: 'hash', name: 'Fast Structural Hashing' }
                    ],
                    test_categories: ['positive', 'negative', 'boundary', 'edge_case', 'security']
                });
            } finally {
                setLoading(false);
                console.log('✅ Config loading complete (loading=false)');
            }
        };

        fetchConfig();
    }, []);

    return { config, loading, error };
};
