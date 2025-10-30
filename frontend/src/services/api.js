/**
 * API Service - Backend Communication
 * Handles all HTTP requests to the backend
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
const API_VERSION = import.meta.env.VITE_API_VERSION || 'v1'; // ADDED
const REQUEST_TIMEOUT = import.meta.env.VITE_REQUEST_TIMEOUT || 300000;

/**
 * Custom error class for API errors
 */
export class APIError extends Error {
    constructor(message, status, data) {
        super(message);
        this.name = 'APIError';
        this.status = status;
        this.data = data;
    }
}

/**
 * Create full API URL
 * FIXED: Now uses /api/v1/ prefix
 */
export const createURL = (endpoint) => {
    const base = API_BASE_URL.replace(/\/$/, '');
    const path = endpoint.replace(/^\//, '');
    return `${base}/api/${API_VERSION}/${path}`;
};

/**
 * Handle fetch with timeout
 */
const fetchWithTimeout = async (url, options = {}, timeout = REQUEST_TIMEOUT) => {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    try {
        const response = await fetch(url, {
            ...options,
            signal: controller.signal,
        });
        clearTimeout(timeoutId);
        return response;
    } catch (error) {
        clearTimeout(timeoutId);
        if (error.name === 'AbortError') {
            throw new APIError('Request timeout', 408, null);
        }
        throw error;
    }
};

/**
 * Generic request handler
 */
const request = async (endpoint, options = {}) => {
    const url = createURL(endpoint);

    const defaultHeaders = {
        'Content-Type': 'application/json',
    };

    const config = {
        ...options,
        headers: {
            ...defaultHeaders,
            ...options.headers,
        },
    };

    try {
        const response = await fetchWithTimeout(url, config);

        // Handle non-JSON responses
        const contentType = response.headers.get('content-type');
        const isJSON = contentType && contentType.includes('application/json');

        if (!response.ok) {
            const errorData = isJSON ? await response.json() : await response.text();
            throw new APIError(
                errorData?.detail || errorData || 'Request failed',
                response.status,
                errorData
            );
        }

        // Return JSON if available, otherwise text
        return isJSON ? await response.json() : await response.text();
    } catch (error) {
        if (error instanceof APIError) {
            throw error;
        }

        // Network or other errors
        throw new APIError(
            error.message || 'Network error',
            0,
            null
        );
    }
};

/**
 * API Methods
 */
export const api = {
    /**
     * Fetch backend configuration
     * GET /api/v1/config
     */
    getConfig: async () => {
        // Shorter timeout for config (10 seconds instead of 5 minutes)
        const configTimeout = 10000;

        try {
            const url = createURL('config');
            console.log('📡 Fetching config from:', url);

            const response = await fetchWithTimeout(
                url,
                { method: 'GET' },
                configTimeout
            );

            const contentType = response.headers.get('content-type');
            const isJSON = contentType && contentType.includes('application/json');

            if (!response.ok) {
                throw new APIError(
                    `Config fetch failed: ${response.status}`,
                    response.status,
                    null
                );
            }

            const data = isJSON ? await response.json() : await response.text();
            console.log('✅ Config response:', data);
            return data;
        } catch (error) {
            console.error('❌ Config fetch error:', error);
            throw error;
        }
    },


    /**
     * Generate tests (initiates SSE stream)
     * POST /api/v1/generate-tests
     * Note: This returns a Response object for SSE handling
     */
    generateTests: async (payload, options = {}) => {
        console.log('🌐 api.generateTests called');
        console.log('📦 Payload:', payload);

        const url = createURL('generate-tests');
        console.log('🔗 Target URL:', url);

        // ✅ FIXED: Match backend schema exactly
        const body = {
            // Backend expects 'function_code', not 'code'
            function_code: payload.code,

            // Backend expects 'language' (same)
            language: payload.language || 'python',

            // Backend expects 'models' (same)
            models: payload.models || [],

            // Backend expects 'roles' (same)
            roles: payload.roles || [],

            // Optional: function name (auto-detected if not provided)
            function_name: payload.functionName || null,

            // ✅ FIXED: Backend only accepts 'vector' or 'hash'
            clustering_method: payload.clusteringMethod || 'vector',

            // Optional: max tests per model
            max_tests_per_model: payload.maxTestsPerModel || 10,

            // Optional: run coverage analysis
            run_coverage: payload.runCoverage !== undefined ? payload.runCoverage : true,
        };

        console.log('📤 Request body (backend schema):', body);

        try {
            console.log('📡 Sending POST request...');
            const response = await fetchWithTimeout(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'text/event-stream',
                },
                body: JSON.stringify(body),
                signal: options.signal,
            });

            console.log('✅ Response received:', {
                status: response.status,
                statusText: response.statusText,
                headers: Object.fromEntries(response.headers.entries()),
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => null);
                console.error('❌ API error response:', errorData);

                // Better error message formatting
                let errorMessage = 'Failed to start test generation';
                if (errorData?.detail) {
                    if (Array.isArray(errorData.detail)) {
                        // Pydantic validation errors
                        errorMessage = errorData.detail
                            .map(err => `${err.loc.join('.')}: ${err.msg}`)
                            .join('; ');
                    } else {
                        errorMessage = errorData.detail;
                    }
                }

                throw new APIError(
                    errorMessage,
                    response.status,
                    errorData
                );
            }

            console.log('✅ Returning response for SSE handling');
            return response;
        } catch (error) {
            console.error('❌ api.generateTests error:', error);
            throw error;
        }
    },



    /**
     * Get generation status
     * GET /api/v1/generate-tests/status
     */
    getGenerationStatus: async () => {
        return await request('generate-tests/status', {
            method: 'GET',
        });
    },

    /**
     * Health check
     * GET /api/v1/health
     */
    healthCheck: async () => {
        return await request('health', {
            method: 'GET',
        });
    },

    /**
     * Get available example functions
     * GET /api/v1/examples (if you add this endpoint)
     */
    getExamples: async () => {
        try {
            return await request('examples', {
                method: 'GET',
            });
        } catch (error) {
            // Fallback to hardcoded examples if endpoint doesn't exist
            console.warn('Examples endpoint not available, using fallback');
            return [];
        }
    },
};

// Also export as default for backwards compatibility
export default api;
