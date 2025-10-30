/**
 * Hero Component
 * Landing page with animated intro and CTA - Redesigned for maximum impact
 */

import { motion } from 'framer-motion';
import {
    FiZap,
    FiCpu,
    FiShield,
    FiTrendingUp,
    FiArrowRight,
    FiCode,
    FiLayers,
} from 'react-icons/fi';
import Button from '@/components/shared/Button';
import { useApp } from '@/contexts/AppContext';
import styles from './Hero.module.css';

const Hero = () => {
    const { setPhase } = useApp();

    // Animation variants
    const containerVariants = {
        initial: {},
        animate: {
            transition: {
                staggerChildren: 0.15,
                delayChildren: 0.3,
            },
        },
    };

    const itemVariants = {
        initial: { opacity: 0, y: 30 },
        animate: {
            opacity: 1,
            y: 0,
            transition: {
                duration: 0.6,
                ease: [0.25, 0.1, 0.25, 1],
            },
        },
    };

    const features = [
        {
            icon: <FiCpu />,
            title: 'Multi-Model Council',
            description: '3 LLMs working in parallel',
            color: 'var(--accent-blue)',
        },
        {
            icon: <FiZap />,
            title: 'Real-Time Streaming',
            description: 'Watch generation happen live',
            color: 'var(--accent-cyan)',
        },
        {
            icon: <FiShield />,
            title: 'Role-Based Generation',
            description: 'Specialized AI roles',
            color: 'var(--accent-purple)',
        },
        {
            icon: <FiTrendingUp />,
            title: 'Smart Synthesis',
            description: 'Intelligent deduplication',
            color: 'var(--accent-pink)',
        },
        {
            icon: <FiCode />,
            title: 'Production Ready',
            description: 'Copy-paste test code',
            color: 'var(--accent-teal)',
        },
        {
            icon: <FiLayers />,
            title: 'Multi-Stage Pipeline',
            description: '6 processing stages',
            color: 'var(--primary)',
        },
    ];

    return (
        <div className={styles.hero}>
            {/* Background Effects */}
            <div className={styles.background}>
                <div className={styles.gradientOrb1} />
                <div className={styles.gradientOrb2} />
                <div className={styles.gradientOrb3} />
                <div className={styles.gridOverlay} />
                <div className={styles.scanline} />
            </div>

            {/* Main Content Container */}
            <motion.div
                className={styles.contentWrapper}
                variants={containerVariants}
                initial="initial"
                animate="animate"
            >
                {/* Top Badge */}
                <motion.div variants={itemVariants} className={styles.badge}>
                    <span className={styles.badgeDot} />
                    <span>LLM Council Architecture</span>
                    <span className={styles.badgePulse} />
                </motion.div>

                {/* Main Title Section */}
                <motion.div variants={itemVariants} className={styles.titleSection}>
                    <h1 className={styles.mainTitle}>
                        AI-Powered Test Generation
                    </h1>
                    <h2 className={styles.subTitle}>
                        Three LLMs. One Mission.{' '}
                        <span className={styles.gradient}>Comprehensive Coverage.</span>
                    </h2>
                </motion.div>

                {/* Description */}
                <motion.p variants={itemVariants} className={styles.description}>
                    Experience next-generation test creation powered by Gemini, Grok, and
                    Qwen working together in real-time. Watch as multiple AI models
                    collaborate to generate comprehensive, production-ready test suites.
                </motion.p>

                {/* CTA Button */}
                <motion.div
                    variants={itemVariants}
                    className={styles.ctaContainer}
                >
                    <Button
                        variant="primary"
                        size="hero"
                        onClick={() => setPhase('input')}
                        className={styles.heroButton}
                    >
                        <span className={styles.buttonContent}>
                            <FiZap className={styles.buttonIconLeft} />
                            <span className={styles.buttonText}>Start Generating Tests</span>
                            <FiArrowRight className={styles.buttonIconRight} />
                        </span>
                    </Button>
                    <p className={styles.ctaHint}>
                        No setup required • Free to use • Instant results
                    </p>
                </motion.div>

                {/* Stats Row */}
                <motion.div variants={itemVariants} className={styles.statsContainer}>
                    <div className={styles.statCard}>
                        <div className={styles.statNumber}>3</div>
                        <div className={styles.statLabel}>AI Models</div>
                        <div className={styles.statAccent} />
                    </div>
                    <div className={styles.statCard}>
                        <div className={styles.statNumber}>4</div>
                        <div className={styles.statLabel}>Specialized Roles</div>
                        <div className={styles.statAccent} />
                    </div>
                    <div className={styles.statCard}>
                        <div className={styles.statNumber}>∞</div>
                        <div className={styles.statLabel}>Test Cases</div>
                        <div className={styles.statAccent} />
                    </div>
                </motion.div>
            </motion.div>

            {/* Features Grid */}
            <motion.section
                className={styles.featuresSection}
                initial={{ opacity: 0, y: 40 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 1, duration: 0.8 }}
            >
                <div className={styles.featuresGrid}>
                    {features.map((feature, index) => (
                        <motion.div
                            key={index}
                            className={styles.featureCard}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{
                                delay: 1.2 + index * 0.1,
                                duration: 0.5,
                            }}
                            whileHover={{
                                scale: 1.05,
                                y: -5,
                                transition: { duration: 0.2 },
                            }}
                        >
                            <div
                                className={styles.featureIcon}
                                style={{ '--feature-color': feature.color }}
                            >
                                {feature.icon}
                            </div>
                            <h3 className={styles.featureTitle}>{feature.title}</h3>
                            <p className={styles.featureDescription}>
                                {feature.description}
                            </p>
                            <div className={styles.featureGlow} />
                        </motion.div>
                    ))}
                </div>
            </motion.section>

            {/* Floating Particles */}
            {[...Array(20)].map((_, i) => (
                <motion.div
                    key={i}
                    className={styles.particle}
                    style={{
                        left: `${Math.random() * 100}%`,
                        top: `${Math.random() * 100}%`,
                    }}
                    animate={{
                        y: [0, -30, 0],
                        opacity: [0.2, 0.5, 0.2],
                    }}
                    transition={{
                        duration: 3 + Math.random() * 2,
                        repeat: Infinity,
                        delay: Math.random() * 2,
                    }}
                />
            ))}
        </div>
    );
};

export default Hero;
