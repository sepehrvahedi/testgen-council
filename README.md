# 🧪 Intelligent Test Council - AI-Powered Python Test Generation

A sophisticated test generation system that uses multiple Large Language Models (LLMs) working together as a "council" to create comprehensive, high-quality test suites for Python functions. The system features intelligent duplicate removal, test classification, coverage analysis, and an interactive GUI interface.

## 🌟 Features

### 🤖 Multi-Model AI Council
- **Collaborative Testing**: Uses multiple LLMs (GPT-4, Claude, Gemini) working together
- **Diverse Perspectives**: Each model contributes unique test cases and edge cases
- **Intelligent Synthesis**: Combines and refines outputs from all models

### 🎯 Comprehensive Test Generation
- **Automatic Code Analysis**: Extracts function signatures, docstrings, and complexity metrics
- **Smart Classification**: Categorizes tests into Basic, Edge Case, Error Handling, Performance, etc.
- **Duplicate Removal**: Uses semantic similarity to eliminate redundant tests
- **Coverage Analysis**: Ensures comprehensive code path coverage

### 🎮 Interactive GUI Interface
- **Jupyter-Friendly**: Beautiful `ipywidgets`-based interface
- **Dark Mode Support**: Optimized styling for both light and dark themes
- **Real-time Progress**: Visual feedback during test generation
- **Clean Output**: Automatically removes markdown formatting from saved files

### 📊 Advanced Analytics
- **Detailed Metrics**: Track test counts, reduction ratios, and coverage percentages
- **Model Performance**: Compare contributions from different AI models
- **Category Breakdown**: Understand test distribution across different types

### Basic Usage

2. **Run the Setup Cells** (Cells 1-12) to initialize all components

3. **Use the Interactive GUI** (Cell 13):
   - Enter your Python function code
   - Click "Generate Tests" 
   - View comprehensive results
   - Save clean test files

## 🔧 Core Components

### 1. Configuration Management (`Config`)
- Manages API keys and model settings
- Supports environment variables and direct configuration
- Handles model availability and fallbacks

### 2. Code Analysis (`CodeAnalyzer`)
- Extracts function information (name, parameters, docstring)
- Calculates complexity metrics
- Identifies potential test scenarios

### 3. LLM Council (`LLMCouncil`)
- Orchestrates multiple AI models
- Generates diverse test cases
- Handles API rate limiting and errors

### 4. Test Classification (`TestClassifier`)
- Categorizes tests by type and purpose
- Ensures comprehensive coverage of test scenarios
- Identifies missing test categories

### 5. Test Synthesis (`TestSynthesizer`)
- Removes semantic duplicates
- Creates clean, executable test files
- Maintains test diversity and coverage

### 6. Coverage Analysis (`CoverageAnalyzer`)
- Analyzes code path coverage
- Identifies untested branches
- Provides coverage metrics

### 7. Interactive GUI (`InteractiveTestGUI`)
- User-friendly Jupyter interface
- Real-time progress tracking
- Clean file output with automatic formatting

## 🎯 Generated Test Categories

The system automatically generates tests in these categories:

- **🔵 Basic Functionality**: Core function behavior
- **⚠️ Edge Cases**: Boundary conditions and special inputs
- **❌ Error Handling**: Exception scenarios and invalid inputs
- **⚡ Performance**: Efficiency and resource usage tests
- **🔀 Integration**: Function interaction tests
- **🧪 Regression**: Tests for known issues
- **📊 Data Validation**: Input/output validation tests

## 📊 Example Output


🎯 GENERATION SUMMARY
==================================================
📊 Original tests generated: 45
🎯 Final tests after synthesis: 23
📉 Reduction ratio: 48.89%
📈 Code coverage: 94.2%
🤖 Models used: gpt-4, claude-3-sonnet, gemini-pro
🏷️  Test categories: Basic, Edge Cases, Error Handling, Performance
⚙️  Synthesizer: gpt-4

## 📝 File Outputs

### `test_generated.py`
Clean Python test file with:
- Proper pytest format
- Comprehensive test coverage
- Clear test documentation
- No markdown artifacts

### `analysis_results.json`
Detailed analysis including:
- Function metadata
- Model contributions
- Test classifications
- Coverage metrics
- Generation statistics

## 🙏 Acknowledgments

- OpenAI for GPT-4 API
- Anthropic for Claude API  
- Google for Gemini API
- Jupyter Project for notebook infrastructure
- ipywidgets for GUI components

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review example notebooks in `/examples`

---

**Made with ❤️ and AI collaboration**

*Generate better tests, write better code!* 🚀
