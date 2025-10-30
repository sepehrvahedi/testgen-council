import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [react()],

    // Server configuration
    server: {
        port: 3000,
        host: true, // Listen on all addresses
        open: true, // Auto-open browser
        strictPort: false, // Try next port if 3000 is busy
    },

    // Path aliases
    resolve: {
        alias: {
            '@': path.resolve(__dirname, './src'),
        },
    },

    // Build configuration
    build: {
        outDir: 'dist',
        sourcemap: true,
        rollupOptions: {
            output: {
                manualChunks: {
                    vendor: ['react', 'react-dom'],
                    animations: ['framer-motion'],
                },
            },
        },
    },

    // CSS configuration
    css: {
        modules: {
            localsConvention: 'camelCase',
        },
    },
});
