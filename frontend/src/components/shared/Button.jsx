/**
 * Button Component
 * Flexible, animated button with multiple variants
 */

import { motion } from 'framer-motion';
import styles from './Button.module.css';

const Button = ({
                    children,
                    variant = 'primary', // 'primary' | 'secondary' | 'ghost' | 'danger'
                    size = 'medium', // 'small' | 'medium' | 'large'
                    icon,
                    iconPosition = 'left', // 'left' | 'right'
                    fullWidth = false,
                    disabled = false,
                    loading = false,
                    onClick,
                    type = 'button',
                    className = '',
                    ...props
                }) => {
    const buttonClasses = [
        styles.button,
        styles[variant],
        styles[size],
        fullWidth && styles.fullWidth,
        disabled && styles.disabled,
        loading && styles.loading,
        className,
    ]
        .filter(Boolean)
        .join(' ');

    const renderContent = () => {
        if (loading) {
            return (
                <>
                    <span className={styles.spinner} />
                    <span className={styles.loadingText}>Processing...</span>
                </>
            );
        }

        return (
            <>
                {icon && iconPosition === 'left' && (
                    <span className={styles.icon}>{icon}</span>
                )}
                <span className={styles.text}>{children}</span>
                {icon && iconPosition === 'right' && (
                    <span className={styles.icon}>{icon}</span>
                )}
            </>
        );
    };

    return (
        <motion.button
            className={buttonClasses}
            type={type}
            disabled={disabled || loading}
            onClick={onClick}
            whileHover={!disabled && !loading ? { scale: 1.02 } : {}}
            whileTap={!disabled && !loading ? { scale: 0.98 } : {}}
            transition={{ duration: 0.2 }}
            {...props}
        >
            {renderContent()}
        </motion.button>
    );
};

export default Button;
