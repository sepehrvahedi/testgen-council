/**
 * useSSEStream Hook
 * Manages SSE connections and event handling
 */

import { useEffect, useRef, useCallback } from 'react';
import SSEManager, { SSE_EVENTS } from '@/services/sse';

export const useSSEStream = () => {
    const managerRef = useRef(null);
    const listenersRef = useRef(new Map());

    // Initialize SSE manager
    useEffect(() => {
        managerRef.current = new SSEManager();

        return () => {
            if (managerRef.current) {
                managerRef.current.disconnect();
                managerRef.current.clearListeners();
            }
        };
    }, []);

    /**
     * Connect to SSE stream and subscribe to events
     * @param {Response} response - Fetch API Response object
     * @param {Function} eventHandler - Callback for all SSE events
     * @returns {Function} Unsubscribe function
     */
    const connect = useCallback(async (response, eventHandler) => {
        if (!managerRef.current) {
            console.error('❌ SSE Manager not initialized');
            throw new Error('SSE Manager not initialized');
        }

        console.log('🔌 useSSEStream: Starting connection...');

        // Subscribe to all events BEFORE connecting
        const unsubscribe = managerRef.current.on('*', (event) => {
            console.log('📨 useSSEStream: Event received from manager:', event);
            eventHandler(event);
        });

        // Start the SSE connection
        managerRef.current.connect(response, (error) => {
            console.error('❌ SSE connection error:', error);
            eventHandler({
                event_type: 'error',
                data: { message: error.message },
            });
        });

        console.log('✅ useSSEStream: Connection established');

        // Return cleanup function
        return () => {
            console.log('🔌 useSSEStream: Cleaning up connection');
            unsubscribe();
            if (managerRef.current) {
                managerRef.current.disconnect();
            }
        };
    }, []);

    /**
     * Subscribe to specific event type
     */
    const subscribe = useCallback((eventType, callback) => {
        if (!managerRef.current) {
            console.warn('⚠️ SSE Manager not initialized for subscribe');
            return () => {};
        }

        console.log(`📡 Subscribing to event: ${eventType}`);
        managerRef.current.on(eventType, callback);

        // Track listener for cleanup
        if (!listenersRef.current.has(eventType)) {
            listenersRef.current.set(eventType, new Set());
        }
        listenersRef.current.get(eventType).add(callback);

        // Return unsubscribe function
        return () => {
            if (managerRef.current) {
                managerRef.current.off(eventType, callback);
            }
            listenersRef.current.get(eventType)?.delete(callback);
        };
    }, []);

    /**
     * Disconnect from SSE stream
     */
    const disconnect = useCallback(() => {
        if (managerRef.current) {
            console.log('🔌 Disconnecting SSE stream');
            managerRef.current.disconnect();
        }
    }, []);

    /**
     * Get connection status
     */
    const getStatus = useCallback(() => {
        return managerRef.current?.getStatus() || {
            isConnected: false,
            retryCount: 0
        };
    }, []);

    return {
        connect,
        disconnect,
        subscribe,
        getStatus,
        SSE_EVENTS,
    };
};
