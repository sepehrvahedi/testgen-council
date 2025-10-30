/**
 * ModelOutputPanel - REDESIGNED
 * Beautiful, collapsible model output display
 */

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FiChevronDown, FiCpu, FiActivity } from 'react-icons/fi';
import ThinkingStream from './ThinkingStream';
import styles from './ModelOutputPanel.module.css';

const ModelOutputPanel = ({ modelName, modelData, roles, index }) => {
    const [expandedRoles, setExpandedRoles] = useState(new Set());

    const MODEL_COLORS = {
        'gemini-2.0-flash-thinking-exp': '#4285f4',
        'grok-2-latest': '#000000',
        'qwen-qwq-32b-preview': '#722ed1',
        'claude-3-7-sonnet-20250219': '#c17a3a',
        'o1': '#10a37f',
    };

    const modelColor = MODEL_COLORS[modelName] || '#6366f1';

    // Auto-expand first role
    useEffect(() => {
        const activeRoles = Object.keys(modelData || {});
        if (activeRoles.length > 0 && expandedRoles.size === 0) {
            setExpandedRoles(new Set([activeRoles[0]]));
        }
    }, [modelData]);

    const toggleRole = (role) => {
        setExpandedRoles((prev) => {
            const next = new Set(prev);
            next.has(role) ? next.delete(role) : next.add(role);
            return next;
        });
    };

    const activeRoles = Object.keys(modelData || {});

    if (activeRoles.length === 0) {
        return (
            <motion.div
                className={styles.panel}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
            >
                <div className={styles.waiting}>
                    <FiActivity className={styles.waitingIcon} />
                    <h3>{modelName}</h3>
                    <p>Initializing...</p>
                </div>
            </motion.div>
        );
    }

    return (
        <motion.div
            className={styles.panel}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            style={{ '--model-color': modelColor }}
        >
            {/* Panel Header */}
            <div className={styles.panelHeader}>
                <div className={styles.modelInfo}>
                    <div className={styles.modelIcon} style={{ background: modelColor }}>
                        <FiCpu />
                    </div>
                    <div>
                        <h3 className={styles.modelName}>{modelName}</h3>
                        <p className={styles.modelStats}>
                            {activeRoles.length} role{activeRoles.length > 1 ? 's' : ''} active
                        </p>
                    </div>
                </div>
            </div>

            {/* Roles List */}
            <div className={styles.rolesList}>
                {activeRoles.map((role) => {
                    const roleData = modelData[role];
                    const isExpanded = expandedRoles.has(role);
                    const roleConfig = roles?.find((r) => r.name === role);
                    const displayName = roleConfig?.display_name || role;

                    return (
                        <div key={role} className={styles.roleItem}>
                            <button
                                className={styles.roleButton}
                                onClick={() => toggleRole(role)}
                            >
                                <span className={styles.roleName}>{displayName}</span>
                                <div className={styles.roleActions}>
                                    {roleData?.thinking && (
                                        <span className={styles.charCount}>
                                            {roleData.thinking.length} chars
                                        </span>
                                    )}
                                    <motion.div
                                        animate={{ rotate: isExpanded ? 180 : 0 }}
                                        transition={{ duration: 0.2 }}
                                    >
                                        <FiChevronDown className={styles.chevron} />
                                    </motion.div>
                                </div>
                            </button>

                            <AnimatePresence>
                                {isExpanded && (
                                    <motion.div
                                        className={styles.roleContent}
                                        initial={{ height: 0, opacity: 0 }}
                                        animate={{ height: 'auto', opacity: 1 }}
                                        exit={{ height: 0, opacity: 0 }}
                                        transition={{ duration: 0.3 }}
                                    >
                                        <ThinkingStream content={roleData.thinking || ''} />
                                    </motion.div>
                                )}
                            </AnimatePresence>
                        </div>
                    );
                })}
            </div>
        </motion.div>
    );
};

export default ModelOutputPanel;
