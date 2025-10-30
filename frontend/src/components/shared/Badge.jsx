/**
 * Badge Component - Enhanced
 * Small colored labels with icon support
 */

import { motion } from 'framer-motion';

const Badge = ({
                   children,
                   variant = 'default',
                   size = 'md',
                   className = '',
                   ...props
               }) => {
    const variants = {
        default: 'bg-gray-700/50 text-gray-300 border-gray-600/50',
        primary: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
        secondary: 'bg-purple-500/20 text-purple-400 border-purple-500/30',
        success: 'bg-green-500/20 text-green-400 border-green-500/30',
        warning: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
        danger: 'bg-red-500/20 text-red-400 border-red-500/30',
        info: 'bg-cyan-500/20 text-cyan-400 border-cyan-500/30',
    };

    const sizes = {
        sm: 'px-2 py-0.5 text-xs gap-1',
        md: 'px-2.5 py-1 text-sm gap-1.5',
        lg: 'px-3 py-1.5 text-base gap-2',
    };

    return (
        <motion.span
            className={`
                inline-flex items-center justify-center
                rounded-full font-medium border backdrop-blur-sm
                ${variants[variant]}
                ${sizes[size]}
                ${className}
            `}
            initial={{ scale: 0, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ type: 'spring', stiffness: 500, damping: 25 }}
            whileHover={{ scale: 1.05 }}
            {...props}
        >
            {children}
        </motion.span>
    );
};

export default Badge;
