/**
 * Formatting Utilities
 * Helper functions for data transformation and display
 */

/**
 * Format duration from milliseconds to human-readable string
 */
export const formatDuration = (ms) => {
    if (!ms || ms < 0) return '0s';

    const seconds = Math.floor(ms / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);

    if (hours > 0) {
        return `${hours}h ${minutes % 60}m`;
    }
    if (minutes > 0) {
        return `${minutes}m ${seconds % 60}s`;
    }
    return `${seconds}s`;
};

/**
 * Format percentage with precision
 */
export const formatPercentage = (value, decimals = 1) => {
    if (value === null || value === undefined) return '0%';
    return `${Number(value).toFixed(decimals)}%`;
};

/**
 * Format large numbers with K/M suffixes
 */
export const formatNumber = (num) => {
    if (!num) return '0';

    if (num >= 1000000) {
        return `${(num / 1000000).toFixed(1)}M`;
    }
    if (num >= 1000) {
        return `${(num / 1000).toFixed(1)}K`;
    }
    return num.toString();
};

/**
 * Truncate text with ellipsis
 */
export const truncateText = (text, maxLength = 100) => {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    return `${text.substring(0, maxLength)}...`;
};

/**
 * Format timestamp to relative time
 */
export const formatRelativeTime = (timestamp) => {
    const now = Date.now();
    const diff = now - new Date(timestamp).getTime();

    const seconds = Math.floor(diff / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);

    if (days > 0) return `${days}d ago`;
    if (hours > 0) return `${hours}h ago`;
    if (minutes > 0) return `${minutes}m ago`;
    if (seconds > 0) return `${seconds}s ago`;
    return 'just now';
};

/**
 * Format date to locale string
 */
export const formatDate = (date, options = {}) => {
    const defaultOptions = {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
    };

    return new Date(date).toLocaleString('en-US', {
        ...defaultOptions,
        ...options,
    });
};

/**
 * Sanitize code for display (remove sensitive data, normalize whitespace)
 */
export const sanitizeCode = (code) => {
    if (!code) return '';

    return code
        .replace(/\r\n/g, '\n') // Normalize line endings
        .replace(/\t/g, '    ') // Convert tabs to spaces
        .trim();
};

/**
 * Get programming language from code heuristics
 */
export const detectLanguage = (code) => {
    if (!code) return 'python';

    // Simple heuristics
    // if (/^import\s+|^from\s+/.test(code)) return 'python';
    // if (/^def\s+|^class\s+/.test(code)) return 'python';

    return 'python'; // Default
};

/**
 * Format bytes to human-readable size
 */
export const formatBytes = (bytes, decimals = 2) => {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(decimals))} ${sizes[i]}`;
};

/**
 * Calculate color based on percentage (gradient from red to green)
 */
export const getColorForPercentage = (percentage) => {
    if (percentage >= 80) return 'var(--color-success)';
    if (percentage >= 60) return 'var(--color-warning)';
    return 'var(--color-danger)';
};

/**
 * Generate unique ID
 */
export const generateId = () => {
    return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
};

/**
 * Parse error message from various error types
 */
export const parseErrorMessage = (error) => {
    if (typeof error === 'string') return error;
    if (error?.message) return error.message;
    if (error?.error) return error.error;
    return 'An unknown error occurred';
};

/**
 * Format role name for display
 */
export const formatRoleName = (roleId) => {
    if (!roleId) return 'Unknown';

    return roleId
        .split('_')
        .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
};

/**
 * Format model name for display
 */
export const formatModelName = (modelId) => {
    if (!modelId) return 'Unknown';

    // Handle common patterns
    const patterns = {
        'gemini-2.0-flash': 'Gemini 2.0 Flash',
        'deepseek-chat': 'Deepseek Chat',
        'qwen3-235b-a22b': 'Qwen3 235B',
    };

    return patterns[modelId] || modelId;
};

/**
 * Group array by key
 */
export const groupBy = (array, key) => {
    return array.reduce((result, item) => {
        const group = item[key];
        if (!result[group]) {
            result[group] = [];
        }
        result[group].push(item);
        return result;
    }, {});
};

/**
 * Debounce function
 */
export const debounce = (func, wait) => {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
};

export default {
    formatDuration,
    formatPercentage,
    formatNumber,
    truncateText,
    formatRelativeTime,
    formatDate,
    sanitizeCode,
    detectLanguage,
    formatBytes,
    getColorForPercentage,
    generateId,
    parseErrorMessage,
    formatRoleName,
    formatModelName,
    groupBy,
    debounce,
};
