/**
 * SSE Service - Server-Sent Events Handler
 * Manages real-time streaming from backend
 */

const SSE_RETRY_INTERVAL = parseInt(import.meta.env.VITE_SSE_RETRY_INTERVAL) || 3000;
const SSE_MAX_RETRIES = parseInt(import.meta.env.VITE_SSE_MAX_RETRIES) || 5;

export const SSE_EVENTS = {
    // Pipeline events
    PIPELINE_START: 'pipeline_start',
    PIPELINE_COMPLETE: 'pipeline_complete',

    // LLM events
    LLM_START: 'llm_start',
    LLM_CHUNK: 'llm_chunk',
    LLM_COMPLETE: 'llm_complete',
    LLM_ERROR: 'llm_error',

    // Clustering events
    CLUSTERING_START: 'clustering_start',
    CLUSTER_FORMED: 'cluster_formed',
    CLUSTER_UPDATE: 'cluster_update',
    CLUSTERING_COMPLETE: 'clustering_complete',

    // Synthesis events
    SYNTHESIS_START: 'synthesis_start',
    SYNTHESIS_CHUNK: 'synthesis_chunk',
    SYNTHESIS_COMPLETE: 'synthesis_complete',

    // Coverage events
    COVERAGE_START: 'coverage_start',
    COVERAGE_COMPLETE: 'coverage_complete',

    // System events
    HEARTBEAT: 'heartbeat',
    ERROR: 'error',
};

/**
 * SSE Connection Manager
 */
class SSEManager {
    constructor() {
        this.reader = null;
        this.listeners = new Map();
        this.retryCount = 0;
        this.retryTimeout = null;
        this.isConnected = false;
        this.currentEvent = null;
        this.abortController = null;
        this.shouldStop = false; // ✅ NEW: Flag to gracefully stop reading
    }

    /**
     * Connect to SSE endpoint using fetch Response
     */
    connect(response, onError) {
        if (this.reader) {
            this.disconnect();
        }

        try {
            this.isConnected = true;
            this.shouldStop = false; // ✅ Reset stop flag
            this.retryCount = 0;
            this.abortController = new AbortController();
            this._readStream(response, onError);
        } catch (error) {
            this._handleConnectionError(error, onError);
        }
    }

    /**
     * Read SSE stream from Response
     */
    async _readStream(response, onError) {
        if (!response.body) {
            this._handleConnectionError(new Error('Response body is null'), onError);
            return;
        }

        this.reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';

        try {
            while (true) {
                // ✅ Check if we should stop BEFORE reading
                if (this.shouldStop) {
                    console.log('🛑 SSE stream stopping gracefully');
                    break;
                }

                // ✅ Guard against null reader
                if (!this.reader) {
                    console.log('⚠️ Reader is null, stopping stream');
                    break;
                }

                const { done, value } = await this.reader.read();

                if (done) {
                    console.log('✅ SSE stream ended normally');
                    this._triggerEvent('connection_closed', { reason: 'stream_ended' });
                    break;
                }

                // Decode chunk and add to buffer
                buffer += decoder.decode(value, { stream: true });

                // Process complete messages (split by double newline)
                const messages = buffer.split('\n\n');
                buffer = messages.pop() || ''; // Keep incomplete message in buffer

                for (const message of messages) {
                    if (message.trim() === '') continue;
                    this._parseSSEMessage(message);
                }
            }
        } catch (error) {
            if (error.name === 'AbortError') {
                console.log('🛑 SSE stream aborted by user');
                this._triggerEvent('connection_closed', { reason: 'aborted' });
            } else if (error.message?.includes('Cannot read properties of null')) {
                // ✅ Handle the specific error gracefully
                console.log('ℹ️ SSE stream closed (reader nullified)');
            } else {
                this._handleConnectionError(error, onError);
            }
        } finally {
            this.isConnected = false;
            this.reader = null;
            console.log('🔌 SSE _readStream cleanup complete');
        }
    }

    /**
     * Parse SSE message format
     */
    _parseSSEMessage(message) {
        console.log('📥 Parsing SSE message:', message.substring(0, 100));

        const lines = message.split('\n');
        let eventType = null;
        let data = null;

        for (const line of lines) {
            if (line.startsWith('event:')) {
                eventType = line.substring(6).trim();
            } else if (line.startsWith('data:')) {
                const dataStr = line.substring(5).trim();
                try {
                    data = JSON.parse(dataStr);
                } catch (parseError) {
                    console.error('Failed to parse SSE data:', parseError, dataStr);
                    continue;
                }
            }
        }

        if (eventType && data) {
            console.log('✅ Parsed SSE event:', { event_type: eventType, data });
            this._triggerEvent(eventType, data);
        } else {
            console.warn('⚠️ Incomplete SSE message:', { eventType, data });
        }
    }

    /**
     * Add event listener
     */
    on(eventType, callback) {
        if (!this.listeners.has(eventType)) {
            this.listeners.set(eventType, new Set());
        }
        this.listeners.get(eventType).add(callback);
        return callback; // ✅ Return for easier cleanup
    }

    /**
     * Remove event listener
     */
    off(eventType, callback) {
        if (this.listeners.has(eventType)) {
            this.listeners.get(eventType).delete(callback);
        }
    }

    /**
     * Trigger event listeners
     */
    _triggerEvent(eventType, eventData) {
        console.log('🔔 SSE _triggerEvent:', { eventType, eventData });

        const standardEvent = {
            event_type: eventType,
            data: eventData,
        };

        let hasListeners = false;

        // Trigger specific event listeners
        const listeners = this.listeners.get(eventType);
        if (listeners && listeners.size > 0) {
            hasListeners = true;
            console.log(`✅ Found ${listeners.size} specific listeners for ${eventType}`);
            listeners.forEach(callback => {
                try {
                    callback(standardEvent);
                } catch (error) {
                    console.error(`Error in ${eventType} listener:`, error);
                }
            });
        }

        // Also trigger wildcard listeners
        const wildcardListeners = this.listeners.get('*');
        if (wildcardListeners && wildcardListeners.size > 0) {
            hasListeners = true;
            console.log(`✅ Found ${wildcardListeners.size} wildcard listeners`);
            wildcardListeners.forEach(callback => {
                try {
                    callback(standardEvent);
                } catch (error) {
                    console.error('Error in wildcard listener:', error);
                }
            });
        }

        if (!hasListeners) {
            console.warn(`⚠️ No listeners registered for event: ${eventType}`);
        }
    }

    /**
     * Handle connection errors
     */
    _handleConnectionError(error, onError) {
        console.error('❌ SSE connection error:', error);

        this.isConnected = false;

        if (onError) {
            onError(error);
        }

        this._triggerEvent('error', {
            message: error.message,
            retryCount: this.retryCount,
        });
    }

    /**
     * Disconnect from SSE - IMPROVED
     */
    disconnect() {
        console.log('🔌 SSEManager.disconnect() called');

        // ✅ Set flag to stop reading loop gracefully
        this.shouldStop = true;

        if (this.retryTimeout) {
            clearTimeout(this.retryTimeout);
            this.retryTimeout = null;
        }

        // ✅ Cancel reader FIRST before nullifying
        if (this.reader) {
            this.reader.cancel().catch(err => {
                console.warn('⚠️ Error canceling reader:', err);
            });
            this.reader = null;
        }

        if (this.abortController) {
            this.abortController.abort();
            this.abortController = null;
        }

        this.isConnected = false;
        this.retryCount = 0;

        console.log('✅ SSE disconnect complete');
    }

    /**
     * Remove all listeners
     */
    clearListeners() {
        this.listeners.clear();
    }

    /**
     * Get connection status
     */
    getStatus() {
        return {
            isConnected: this.isConnected,
            retryCount: this.retryCount,
        };
    }
}

export default SSEManager;
