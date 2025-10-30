/**
 * SynthesisView - Final synthesized tests view
 */

import { motion } from 'framer-motion';
import { FiZap, FiCheckCircle, FiTrendingUp } from 'react-icons/fi';
import TestCard from './TestCard';
import ThinkingStream from './ThinkingStream';
import styles from './SynthesisView.module.css';

const SynthesisView = ({ synthesis }) => {
    const { thinking, deduplicatedTests, coverage } = synthesis || {};

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
                        <h3>Synthesis Process</h3>
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
                        <h3>Final Test Suite</h3>
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
            {coverage && (
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
            )}
        </div>
    );
};

export default SynthesisView;
