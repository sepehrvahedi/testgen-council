/**
 * Animation Utilities
 * Framer Motion helpers and presets
 */

import { ANIMATION_VARIANTS, TRANSITIONS } from './constants';

/**
 * Stagger children animation
 */
export const staggerContainer = {
    initial: {},
    animate: {
        transition: {
            staggerChildren: 0.1,
        },
    },
};

/**
 * Stagger children with delay
 */
export const staggerContainerDelayed = (delay = 0.2) => ({
    initial: {},
    animate: {
        transition: {
            staggerChildren: 0.1,
            delayChildren: delay,
        },
    },
});

/**
 * Pulse animation (for loading states)
 */
export const pulse = {
    initial: { scale: 1, opacity: 1 },
    animate: {
        scale: [1, 1.05, 1],
        opacity: [1, 0.8, 1],
        transition: {
            duration: 2,
            repeat: Infinity,
            ease: 'easeInOut',
        },
    },
};

/**
 * Shimmer animation (for loading skeletons)
 */
export const shimmer = {
    initial: { backgroundPosition: '-1000px 0' },
    animate: {
        backgroundPosition: '1000px 0',
        transition: {
            duration: 2,
            repeat: Infinity,
            ease: 'linear',
        },
    },
};

/**
 * Typing cursor blink
 */
export const cursorBlink = {
    animate: {
        opacity: [1, 0],
        transition: {
            duration: 0.7,
            repeat: Infinity,
            repeatType: 'reverse',
        },
    },
};

/**
 * Float animation (for floating elements)
 */
export const float = {
    animate: {
        y: [0, -10, 0],
        transition: {
            duration: 3,
            repeat: Infinity,
            ease: 'easeInOut',
        },
    },
};

/**
 * Glow animation (for glowing effects)
 */
export const glow = {
    animate: {
        boxShadow: [
            '0 0 10px rgba(var(--color-primary-rgb), 0.3)',
            '0 0 20px rgba(var(--color-primary-rgb), 0.6)',
            '0 0 10px rgba(var(--color-primary-rgb), 0.3)',
        ],
        transition: {
            duration: 2,
            repeat: Infinity,
            ease: 'easeInOut',
        },
    },
};

/**
 * Rotate animation
 */
export const rotate = (duration = 2) => ({
    animate: {
        rotate: 360,
        transition: {
            duration,
            repeat: Infinity,
            ease: 'linear',
        },
    },
});

/**
 * Progress bar fill
 */
export const progressFill = (percentage) => ({
    initial: { width: '0%' },
    animate: {
        width: `${percentage}%`,
        transition: {
            duration: 0.5,
            ease: 'easeOut',
        },
    },
});

/**
 * Count up number animation
 */
export const countUp = (from = 0, to = 100) => ({
    initial: { value: from },
    animate: {
        value: to,
        transition: {
            duration: 1,
            ease: 'easeOut',
        },
    },
});

/**
 * List item variants (for animated lists)
 */
export const listItemVariants = {
    hidden: { opacity: 0, x: -20 },
    visible: {
        opacity: 1,
        x: 0,
        transition: TRANSITIONS.smooth,
    },
    exit: {
        opacity: 0,
        x: 20,
        transition: TRANSITIONS.fast,
    },
};

/**
 * Modal backdrop variants
 */
export const backdropVariants = {
    hidden: { opacity: 0 },
    visible: {
        opacity: 1,
        transition: TRANSITIONS.fast,
    },
    exit: {
        opacity: 0,
        transition: TRANSITIONS.fast,
    },
};

/**
 * Modal content variants
 */
export const modalVariants = {
    hidden: {
        opacity: 0,
        scale: 0.95,
        y: -20,
    },
    visible: {
        opacity: 1,
        scale: 1,
        y: 0,
        transition: TRANSITIONS.spring,
    },
    exit: {
        opacity: 0,
        scale: 0.95,
        y: 20,
        transition: TRANSITIONS.fast,
    },
};

/**
 * Page transition variants
 */
export const pageVariants = {
    initial: {
        opacity: 0,
        x: -100,
    },
    animate: {
        opacity: 1,
        x: 0,
        transition: TRANSITIONS.smooth,
    },
    exit: {
        opacity: 0,
        x: 100,
        transition: TRANSITIONS.fast,
    },
};

/**
 * Card hover variants
 */
export const cardHoverVariants = {
    rest: {
        scale: 1,
        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
    },
    hover: {
        scale: 1.02,
        boxShadow: '0 10px 20px rgba(0, 0, 0, 0.2)',
        transition: TRANSITIONS.fast,
    },
};

/**
 * Get variant by name
 */
export const getVariant = (name) => {
    return ANIMATION_VARIANTS[name] || ANIMATION_VARIANTS.fadeIn;
};

/**
 * Get transition by name
 */
export const getTransition = (name) => {
    return TRANSITIONS[name] || TRANSITIONS.smooth;
};

export default {
    staggerContainer,
    staggerContainerDelayed,
    pulse,
    shimmer,
    cursorBlink,
    float,
    glow,
    rotate,
    progressFill,
    countUp,
    listItemVariants,
    backdropVariants,
    modalVariants,
    pageVariants,
    cardHoverVariants,
    getVariant,
    getTransition,
};
