/**
 * PipelineProgress Component - Minimalist Text-Based Design
 * Clean progress bar with elegant text indicators
 */

import { motion, AnimatePresence } from 'framer-motion';
import { FiLoader } from 'react-icons/fi';
import styles from './PipelineProgress.module.css';

const PIPELINE_STAGES = [
    {
        id: 'initialization',
        label: 'Initialize',
        color: '#3b82f6',
        description: 'Setting up generation',
    },
    {
        id: 'model_generation',
        label: 'Generate',
        color: '#8b5cf6',
        description: 'AI models generating tests',
    },
    {
        id: 'clustering',
        label: 'Cluster',
        color: '#ec4899',
        description: 'Grouping similar tests',
    },
    {
        id: 'synthesis',
        label: 'Synthesize',
        color: '#f59e0b',
        description: 'Finalizing test suite',
    },
    {
        id: 'complete',
        label: 'Complete',
        color: '#10b981',
        description: 'Ready to use',
    },
];

const PipelineProgress = ({ currentStage, progress, isGenerating }) => {
    const getCurrentStageIndex = () => {
        if (!currentStage) return -1;

        const stageMap = {
            initialization: 0,
            model_generation: 1,
            thinking: 1,
            test_generation: 1,
            clustering: 2,
            cluster_analysis: 2,
            synthesis: 3,
            deduplication: 3,
            coverage_analysis: 3,
            complete: 4,
        };

        return stageMap[currentStage] ?? 1;
    };

    const currentIndex = getCurrentStageIndex();
    const currentStageData = PIPELINE_STAGES[currentIndex] || PIPELINE_STAGES[0];

    return (
        <div className={styles.container}>
            {/* Current Stage Header */}
            <AnimatePresence mode="wait">
                <motion.div
                    key={currentStageData.id}
                    className={styles.currentStageHeader}
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: 10 }}
                    transition={{ duration: 0.2 }}
                >
                    <div className={styles.currentStageInfo}>
                        <div className={styles.stageTitleRow}>
                            <h3 className={styles.currentStageLabel}>{currentStageData.label}</h3>
                            {isGenerating && (
                                <motion.div
                                    className={styles.generatingBadge}
                                    animate={{ opacity: [0.5, 1, 0.5] }}
                                    transition={{ duration: 2, repeat: Infinity }}
                                >
                                    <FiLoader className={styles.generatingIcon} />
                                    <span>Processing</span>
                                </motion.div>
                            )}
                        </div>
                        <p className={styles.currentStageDescription}>
                            {currentStageData.description}
                        </p>
                    </div>
                </motion.div>
            </AnimatePresence>

            {/* Progress Bar with Percentage */}
            <div className={styles.progressSection}>
                <div className={styles.progressHeader}>
                    <span className={styles.progressLabel}>Progress</span>
                    <motion.span
                        className={styles.progressPercentage}
                        key={progress}
                        initial={{ scale: 1.1, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        transition={{ duration: 0.2 }}
                    >
                        {progress}%
                    </motion.span>
                </div>
                <div className={styles.progressBar}>
                    <motion.div
                        className={styles.progressFill}
                        initial={{ width: 0 }}
                        animate={{ width: `${progress}%` }}
                        transition={{ duration: 0.4, ease: 'easeOut' }}
                        style={
                            {
                                '--progress-color': currentStageData.color,
                            }
                        }
                    />
                </div>
            </div>

            {/* Text-Based Pipeline Stages */}
            <div className={styles.pipeline}>
                {PIPELINE_STAGES.map((stage, index) => {
                    const isComplete = index < currentIndex;
                    const isCurrent = index === currentIndex;
                    const isPending = index > currentIndex;

                    return (
                        <motion.div
                            key={stage.id}
                            className={`${styles.stageText} ${
                                isComplete
                                    ? styles.stageComplete
                                    : isCurrent
                                        ? styles.stageCurrent
                                        : styles.stagePending
                            }`}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: index * 0.05 }}
                            style={
                                {
                                    '--stage-color': stage.color,
                                }
                            }
                        >
                            <span className={styles.stageNumber}>{index + 1}</span>
                            <span className={styles.stageName}>{stage.label}</span>
                            {isCurrent && isGenerating && (
                                <motion.span
                                    className={styles.currentDot}
                                    animate={{
                                        scale: [1, 1.2, 1],
                                        opacity: [0.5, 1, 0.5],
                                    }}
                                    transition={{
                                        duration: 1.5,
                                        repeat: Infinity,
                                        ease: 'easeInOut',
                                    }}
                                />
                            )}
                        </motion.div>
                    );
                })}
            </div>
        </div>
    );
};

export default PipelineProgress;
