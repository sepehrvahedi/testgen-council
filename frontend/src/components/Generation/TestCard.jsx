/**
 * TestCard Component - Modern test display card with copy functionality
 */

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FiCheckCircle, FiCode, FiLayers, FiCopy, FiCheck } from 'react-icons/fi';
import styles from './TestCard.module.css';
import Prism from 'prismjs';
import 'prismjs/themes/prism-tomorrow.css';
import 'prismjs/components/prism-python';

const TestCard = ({ test, index = 0 }) => {
    const { name, description, code, category, priority } = test;
    const [copiedTest, setCopiedTest] = useState(false);
    const [copiedCode, setCopiedCode] = useState(false);

    const priorityColors = {
        high: '#ef4444',
        medium: '#f59e0b',
        low: '#10b981',
    };

    // Copy entire test (name + description + code)
    const copyFullTest = async () => {
        try {
            const fullText = `${name}\n\n${description || ''}\n\n${code || ''}`.trim();
            await navigator.clipboard.writeText(fullText);
            setCopiedTest(true);
            setTimeout(() => setCopiedTest(false), 2000);
        } catch (err) {
            console.error('Failed to copy test:', err);
        }
    };

    // Copy just the code
    const copyCode = async (e) => {
        e.stopPropagation(); // Prevent details toggle
        try {
            await navigator.clipboard.writeText(code);
            setCopiedCode(true);
            setTimeout(() => setCopiedCode(false), 2000);
        } catch (err) {
            console.error('Failed to copy code:', err);
        }
    };

    return (
        <motion.div
            className={styles.card}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.05 }}
        >
            <div className={styles.header}>
                <div className={styles.titleSection}>
                    <FiCheckCircle className={styles.checkIcon} />
                    <h4 className={styles.name}>{name}</h4>
                </div>
                <div className={styles.headerActions}>
                    {priority && (
                        <span
                            className={styles.priority}
                            style={{ background: priorityColors[priority] }}
                        >
                            {priority}
                        </span>
                    )}
                    <button
                        className={styles.copyButton}
                        onClick={copyFullTest}
                        title="Copy full test"
                    >
                        <AnimatePresence mode="wait">
                            {copiedTest ? (
                                <motion.div
                                    key="check"
                                    initial={{ scale: 0, rotate: -180 }}
                                    animate={{ scale: 1, rotate: 0 }}
                                    exit={{ scale: 0, rotate: 180 }}
                                    transition={{ duration: 0.2 }}
                                >
                                    <FiCheck className={styles.copyIconSuccess} />
                                </motion.div>
                            ) : (
                                <motion.div
                                    key="copy"
                                    initial={{ scale: 0 }}
                                    animate={{ scale: 1 }}
                                    exit={{ scale: 0 }}
                                >
                                    <FiCopy className={styles.copyIcon} />
                                </motion.div>
                            )}
                        </AnimatePresence>
                    </button>
                </div>
            </div>

            {description && <p className={styles.description}>{description}</p>}

            {category && (
                <div className={styles.meta}>
                    <FiLayers className={styles.metaIcon} />
                    <span className={styles.category}>{category}</span>
                </div>
            )}

            {code && (
                <details className={styles.codeSection}>
                    <summary className={styles.codeSummary}>
                        <FiCode className={styles.codeIcon} />
                        <span>View Code</span>
                    </summary>
                    <div className={styles.codeWrapper}>
                        <button
                            className={styles.copyCodeButton}
                            onClick={copyCode}
                            title="Copy code"
                        >
                            <AnimatePresence mode="wait">
                                {copiedCode ? (
                                    <motion.div
                                        key="check"
                                        initial={{ scale: 0, rotate: -180 }}
                                        animate={{ scale: 1, rotate: 0 }}
                                        exit={{ scale: 0, rotate: 180 }}
                                        transition={{ duration: 0.2 }}
                                    >
                                        <FiCheck className={styles.copyIconSuccess} />
                                    </motion.div>
                                ) : (
                                    <motion.div
                                        key="copy"
                                        initial={{ scale: 0 }}
                                        animate={{ scale: 1 }}
                                        exit={{ scale: 0 }}
                                    >
                                        <FiCopy className={styles.copyIcon} />
                                    </motion.div>
                                )}
                            </AnimatePresence>
                        </button>
                        <pre className={`${styles.code} language-python`}>
                            <code
                                className="language-python"
                                dangerouslySetInnerHTML={{
                                    __html: Prism.highlight(
                                        code,
                                        Prism.languages.python,
                                        'python'
                                    ),
                                }}
                            />
                        </pre>
                    </div>
                </details>
            )}
        </motion.div>
    );
};


export default TestCard;
