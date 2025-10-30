/**
 * ClusterView Component - Premium Redesign
 * Displays clustered test cases with modern, interactive visualization
 */

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Prism from 'prismjs';
import 'prismjs/themes/prism-tomorrow.css';
import 'prismjs/components/prism-python';
import {
    FiPackage,
    FiChevronDown,
    FiChevronRight,
    FiUsers,
    FiTag,
    FiCpu,
    FiCode,
    FiLayers,
    FiCheckCircle,
    FiAlertCircle,
    FiInfo,
    FiZap,
    FiCopy,
    FiExternalLink,
} from 'react-icons/fi';
import Badge from '@/components/shared/Badge';
import styles from './ClusterView.module.css';

const ClusterView = ({ clusters = [] }) => {
    const [expandedClusters, setExpandedClusters] = useState(new Set([]));
    const [selectedTest, setSelectedTest] = useState(null);
    const [copiedTest, setCopiedTest] = useState(null);

    // Auto-highlight code when test is selected
    useEffect(() => {
        if (selectedTest?.code) {
            Prism.highlightAll();
        }
    }, [selectedTest]);

    const toggleCluster = (clusterId) => {
        setExpandedClusters((prev) => {
            const newSet = new Set(prev);
            if (newSet.has(clusterId)) {
                newSet.delete(clusterId);
            } else {
                newSet.add(clusterId);
            }
            return newSet;
        });
    };

    const copyTestCode = async (test) => {
        try {
            await navigator.clipboard.writeText(test.code);
            setCopiedTest(test.id);
            setTimeout(() => setCopiedTest(null), 2000);
        } catch (err) {
            console.error('Failed to copy:', err);
        }
    };

    const getCategoryColor = (category) => {
        const colors = {
            positive: 'success',
            negative: 'danger',
            boundary: 'warning',
            edge_case: 'info',
            security: 'danger',
            performance: 'primary',
        };
        return colors[category] || 'default';
    };

    const getCategoryIcon = (category) => {
        const icons = {
            positive: FiCheckCircle,
            negative: FiAlertCircle,
            boundary: FiInfo,
            edge_case: FiZap,
            security: FiAlertCircle,
            performance: FiZap,
        };
        return icons[category] || FiCode;
    };

    if (!clusters || clusters.length === 0) {
        return (
            <div className={styles.emptyState}>
                <motion.div
                    className={styles.emptyIconWrapper}
                    initial={{ scale: 0, rotate: -180 }}
                    animate={{ scale: 1, rotate: 0 }}
                    transition={{ type: 'spring', duration: 0.8 }}
                >
                    <FiLayers className={styles.emptyIcon} />
                </motion.div>
                <motion.h3
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 }}
                >
                    No Clusters Yet
                </motion.h3>
                <motion.p
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3 }}
                >
                    Clusters will appear once tests are grouped by similarity
                </motion.p>
            </div>
        );
    }

    const totalTests = clusters.reduce((acc, c) => acc + (c.tests?.length || 0), 0);
    const totalContributors = clusters.reduce(
        (acc, c) => acc + (c.contributors?.length || 0),
        0
    );

    return (
        <div className={styles.container}>
            {/* Header */}
            <motion.div
                className={styles.header}
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4 }}
            >
                <div className={styles.headerContent}>
                    <div className={styles.headerIcon}>
                        <FiPackage />
                    </div>
                    <div>
                        <h2 className={styles.headerTitle}>Test Clusters</h2>
                        <p className={styles.headerSubtitle}>
                            Grouped by similarity and category
                        </p>
                    </div>
                </div>
            </motion.div>

            {/* Statistics Bar */}
            <div className={styles.statsBar}>
                <motion.div
                    className={styles.statCard}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.3, delay: 0.1 }}
                    whileHover={{ y: -4 }}
                >
                    <div className={styles.statIconWrapper} style={{ '--stat-color': '#6366f1' }}>
                        <FiPackage className={styles.statIcon} />
                    </div>
                    <div className={styles.statContent}>
                        <span className={styles.statValue}>{clusters.length}</span>
                        <span className={styles.statLabel}>Clusters</span>
                    </div>
                    <div className={styles.statGlow} style={{ '--stat-color': '#6366f1' }} />
                </motion.div>

                <motion.div
                    className={styles.statCard}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.3, delay: 0.2 }}
                    whileHover={{ y: -4 }}
                >
                    <div className={styles.statIconWrapper} style={{ '--stat-color': '#10b981' }}>
                        <FiCode className={styles.statIcon} />
                    </div>
                    <div className={styles.statContent}>
                        <span className={styles.statValue}>{totalTests}</span>
                        <span className={styles.statLabel}>Total Tests</span>
                    </div>
                    <div className={styles.statGlow} style={{ '--stat-color': '#10b981' }} />
                </motion.div>

                <motion.div
                    className={styles.statCard}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.3, delay: 0.3 }}
                    whileHover={{ y: -4 }}
                >
                    <div className={styles.statIconWrapper} style={{ '--stat-color': '#f59e0b' }}>
                        <FiCpu className={styles.statIcon} />
                    </div>
                    <div className={styles.statContent}>
                        <span className={styles.statValue}>{totalContributors}</span>
                        <span className={styles.statLabel}>Contributors</span>
                    </div>
                    <div className={styles.statGlow} style={{ '--stat-color': '#f59e0b' }} />
                </motion.div>
            </div>

            {/* Clusters List */}
            <div className={styles.clustersList}>
                {clusters.map((cluster, index) => {
                    const isExpanded = expandedClusters.has(index);
                    const testCount = cluster.tests?.length || 0;
                    const contributors = cluster.contributors || [];
                    const CategoryIcon = getCategoryIcon(cluster.category);

                    return (
                        <motion.div
                            key={cluster.id || index}
                            className={styles.clusterCard}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.3, delay: index * 0.05 }}
                            layout
                        >
                            {/* Cluster Header */}
                            <motion.button
                                className={styles.clusterHeader}
                                onClick={() => toggleCluster(index)}
                                whileHover={{ backgroundColor: 'rgba(255, 255, 255, 0.03)' }}
                                whileTap={{ scale: 0.98 }}
                            >
                                <div className={styles.clusterHeaderLeft}>
                                    <motion.div
                                        className={styles.expandIconWrapper}
                                        animate={{ rotate: isExpanded ? 90 : 0 }}
                                        transition={{ duration: 0.2 }}
                                    >
                                        <FiChevronRight className={styles.expandIcon} />
                                    </motion.div>

                                    <div
                                        className={styles.clusterIconWrapper}
                                        style={{
                                            '--cluster-color': cluster.color || '#6366f1',
                                        }}
                                    >
                                        <CategoryIcon className={styles.clusterIcon} />
                                        <div className={styles.clusterIconGlow} />
                                    </div>

                                    <div className={styles.clusterInfo}>
                                        <h3 className={styles.clusterTitle}>
                                            {cluster.theme || `Cluster ${index + 1}`}
                                        </h3>
                                        <p className={styles.clusterDescription}>
                                            {cluster.description || 'No description available'}
                                        </p>
                                    </div>
                                </div>

                                <div className={styles.clusterHeaderRight}>
                                    <Badge variant="primary" className={styles.clusterBadge}>
                                        <FiCode size={12} />
                                        {testCount}
                                    </Badge>
                                    {cluster.category && (
                                        <Badge
                                            variant={getCategoryColor(cluster.category)}
                                            className={styles.clusterBadge}
                                        >
                                            <CategoryIcon size={12} />
                                            {cluster.category}
                                        </Badge>
                                    )}
                                </div>
                            </motion.button>

                            {/* Expanded Content */}
                            <AnimatePresence>
                                {isExpanded && (
                                    <motion.div
                                        initial={{ height: 0, opacity: 0 }}
                                        animate={{ height: 'auto', opacity: 1 }}
                                        exit={{ height: 0, opacity: 0 }}
                                        transition={{ duration: 0.3, ease: 'easeInOut' }}
                                        className={styles.clusterContent}
                                    >
                                        <div className={styles.clusterContentInner}>
                                            {/* Contributors */}
                                            {contributors.length > 0 && (
                                                <motion.div
                                                    className={styles.section}
                                                    initial={{ opacity: 0, x: -20 }}
                                                    animate={{ opacity: 1, x: 0 }}
                                                    transition={{ delay: 0.1 }}
                                                >
                                                    <div className={styles.sectionHeader}>
                                                        <div className={styles.sectionHeaderLeft}>
                                                            <FiCpu className={styles.sectionIcon} />
                                                            <h4 className={styles.sectionTitle}>
                                                                Model Contributors
                                                            </h4>
                                                        </div>
                                                        <span className={styles.sectionCount}>
                                                            {contributors.length}
                                                        </span>
                                                    </div>
                                                    <div className={styles.contributorsList}>
                                                        {contributors.map((contributor, idx) => (
                                                            <motion.div
                                                                key={idx}
                                                                initial={{ opacity: 0, scale: 0.8 }}
                                                                animate={{ opacity: 1, scale: 1 }}
                                                                transition={{ delay: idx * 0.05 }}
                                                                whileHover={{ scale: 1.05 }}
                                                            >
                                                                <Badge
                                                                    variant="secondary"
                                                                    className={styles.contributorBadge}
                                                                >
                                                                    <FiCpu size={12} />
                                                                    {contributor}
                                                                </Badge>
                                                            </motion.div>
                                                        ))}
                                                    </div>
                                                </motion.div>
                                            )}

                                            {/* Tests */}
                                            {cluster.tests && cluster.tests.length > 0 && (
                                                <motion.div
                                                    className={styles.section}
                                                    initial={{ opacity: 0, x: -20 }}
                                                    animate={{ opacity: 1, x: 0 }}
                                                    transition={{ delay: 0.2 }}
                                                >
                                                    <div className={styles.sectionHeader}>
                                                        <div className={styles.sectionHeaderLeft}>
                                                            <FiCode className={styles.sectionIcon} />
                                                            <h4 className={styles.sectionTitle}>
                                                                Test Cases
                                                            </h4>
                                                        </div>
                                                        <span className={styles.sectionCount}>
                                                            {testCount}
                                                        </span>
                                                    </div>
                                                    <div className={styles.testsList}>
                                                        {cluster.tests.map((test, testIdx) => {
                                                            const isSelected =
                                                                selectedTest?.id === test.id;
                                                            const isCopied = copiedTest === test.id;

                                                            return (
                                                                <motion.div
                                                                    key={test.id || testIdx}
                                                                    className={`${styles.testItem} ${
                                                                        isSelected
                                                                            ? styles.testItemSelected
                                                                            : ''
                                                                    }`}
                                                                    initial={{ opacity: 0, x: -20 }}
                                                                    animate={{ opacity: 1, x: 0 }}
                                                                    transition={{
                                                                        duration: 0.2,
                                                                        delay: testIdx * 0.03,
                                                                    }}
                                                                    onClick={() =>
                                                                        setSelectedTest(
                                                                            isSelected ? null : test
                                                                        )
                                                                    }
                                                                    whileHover={{ x: 4 }}
                                                                    layout
                                                                >
                                                                    <div
                                                                        className={styles.testHeader}
                                                                    >
                                                                        <div
                                                                            className={
                                                                                styles.testHeaderLeft
                                                                            }
                                                                        >
                                                                            <div
                                                                                className={
                                                                                    styles.testIconWrapper
                                                                                }
                                                                            >
                                                                                <FiCode
                                                                                    className={
                                                                                        styles.testIcon
                                                                                    }
                                                                                />
                                                                            </div>
                                                                            <h5
                                                                                className={
                                                                                    styles.testName
                                                                                }
                                                                            >
                                                                                {test.name ||
                                                                                    'Unnamed Test'}
                                                                            </h5>
                                                                        </div>
                                                                        <div
                                                                            className={
                                                                                styles.testHeaderRight
                                                                            }
                                                                        >
                                                                            {test.category && (
                                                                                <Badge
                                                                                    variant={getCategoryColor(
                                                                                        test.category
                                                                                    )}
                                                                                    size="sm"
                                                                                >
                                                                                    {test.category}
                                                                                </Badge>
                                                                            )}
                                                                            <motion.button
                                                                                className={
                                                                                    styles.testAction
                                                                                }
                                                                                onClick={(e) => {
                                                                                    e.stopPropagation();
                                                                                    copyTestCode(
                                                                                        test
                                                                                    );
                                                                                }}
                                                                                whileHover={{
                                                                                    scale: 1.1,
                                                                                }}
                                                                                whileTap={{
                                                                                    scale: 0.95,
                                                                                }}
                                                                            >
                                                                                {isCopied ? (
                                                                                    <FiCheckCircle />
                                                                                ) : (
                                                                                    <FiCopy />
                                                                                )}
                                                                            </motion.button>
                                                                        </div>
                                                                    </div>

                                                                    {test.description && (
                                                                        <p
                                                                            className={
                                                                                styles.testDescription
                                                                            }
                                                                        >
                                                                            {test.description}
                                                                        </p>
                                                                    )}

                                                                    {/* Expanded Test Details */}
                                                                    <AnimatePresence>
                                                                        {isSelected && (
                                                                            <motion.div
                                                                                className={
                                                                                    styles.testDetails
                                                                                }
                                                                                initial={{
                                                                                    height: 0,
                                                                                    opacity: 0,
                                                                                }}
                                                                                animate={{
                                                                                    height: 'auto',
                                                                                    opacity: 1,
                                                                                }}
                                                                                exit={{
                                                                                    height: 0,
                                                                                    opacity: 0,
                                                                                }}
                                                                                transition={{
                                                                                    duration: 0.3,
                                                                                }}
                                                                            >
                                                                                {test.code && (
                                                                                    <div
                                                                                        className={
                                                                                            styles.testCode
                                                                                        }
                                                                                    >
                                                                                        <div
                                                                                            className={
                                                                                                styles.codeHeader
                                                                                            }
                                                                                        >
                                                                                            <span
                                                                                                className={
                                                                                                    styles.codeLanguage
                                                                                                }
                                                                                            >
                                                                                                Python
                                                                                            </span>
                                                                                            <motion.button
                                                                                                className={
                                                                                                    styles.copyButton
                                                                                                }
                                                                                                onClick={(
                                                                                                    e
                                                                                                ) => {
                                                                                                    e.stopPropagation();
                                                                                                    copyTestCode(
                                                                                                        test
                                                                                                    );
                                                                                                }}
                                                                                                whileHover={{
                                                                                                    scale: 1.05,
                                                                                                }}
                                                                                                whileTap={{
                                                                                                    scale: 0.95,
                                                                                                }}
                                                                                            >
                                                                                                {isCopied ? (
                                                                                                    <>
                                                                                                        <FiCheckCircle
                                                                                                            size={
                                                                                                                14
                                                                                                            }
                                                                                                        />
                                                                                                        Copied!
                                                                                                    </>
                                                                                                ) : (
                                                                                                    <>
                                                                                                        <FiCopy
                                                                                                            size={
                                                                                                                14
                                                                                                            }
                                                                                                        />
                                                                                                        Copy
                                                                                                    </>
                                                                                                )}
                                                                                            </motion.button>
                                                                                        </div>
                                                                                        <pre className="language-python">
                                                                                            <code
                                                                                                className="language-python"
                                                                                                dangerouslySetInnerHTML={{
                                                                                                    __html: Prism.highlight(
                                                                                                        test.code,
                                                                                                        Prism
                                                                                                            .languages
                                                                                                            .python,
                                                                                                        'python'
                                                                                                    ),
                                                                                                }}
                                                                                            />
                                                                                        </pre>
                                                                                    </div>
                                                                                )}
                                                                                {test.source && (
                                                                                    <div
                                                                                        className={
                                                                                            styles.testMeta
                                                                                        }
                                                                                    >
                                                                                        <span
                                                                                            className={
                                                                                                styles.metaLabel
                                                                                            }
                                                                                        >
                                                                                            <FiExternalLink
                                                                                                size={12}
                                                                                            />
                                                                                            Source:
                                                                                        </span>
                                                                                        <Badge
                                                                                            variant="secondary"
                                                                                            size="sm"
                                                                                        >
                                                                                            {test.source}
                                                                                        </Badge>
                                                                                    </div>
                                                                                )}
                                                                            </motion.div>
                                                                        )}
                                                                    </AnimatePresence>
                                                                </motion.div>
                                                            );
                                                        })}
                                                    </div>
                                                </motion.div>
                                            )}
                                        </div>
                                    </motion.div>
                                )}
                            </AnimatePresence>
                        </motion.div>
                    );
                })}
            </div>
        </div>
    );
};

export default ClusterView;
