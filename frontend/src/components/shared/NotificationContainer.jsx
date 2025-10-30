/**
 * NotificationContainer Component
 * Displays toast notifications
 */

import { AnimatePresence, motion } from 'framer-motion';
import { useApp } from '@/contexts/AppContext';
import styles from './NotificationContainer.module.css';

const NotificationContainer = () => {
    const { notifications, removeNotification } = useApp();

    return (
        <div className={styles.container}>
            <AnimatePresence>
                {notifications.map((notification) => (
                    <Notification
                        key={notification.id}
                        notification={notification}
                        onClose={() => removeNotification(notification.id)}
                    />
                ))}
            </AnimatePresence>
        </div>
    );
};

const Notification = ({ notification, onClose }) => {
    const { type, message, description, duration = 5000 } = notification;

    // Auto-close after duration
    if (duration > 0) {
        setTimeout(onClose, duration);
    }

    const icons = {
        success: '✓',
        error: '✕',
        warning: '⚠',
        info: 'ℹ',
    };

    return (
        <motion.div
            className={`${styles.notification} ${styles[type]}`}
            initial={{ opacity: 0, x: 100 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 100 }}
            transition={{ duration: 0.3 }}
        >
            <div className={styles.icon}>{icons[type]}</div>
            <div className={styles.content}>
                <div className={styles.message}>{message}</div>
                {description && <div className={styles.description}>{description}</div>}
            </div>
            <button className={styles.close} onClick={onClose}>
                ✕
            </button>
        </motion.div>
    );
};

export default NotificationContainer;
