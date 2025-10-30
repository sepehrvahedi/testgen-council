/**
 * Card Component with Subcomponents
 */

import { motion } from 'framer-motion';
import styles from './Card.module.css';

const Card = ({ children, variant = 'default', className = '' }) => {
    return (
        <motion.div
            className={`${styles.card} ${styles[variant]} ${className}`}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
        >
            {children}
        </motion.div>
    );
};

// Subcomponents
Card.Header = ({ children, className = '' }) => (
    <div className={`${styles.cardHeader} ${className}`}>{children}</div>
);

Card.Body = ({ children, className = '' }) => (
    <div className={`${styles.cardBody} ${className}`}>{children}</div>
);

Card.Footer = ({ children, className = '' }) => (
    <div className={`${styles.cardFooter} ${className}`}>{children}</div>
);

export default Card;
