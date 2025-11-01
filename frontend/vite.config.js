import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => ({
    plugins: [react()],

    // ✅ CRITICAL: Set base path for production
    base: mode === 'production' ? '/' : '/',

    // Server configuration
    server: {
        port: 3000,
        host: true,
        open: false,
        strictPort: false,
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
        sourcemap: mode === 'production' ? false : true, // ✅ Disable in prod
        emptyOutDir: true, // ✅ Clean dist folder before build
        rollupOptions: {
            output: {
                manualChunks: {
                    vendor: ['react', 'react-dom'],
                    animations: ['framer-motion'],
                    editor: ['@monaco-editor/react', 'monaco-editor'],
                },
            },
        },
        chunkSizeWarningLimit: 1000,
    },

    // CSS configuration
    css: {
        modules: {
            localsConvention: 'camelCase',
        },
    },

    // Environment variables
    define: {
        __APP_VERSION__: JSON.stringify(process.env.npm_package_version),
    },
}));
