/**
 * GenerationView Component - REDESIGNED
 * Modern, intuitive test generation interface with smooth transitions
 */

import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useApp } from '@/contexts/AppContext';
import { FiCpu, FiPackage, FiZap, FiCheckCircle } from 'react-icons/fi';
import PipelineProgress from './PipelineProgress';
import ModelOutputPanel from './ModelOutputPanel';
import ClusterView from './ClusterView';
import SynthesisView from './SynthesisView';
import styles from './GenerationView.module.css';

const GenerationView = () => {
    const { generation, modelOutputs, clusters, synthesis, config } = useApp();
    const [activeTab, setActiveTab] = useState('models');

    // Auto-switch tabs based on pipeline progress
    useEffect(() => {
        if (generation.currentStage === 'clustering' && clusters?.length > 0) {
            setActiveTab('clusters');
        } else if (generation.currentStage === 'synthesis' && synthesis?.thinking) {
            setActiveTab('synthesis');
        }
    }, [generation.currentStage, clusters, synthesis]);

    if (!generation?.isGenerating &&
        generation?.currentStage !== 'complete' &&
        Object.keys(modelOutputs || {}).length === 0) {
        return null;
    }

    const hasModelOutputs = Object.keys(modelOutputs || {}).length > 0;
    const hasClusters = clusters?.length > 0;
    const hasSynthesis = synthesis?.thinking || synthesis?.deduplicatedTests?.length > 0;

    const tabs = [
        {
            id: 'models',
            label: 'Model Thinking',
            icon: FiCpu,
            count: Object.keys(modelOutputs || {}).length,
            active: hasModelOutputs,
            color: '#6366f1',
        },
        {
            id: 'clusters',
            label: 'Clusters',
            icon: FiPackage,
            count: clusters?.length || 0,
            active: hasClusters,
            color: '#8b5cf6',
        },
        {
            id: 'synthesis',
            label: 'Final Tests',
            icon: FiZap,
            count: synthesis?.deduplicatedTests?.length || 0,
            active: hasSynthesis,
            color: '#10b981',
        },
    ];

    return (
        <div className={styles.container}>
            {/* Header with Pipeline Progress */}
            <motion.div
                className={styles.header}
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
            >
                <div className={styles.headerContent}>
                    <div className={styles.headerTitle}>
                        <FiZap className={styles.headerIcon} />
                        <h1>Test Generation Pipeline</h1>
                    </div>
                    <PipelineProgress
                        currentStage={generation.currentStage}
                        progress={generation.progress}
                        isGenerating={generation.isGenerating}
                    />
                </div>
            </motion.div>

            {/* Tab Navigation */}
            <motion.div
                className={styles.tabsContainer}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
            >
                <div className={styles.tabs}>
                    {tabs.map((tab) => {
                        const Icon = tab.icon;
                        const isActive = activeTab === tab.id;
                        const isDisabled = !tab.active && !isActive;

                        return (
                            <button
                                key={tab.id}
                                className={`${styles.tab} ${isActive ? styles.tabActive : ''} ${
                                    isDisabled ? styles.tabDisabled : ''
                                }`}
                                onClick={() => !isDisabled && setActiveTab(tab.id)}
                                disabled={isDisabled}
                            >
                                <div className={styles.tabContent}>
                                    <Icon className={styles.tabIcon} />
                                    <span className={styles.tabLabel}>{tab.label}</span>
                                    {tab.count > 0 && (
                                        <motion.span
                                            className={styles.tabBadge}
                                            initial={{ scale: 0 }}
                                            animate={{ scale: 1 }}
                                            style={{ backgroundColor: tab.color }}
                                        >
                                            {tab.count}
                                        </motion.span>
                                    )}
                                </div>
                                {isActive && (
                                    <motion.div
                                        className={styles.tabIndicator}
                                        layoutId="activeTab"
                                        style={{ backgroundColor: tab.color }}
                                    />
                                )}
                            </button>
                        );
                    })}
                </div>
            </motion.div>

            {/* Tab Content */}
            <AnimatePresence mode="wait">
                <motion.div
                    key={activeTab}
                    className={styles.content}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -20 }}
                    transition={{ duration: 0.3 }}
                >
                    {activeTab === 'models' && (
                        <ModelOutputsView
                            modelOutputs={modelOutputs}
                            config={config}
                        />
                    )}
                    {activeTab === 'clusters' && <ClusterView clusters={clusters} />}
                    {activeTab === 'synthesis' && <SynthesisView synthesis={synthesis} />}
                </motion.div>
            </AnimatePresence>
        </div>
    );
};

// Model Outputs View
const ModelOutputsView = ({ modelOutputs, config }) => {
    if (!modelOutputs || Object.keys(modelOutputs).length === 0) {
        return (
            <div className={styles.emptyState}>
                <FiCpu className={styles.emptyIcon} />
                <h3>Waiting for Models</h3>
                <p>AI models are starting their thinking process...</p>
            </div>
        );
    }

    return (
        <div className={styles.modelGrid}>
            {Object.entries(modelOutputs).map(([modelName, modelData], index) => (
                <ModelOutputPanel
                    key={modelName}
                    modelName={modelName}
                    modelData={modelData}
                    roles={config?.roles || []}
                    index={index}
                />
            ))}
        </div>
    );
};

export default GenerationView;
