/**
 * ExampleSelector Component - SIMPLIFIED
 */

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FiChevronDown, FiZap } from 'react-icons/fi';
import styles from './ExampleSelector.module.css';

const EXAMPLES = [
    {
        id: 'factorial',
        name: 'Factorial',
        language: 'python',
        icon: '🔢',
        code: `def factorial(n):
    """Calculate factorial of n"""
    if n < 0:
        raise ValueError("Factorial not defined for negative numbers")
    if n <= 1:
        return 1
    return n * factorial(n - 1)`,
    },
    {
        id: 'binary-search',
        name: 'Binary Search',
        language: 'python',
        icon: '🔍',
        code: `def binary_search(arr, target):
    """Binary search implementation"""
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1`,
    },
    {
        id: 'merge-sort',
        name: 'Merge Sort',
        language: 'python',
        icon: '🔄',
        code: `def merge_sort(arr):
    """Merge sort implementation"""
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result`,
    },
];

const ExampleSelector = ({ onSelect, disabled }) => {
    const [isOpen, setIsOpen] = useState(false);

    const handleSelect = (example) => {
        onSelect(example);
        setIsOpen(false);
    };

    return (
        <div className={styles.container}>
            <motion.button
                className={styles.trigger}
                onClick={() => setIsOpen(!isOpen)}
                disabled={disabled}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
            >
                <div className={styles.triggerContent}>
                    <FiZap className={styles.triggerIcon} />
                    <span>Load Example Code</span>
                </div>
                <motion.div
                    animate={{ rotate: isOpen ? 180 : 0 }}
                    transition={{ duration: 0.3 }}
                >
                    <FiChevronDown />
                </motion.div>
            </motion.button>

            <AnimatePresence>
                {isOpen && (
                    <>
                        <motion.div
                            className={styles.backdrop}
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            onClick={() => setIsOpen(false)}
                        />
                        <motion.div
                            className={styles.dropdown}
                            initial={{ opacity: 0, y: -10, scale: 0.95 }}
                            animate={{ opacity: 1, y: 0, scale: 1 }}
                            exit={{ opacity: 0, y: -10, scale: 0.95 }}
                            transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                        >
                            {EXAMPLES.map((example, index) => (
                                <motion.button
                                    key={example.id}
                                    className={styles.exampleItem}
                                    onClick={() => handleSelect(example)}
                                    initial={{ opacity: 0, x: -10 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    transition={{ delay: index * 0.05 }}
                                    whileHover={{ x: 4 }}
                                >
                                    <span className={styles.exampleIcon}>
                                        {example.icon}
                                    </span>
                                    <div className={styles.exampleInfo}>
                                        <div className={styles.exampleName}>
                                            {example.name}
                                        </div>
                                        <div className={styles.exampleMeta}>
                                            {example.language} •{' '}
                                            {example.code.split('\n').length} lines
                                        </div>
                                    </div>
                                </motion.button>
                            ))}
                        </motion.div>
                    </>
                )}
            </AnimatePresence>
        </div>
    );
};

export default ExampleSelector;
