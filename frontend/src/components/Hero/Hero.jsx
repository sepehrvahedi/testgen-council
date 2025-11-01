/**
 * Hero Component - Elite Professional Design
 * Sophisticated spacing, refined typography, premium aesthetics
 */

import { motion } from 'framer-motion';
import {
    FiZap,
    FiArrowRight,
    FiMail,
    FiGithub,
    FiExternalLink,
    FiCpu,
    FiShield,
    FiCode,
} from 'react-icons/fi';
import Button from '@/components/shared/Button';
import { useApp } from '@/contexts/AppContext';
import styles from './Hero.module.css';

const Hero = () => {
    const { setPhase } = useApp();

    return (
        <div className={styles.hero}>
            {/* Refined Background */}
            <div className={styles.background}>
                <div className={styles.gradientOrb1} />
                <div className={styles.gradientOrb2} />
                <div className={styles.gridOverlay} />
            </div>

            {/* Main Content */}
            <motion.div
                className={styles.mainContent}
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.9, ease: [0.22, 1, 0.36, 1] }}
            >
                {/* Hero Section */}
                <motion.div
                    className={styles.titleBlock}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2, duration: 0.8 }}
                >
                    <div className={styles.badge}>
                        <span className={styles.badgeDot} />
                        <span>Multi-Agent LLM Council</span>
                    </div>

                    <h1 className={styles.mainTitle}>
                        AI Test Generation
                    </h1>

                    <p className={styles.description}>
                        Three specialized LLMs (Gemini, Deepseek, Qwen) working in parallel
                        with role-based prompting to generate comprehensive unit tests.
                        Watch real-time streaming, intelligent deduplication, and instant results.
                    </p>

                    {/* CTA */}
                    <Button
                        variant="primary"
                        size="hero"
                        onClick={() => setPhase('input')}
                        className={styles.heroButton}
                    >
                        <FiZap className={styles.buttonIcon} />
                        <span>Start Generating Tests</span>
                        <FiArrowRight className={styles.buttonIcon} />
                    </Button>

                    {/* Stats */}
                    <div className={styles.quickStats}>
                        <div className={styles.stat}>
                            <FiCpu className={styles.statIcon} />
                            <span>3 AI Models</span>
                        </div>
                        <div className={styles.stat}>
                            <FiShield className={styles.statIcon} />
                            <span>4 Roles</span>
                        </div>
                        <div className={styles.stat}>
                            <FiCode className={styles.statIcon} />
                            <span>Real-Time</span>
                        </div>
                    </div>
                </motion.div>

                {/* Contact Card */}
                <motion.div
                    className={styles.contactBar}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.5, duration: 0.8 }}
                >
                    <div className={styles.contactSection}>
                        <p className={styles.contactLabel}>Project Owner</p>
                        <a
                            href="mailto:sepehr.vahedi@gmail.com"
                            className={styles.contactLink}
                        >
                            <FiMail className={styles.contactIcon} />
                            <span className={styles.contactText}>sepehr.vahedi@gmail.com</span>
                        </a>
                    </div>

                    <div className={styles.divider} />

                    <div className={styles.contactSection}>
                        <p className={styles.contactLabel}>Source Code</p>
                        <a
                            href="https://github.com/sepehrvahedi/testgen-council"
                            target="_blank"
                            rel="noopener noreferrer"
                            className={styles.contactLink}
                        >
                            <FiGithub className={styles.contactIcon} />
                            <span className={styles.contactText}>GitHub Repository</span>
                        </a>
                    </div>
                </motion.div>

                {/* Lab Credit */}
                <motion.div
                    className={styles.labCredit}
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.7, duration: 0.8 }}
                >
                    <a
                        href="https://sharif.ir/~hmirian/sqrlab.html"
                        target="_blank"
                        rel="noopener noreferrer"
                        className={styles.labLink}
                    >
                        <span className={styles.poweredBy}>POWERED BY</span>
                        <span className={styles.labName}>SQR Lab</span>
                        <FiExternalLink className={styles.labIcon} />
                    </a>
                    <p className={styles.labSubtext}>
                        Software Quality Research Lab, Sharif University of Technology
                    </p>
                </motion.div>
            </motion.div>

            {/* Minimal Ambient Particles */}
            {[...Array(8)].map((_, i) => (
                <motion.div
                    key={i}
                    className={styles.particle}
                    style={{
                        left: `${20 + Math.random() * 60}%`,
                        top: `${20 + Math.random() * 60}%`,
                    }}
                    animate={{
                        y: [0, -15, 0],
                        opacity: [0.05, 0.15, 0.05],
                    }}
                    transition={{
                        duration: 4 + Math.random() * 3,
                        repeat: Infinity,
                        delay: Math.random() * 2,
                        ease: "easeInOut",
                    }}
                />
            ))}
        </div>
    );
};

export default Hero;
