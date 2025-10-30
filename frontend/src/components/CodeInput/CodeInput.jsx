/**
 * CodeInput Component - SIMPLIFIED & OPTIMIZED
 * Clean, focused interface with everything above the fold
 */

import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    FiCode,
    FiPlay,
    FiAlertCircle,
    FiX,
    FiLock,
} from 'react-icons/fi';
import Editor from '@monaco-editor/react';
import { useApp } from '@/contexts/AppContext';
import { useTestGeneration } from '@/hooks/useTestGeneration';
import Button from '@/components/shared/Button';
import ExampleSelector from './ExampleSelector';
import styles from './CodeInput.module.css';
import { EDITOR_SETTINGS } from '@/utils/constants';

// Language configuration
const SUPPORTED_LANGUAGES = [
    { id: 'python', name: 'Python', available: true },
    { id: 'javascript', name: 'JavaScript', available: false },
    { id: 'java', name: 'Java', available: false },
];

const CodeInput = () => {
    const { config } = useApp();
    const { startGeneration } = useTestGeneration();

    const [code, setCode] = useState('');
    const [language, setLanguage] = useState('python');
    const [selectedModels, setSelectedModels] = useState([]);
    const [validationError, setValidationError] = useState(null);
    const [isTyping, setIsTyping] = useState(false);
    const [hoveredLanguage, setHoveredLanguage] = useState(null);

    const editorRef = useRef(null);
    const typingIntervalRef = useRef(null);

    // Initialize with all models selected
    useEffect(() => {
        if (config?.models?.length > 0 && selectedModels.length === 0) {
            setSelectedModels(config.models.map((m) => m.id));
        }
    }, [config, selectedModels.length]);

    // Validation logic
    const validateInput = () => {
        setValidationError(null);

        if (!code.trim()) {
            setValidationError('Please enter some code to generate tests for');
            return false;
        }

        if (code.trim().length < 10) {
            setValidationError('Code is too short. Please provide more context.');
            return false;
        }

        if (selectedModels.length === 0) {
            setValidationError('Please select at least one model');
            return false;
        }

        return true;
    };

    // Handle generation start
    const handleGenerate = async () => {
        const isValid = validateInput();
        if (!isValid) return;

        const payload = {
            code,
            language,
            models: selectedModels,
            roles: config?.roles?.map((r) => r.id) || [],
            clusteringMethod: 'vector',
            maxTestsPerModel: 10,
            runCoverage: true,
        };

        try {
            await startGeneration(payload);
        } catch (error) {
            setValidationError(error.message || 'Failed to start generation');
        }
    };

    // Handle example selection with typing animation
    const handleExampleSelect = async (example) => {
        if (typingIntervalRef.current) {
            clearInterval(typingIntervalRef.current);
        }

        setIsTyping(true);
        setCode('');
        setLanguage(example.language);

        await new Promise((resolve) => setTimeout(resolve, 100));

        let currentIndex = 0;
        const fullCode = example.code;

        typingIntervalRef.current = setInterval(() => {
            if (currentIndex < fullCode.length) {
                currentIndex++;
                const chunk = fullCode.slice(0, currentIndex);
                setCode(chunk);
            } else {
                clearInterval(typingIntervalRef.current);
                typingIntervalRef.current = null;
                setIsTyping(false);
            }
        }, 15);
    };

    useEffect(() => {
        return () => {
            if (typingIntervalRef.current) {
                clearInterval(typingIntervalRef.current);
            }
        };
    }, []);

    const handleEditorMount = (editor) => {
        editorRef.current = editor;
    };

    const toggleModel = (modelName) => {
        setSelectedModels((prev) =>
            prev.includes(modelName)
                ? prev.filter((m) => m !== modelName)
                : [...prev, modelName]
        );
    };

    const charCount = code.length;
    const lineCount = code.split('\n').length;
    const isReady = code.trim().length >= 10 && selectedModels.length > 0;

    return (
        <div className={styles.container}>
            {/* Animated Background */}
            <div className={styles.backgroundEffect}>
                <div className={styles.gradientOrb1} />
                <div className={styles.gradientOrb2} />
            </div>

            {/* Header with Actions */}
            <motion.div
                className={styles.header}
                initial={{ opacity: 0, y: -30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6 }}
            >
                <div className={styles.titleSection}>
                    <motion.div
                        className={styles.titleIconWrapper}
                        animate={{ rotate: [0, 5, -5, 0] }}
                        transition={{
                            duration: 3,
                            repeat: Infinity,
                            ease: 'easeInOut',
                        }}
                    >
                        <FiCode className={styles.titleIcon} />
                    </motion.div>
                    <div className={styles.titleContent}>
                        <h1 className={styles.title}>
                            Paste Your <span className={styles.titleGradient}>Code</span>
                        </h1>
                        <p className={styles.subtitle}>
                            Select models and generate comprehensive tests
                        </p>
                    </div>
                </div>

                {/* Example Selector & Generate Button in Header */}
                <div className={styles.headerActions}>
                    <ExampleSelector onSelect={handleExampleSelect} disabled={isTyping} />

                    <Button
                        variant="primary"
                        size="lg"
                        icon={<FiPlay />}
                        onClick={handleGenerate}
                        disabled={!isReady || isTyping}
                        className={styles.generateButtonHero}
                    >
                        Generate Tests
                    </Button>
                </div>
            </motion.div>

            {/* Validation Error */}
            <AnimatePresence>
                {validationError && (
                    <motion.div
                        className={styles.errorBanner}
                        initial={{ opacity: 0, y: -20, scale: 0.95 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, y: -20, scale: 0.95 }}
                        transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                    >
                        <FiAlertCircle className={styles.errorIcon} />
                        <span className={styles.errorText}>{validationError}</span>
                        <motion.button
                            className={styles.errorClose}
                            onClick={() => setValidationError(null)}
                            whileHover={{ scale: 1.1 }}
                            whileTap={{ scale: 0.9 }}
                        >
                            <FiX />
                        </motion.button>
                    </motion.div>
                )}
            </AnimatePresence>

            {/* Main Content */}
            <motion.div
                className={styles.content}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.2 }}
            >
                {/* Editor Section */}
                <div className={styles.editorSection}>
                    <div className={styles.editorHeader}>
                        <div className={styles.editorTitle}>
                            <FiCode className={styles.editorIcon} />
                            <span>Code Editor</span>
                        </div>
                        <div className={styles.editorStats}>
                            <div className={styles.statBadge}>
                                <span className={styles.statNumber}>{lineCount}</span>
                                <span className={styles.statLabel}>lines</span>
                            </div>
                            <div className={styles.statDivider} />
                            <div className={styles.statBadge}>
                                <span className={styles.statNumber}>{charCount}</span>
                                <span className={styles.statLabel}>chars</span>
                            </div>
                        </div>
                    </div>

                    {/* Language Selector */}
                    <div className={styles.languageSelector}>
                        {SUPPORTED_LANGUAGES.map((lang) => (
                            <div key={lang.id} className={styles.languageButtonWrapper}>
                                <motion.button
                                    className={`${styles.languageButton} ${
                                        language === lang.id ? styles.languageButtonActive : ''
                                    } ${!lang.available ? styles.languageButtonDisabled : ''}`}
                                    onClick={() => lang.available && setLanguage(lang.id)}
                                    disabled={isTyping || !lang.available}
                                    onMouseEnter={() => !lang.available && setHoveredLanguage(lang.id)}
                                    onMouseLeave={() => setHoveredLanguage(null)}
                                    whileHover={lang.available ? { scale: 1.05 } : {}}
                                    whileTap={lang.available ? { scale: 0.95 } : {}}
                                >
                                    {!lang.available && <FiLock className={styles.lockIcon} />}
                                    {lang.name}
                                </motion.button>

                                {/* Tooltip for unavailable languages */}
                                <AnimatePresence>
                                    {hoveredLanguage === lang.id && !lang.available && (
                                        <motion.div
                                            className={styles.languageTooltip}
                                            initial={{ opacity: 0, y: -5 }}
                                            animate={{ opacity: 1, y: 0 }}
                                            exit={{ opacity: 0, y: -5 }}
                                            transition={{ duration: 0.2 }}
                                        >
                                            Coming soon! {lang.name} support is under development.
                                        </motion.div>
                                    )}
                                </AnimatePresence>
                            </div>
                        ))}
                    </div>

                    {/* Monaco Editor */}
                    <div className={styles.editorWrapper}>
                        <AnimatePresence>
                            {isTyping && (
                                <motion.div
                                    className={styles.typingOverlay}
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                    exit={{ opacity: 0 }}
                                >
                                    <div className={styles.typingIndicator}>
                                        <div className={styles.typingDot} />
                                        <div className={styles.typingDot} />
                                        <div className={styles.typingDot} />
                                        <span className={styles.typingText}>Typing...</span>
                                    </div>
                                </motion.div>
                            )}
                        </AnimatePresence>
                        <Editor
                            height="500px"
                            language={language}
                            value={code}
                            onChange={(value) => !isTyping && setCode(value || '')}
                            onMount={handleEditorMount}
                            theme="vs-dark"
                            options={{
                                ...EDITOR_SETTINGS,
                                fontSize: 14,
                                lineNumbers: 'on',
                                minimap: { enabled: true },
                                scrollBeyondLastLine: false,
                                wordWrap: 'on',
                                readOnly: isTyping,
                            }}
                        />
                    </div>
                </div>

                {/* Model Selection Sidebar */}
                <div className={styles.modelsSection}>
                    <div className={styles.modelsHeader}>
                        <h3 className={styles.modelsTitle}>AI Models</h3>
                        <div className={styles.modelCount}>
                            {selectedModels.length}/{config?.models?.length || 0}
                        </div>
                    </div>

                    <div className={styles.modelsList}>
                        {config?.models?.map((model, index) => {
                            const isSelected = selectedModels.includes(model.id);
                            return (
                                <motion.button
                                    key={model.id}
                                    className={`${styles.modelCard} ${
                                        isSelected ? styles.modelCardActive : ''
                                    }`}
                                    onClick={() => toggleModel(model.id)}
                                    initial={{ opacity: 0, x: 20 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    transition={{ delay: index * 0.05 }}
                                    whileHover={{ scale: 1.02 }}
                                    whileTap={{ scale: 0.98 }}
                                >
                                    <div className={styles.modelContent}>
                                        <div
                                            className={styles.modelIndicator}
                                            style={{
                                                background:
                                                    model.color || 'var(--primary)',
                                            }}
                                        />
                                        <div className={styles.modelInfo}>
                                            <div className={styles.modelName}>
                                                {model.display_name || model.id}
                                            </div>
                                            {model.description && (
                                                <div className={styles.modelDescription}>
                                                    {model.description}
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                    <AnimatePresence>
                                        {isSelected && (
                                            <motion.div
                                                className={styles.modelCheckmark}
                                                initial={{ scale: 0, rotate: -180 }}
                                                animate={{ scale: 1, rotate: 0 }}
                                                exit={{ scale: 0, rotate: 180 }}
                                                transition={{
                                                    type: 'spring',
                                                    stiffness: 500,
                                                    damping: 30,
                                                }}
                                            >
                                                ✓
                                            </motion.div>
                                        )}
                                    </AnimatePresence>
                                </motion.button>
                            );
                        })}
                    </div>
                </div>
            </motion.div>
        </div>
    );
};

export default CodeInput;
