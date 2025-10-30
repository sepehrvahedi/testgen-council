/**
 * ThinkingStream - FIXED Syntax Highlighting
 * Handles all code fence variations: ```python, ```py, ```, with or without newlines
 */

import { useEffect, useRef, useState } from 'react';
import { motion } from 'framer-motion';
import { FiCpu, FiCode } from 'react-icons/fi';
import Prism from 'prismjs';
import 'prismjs/themes/prism-tomorrow.css';
import 'prismjs/components/prism-python';
import styles from './ThinkingStream.module.css';

const ThinkingStream = ({ content }) => {
    const containerRef = useRef(null);
    const shouldAutoScroll = useRef(true);
    const [processedContent, setProcessedContent] = useState([]);

    // Process and highlight content
    useEffect(() => {
        if (!content) {
            setProcessedContent([]);
            return;
        }

        // More flexible regex that handles:
        // - ```python\ncode``` or ```python code``` or ```py\ncode```
        // - ```\ncode``` or ```code```
        const codeBlockRegex = /```(?:python|py)?[ \t]*\n?([\s\S]*?)```/gi;
        const parts = [];
        let lastIndex = 0;
        let match;

        while ((match = codeBlockRegex.exec(content)) !== null) {
            // Add text before code block
            if (match.index > lastIndex) {
                const textContent = content.substring(lastIndex, match.index);
                if (textContent.trim()) {
                    parts.push({
                        type: 'text',
                        content: textContent,
                    });
                }
            }

            // Add code block (capture group 1 contains the code)
            const code = match[1].trim();

            if (code) {
                parts.push({
                    type: 'code',
                    language: 'python',
                    content: code,
                });
            }

            lastIndex = match.index + match[0].length;
        }

        // Add remaining text
        if (lastIndex < content.length) {
            const textContent = content.substring(lastIndex);
            if (textContent.trim()) {
                parts.push({
                    type: 'text',
                    content: textContent,
                });
            }
        }

        // If no code blocks found, treat entire content as text
        if (parts.length === 0 && content.trim()) {
            parts.push({
                type: 'text',
                content: content,
            });
        }

        setProcessedContent(parts);
    }, [content]);

    // Auto-scroll to bottom
    useEffect(() => {
        if (shouldAutoScroll.current && containerRef.current) {
            containerRef.current.scrollTop = containerRef.current.scrollHeight;
        }
    }, [processedContent]);

    const handleScroll = () => {
        if (containerRef.current) {
            const { scrollTop, scrollHeight, clientHeight } = containerRef.current;
            shouldAutoScroll.current = scrollTop + clientHeight >= scrollHeight - 50;
        }
    };

    if (!content) {
        return (
            <div className={styles.empty}>
                <FiCpu className={styles.emptyIcon} />
                <p>Waiting for thinking stream...</p>
            </div>
        );
    }

    return (
        <motion.div
            className={styles.container}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
        >
            <div
                className={styles.stream}
                ref={containerRef}
                onScroll={handleScroll}
            >
                <div className={styles.content}>
                    {processedContent.map((part, index) => {
                        if (part.type === 'text') {
                            return (
                                <div key={index} className={styles.textBlock}>
                                    {part.content.split('\n').map((line, lineIndex) => (
                                        <div key={lineIndex} className={styles.textLine}>
                                            {line || '\u00A0'}
                                        </div>
                                    ))}
                                </div>
                            );
                        } else if (part.type === 'code') {
                            const highlightedCode = Prism.highlight(
                                part.content,
                                Prism.languages.python,
                                'python'
                            );

                            return (
                                <div key={index} className={styles.codeBlock}>
                                    <div className={styles.codeBlockHeader}>
                                        <FiCode className={styles.codeBlockIcon} />
                                        <span className={styles.codeBlockLang}>
                                            python
                                        </span>
                                    </div>
                                    <pre className="language-python">
                                        <code
                                            className="language-python"
                                            dangerouslySetInnerHTML={{ __html: highlightedCode }}
                                        />
                                    </pre>
                                </div>
                            );
                        }
                        return null;
                    })}
                </div>

                <motion.span
                    className={styles.cursor}
                    animate={{ opacity: [1, 0] }}
                    transition={{ duration: 0.8, repeat: Infinity }}
                >
                    ▊
                </motion.span>
            </div>
        </motion.div>
    );
};

export default ThinkingStream;