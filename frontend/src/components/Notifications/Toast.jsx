/**
 * Toast Component
 * Individual notification with auto-dismiss and animations
 */

import { useEffect } from 'react';
import { motion } from 'framer-motion';
import {
    FiCheckCircle,
    FiAlertCircle,
    FiAlertTriangle,
    FiInfo,
    FiX,
} from 'react-icons/fi';
import styles from './Toast.module.css';
import { TIMEOUTS } from '@/utils/constants';

const Toast = ({ notification, onDismiss }) => {
    const { id, type, message, description, duration } = notification;

    // Auto-dismiss after duration
    useEffect(() => {
        const timeout = setTimeout(() => {
            onDismiss(id);
        }, duration || TIMEOUTS.NOTIFICATION_AUTO_DISMISS);

        return () => clearTimeout(timeout);
    }, [id, duration, onDismiss]);

    // Icon mapping
    const icons = {
        success: <FiCheckCircle className={styles.icon} />,
        error: <FiAlertCircle className={styles.icon} />,
        warning: <FiAlertTriangle className={styles.icon} />,
        info: <FiInfo className={styles.icon} />,
    };

    // Animation variants
    const variants = {
        initial: { opacity: 0, y: -50, scale: 0.9 },
        animate: {
            opacity: 1,
            y: 0,
            scale: 1,
            transition: {
                type: 'spring',
                stiffness: 500,
                damping: 30,
            },
        },
        exit: {
            opacity: 0,
            x: 300,
            transition: {
                duration: 0.2,
            },
        },
    };

    return (
        <motion.div
            className={`${styles.toast} ${styles[type]}`}
            variants={variants}
            initial="initial"
            animate="animate"
            exit="exit"
            layout
        >
            {/* Icon */}
            <div className={styles.iconContainer}>{icons[type]}</div>

            {/* Content */}
            <div className={styles.content}>
                <div className={styles.message}>{message}</div>
                {description && (
                    <div className={styles.description}>{description}</div>
                )}
            </div>

            {/* Close button */}
            <button
                className={styles.closeButton}
                onClick={() => onDismiss(id)}
                aria-label="Dismiss notification"
            >
                <FiX />
            </button>

            {/* Progress bar */}
            <motion.div
                className={styles.progressBar}
                initial={{ scaleX: 1 }}
                animate={{ scaleX: 0 }}
                transition={{
                    duration: (duration || TIMEOUTS.NOTIFICATION_AUTO_DISMISS) / 1000,
                    ease: 'linear',
                }}
            />
        </motion.div>
    );
};

export default Toast;
