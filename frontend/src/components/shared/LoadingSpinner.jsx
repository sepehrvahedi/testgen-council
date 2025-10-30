/**
 * LoadingSpinner Component
 * Reusable loading indicator with size variants
 */

import { motion } from 'framer-motion';
import styles from './Button.module.css'; // Reusing button styles

const LoadingSpinner = ({ size = 'md', className = '' }) => {
    const sizeClasses = {
        sm: 'w-4 h-4',
        md: 'w-6 h-6',
        lg: 'w-8 h-8',
        xl: 'w-12 h-12',
    };

    return (
        <motion.div
            className={`${sizeClasses[size]} ${className}`}
            style={{
                border: '2px solid var(--glass-border)',
                borderTopColor: 'var(--color-primary)',
                borderRadius: '50%',
            }}
            animate={{ rotate: 360 }}
            transition={{
                duration: 1,
                repeat: Infinity,
                ease: 'linear',
            }}
            aria-label="Loading"
            role="status"
        />
    );
};

export default LoadingSpinner;
