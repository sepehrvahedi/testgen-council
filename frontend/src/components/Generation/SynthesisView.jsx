/**
 * SynthesisView - Final synthesized tests view
 */

import { useState } from 'react';
import { motion } from 'framer-motion';
import { FiZap, FiCheckCircle, FiTrendingUp, FiCopy, FiCheck } from 'react-icons/fi';
import { useApp } from '@/contexts/AppContext';
import TestCard from './TestCard';
import ThinkingStream from './ThinkingStream';
import styles from './SynthesisView.module.css';

const SynthesisView = ({ synthesis }) => {
    const { thinking, deduplicatedTests, coverage } = synthesis || {};
    const { addNotification } = useApp();
    const [copied, setCopied] = useState(false);

    /**
     * Extract pure Python code from markdown code fences
     */
    const extractPythonCode = (text) => {
        if (!text) return '';

        // Remove markdown code fences
        // Pattern:
        // ```python\n ... \n```
        const codeBlockRegex = /```(?:python)?\s*\n?([\s\S]*?)\n?```/g;
        const match = codeBlockRegex.exec(text);

        if (match && match[1]) {
            // Return the content inside the code fences
            return match[1].trim();
        }

        // If no code fences found, return the original text
        // (in case the format changes)
        return text.trim();
    };

    /**
     * Copy final test code to clipboard
     */
    const handleCopyTests = async () => {
        if (!thinking) {
            addNotification({
                type: 'warning',
                message: 'No test code available to copy',
                duration: 3000,
            });
            return;
        }

        try {
            // Extract pure Python code without markdown fences
            const cleanCode = extractPythonCode(thinking);

            await navigator.clipboard.writeText(cleanCode);
            setCopied(true);

            addNotification({
                type: 'success',
                message: 'Test code copied to clipboard!',
                duration: 3000,
            });

            // Reset copied state after 2 seconds
            setTimeout(() => setCopied(false), 2000);
        } catch (error) {
            console.error('Failed to copy:', error);
            addNotification({
                type: 'error',
                message: 'Failed to copy to clipboard',
                duration: 3000,
            });
        }
    };

    return (
        <div className={styles.container}>
            {/* Synthesis Thinking */}
            {thinking && (
                <motion.div
                    className={styles.section}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                >
                    <div className={styles.sectionHeader}>
                        <FiZap className={styles.icon} />
                        <h3>Final Test Suite</h3>

                        {/* ✅ Copy Button */}
                        <button
                            onClick={handleCopyTests}
                            className={styles.copyButton}
                            disabled={copied}
                            title={copied ? 'Copied!' : 'Copy test code'}
                        >
                            {copied ? (
                                <>
                                    <FiCheck className={styles.copyIcon} />
                                    <span>Copied!</span>
                                </>
                            ) : (
                                <>
                                    <FiCopy className={styles.copyIcon} />
                                    <span>Copy Tests</span>
                                </>
                            )}
                        </button>
                    </div>
                    <ThinkingStream content={thinking} />
                </motion.div>
            )}

            {/* Final Tests */}
            {deduplicatedTests?.length > 0 && (
                <motion.div
                    className={styles.section}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 }}
                >
                    <div className={styles.sectionHeader}>
                        <FiCheckCircle className={styles.icon} />
                        <h3>Test Summary</h3>
                        <span className={styles.count}>{deduplicatedTests.length} tests</span>
                    </div>
                    <div className={styles.testsList}>
                        {deduplicatedTests.map((test, index) => (
                            <TestCard key={test.id || index} test={test} />
                        ))}
                    </div>
                </motion.div>
            )}

            {/* Coverage */}
            {/* {coverage && (
                <motion.div
                    className={styles.coverage}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 }}
                >
                    <FiTrendingUp className={styles.coverageIcon} />
                    <div className={styles.coverageContent}>
                        <div className={styles.coverageValue}>{coverage.overall}%</div>
                        <div className={styles.coverageLabel}>Code Coverage</div>
                    </div>
                </motion.div>
            )} */}
        </div>
    );
};

export default SynthesisView;
