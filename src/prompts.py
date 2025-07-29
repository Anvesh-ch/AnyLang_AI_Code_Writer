"""
Prompt Templates for AnyLang AI Code Writer
Contains all prompt templates used for different LLM tasks.
"""

# Code Generation Prompts
CODE_GENERATION_PROMPT = """You are an expert programmer.
Task: {task}
Language: {language}
Requirements:
- Write clean, idiomatic code in the selected language.
- Add concise comments for clarity.
- Output only the code block, no extra explanation.
- Ensure the code is functional and follows best practices.
- Include proper error handling where appropriate.
- Use modern language features and conventions."""

# Code Explanation Prompts
CODE_EXPLANATION_PROMPT = """Explain the following {language} code line by line in plain English, suitable for a beginner:

{code}

Provide a clear, educational explanation that helps understand:
- What each line does
- How the code flows
- Key concepts and patterns used
- Any important algorithms or data structures
- The overall purpose and functionality"""

# Code Translation Prompts
CODE_TRANSLATION_PROMPT = """Translate the following code from {source_language} to {target_language}, preserving functionality and idiomatic style:

{code}

Requirements:
- Maintain the same functionality and logic
- Use idiomatic {target_language} patterns and conventions
- Preserve comments and documentation
- Handle language-specific features appropriately
- Ensure the translated code is clean and readable"""

# Unit Test Generation Prompts
UNIT_TEST_PROMPT = """Write comprehensive unit tests for the following {language} code using the best practice testing framework:

{code}

Requirements:
- Test all major functions and edge cases
- Include positive and negative test cases
- Use descriptive test names
- Follow testing best practices for {language}
- Include setup and teardown if needed
- Test error conditions and boundary cases"""

# Code Review Prompts
CODE_REVIEW_PROMPT = """Review this {language} code as a senior developer. Provide a comprehensive analysis including:

1. **Strengths**: What the code does well
2. **Areas for Improvement**: Specific issues and suggestions
3. **Best Practices**: How to make it more idiomatic
4. **Performance**: Any performance considerations
5. **Security**: Security concerns if applicable
6. **Maintainability**: How to make it more maintainable

Code to review:
{code}

Then, provide an improved version of the code that addresses the issues identified."""

# Code Refactoring Prompts
CODE_REFACTOR_PROMPT = """Refactor the following {language} code to make it cleaner, more efficient, and more idiomatic:

{code}

Requirements:
- Improve code structure and organization
- Use more idiomatic {language} patterns
- Optimize performance where possible
- Improve readability and maintainability
- Follow {language} best practices
- Preserve all functionality
- Add better error handling if needed"""

# Documentation Generation Prompts
DOCSTRING_PROMPT = """Generate comprehensive documentation for the following {language} code:

{code}

Requirements:
- Add detailed docstrings for all functions/classes
- Include parameter descriptions and return types
- Document any complex algorithms or logic
- Follow {language} documentation conventions
- Include usage examples where helpful
- Document any important assumptions or limitations"""

# Complexity Analysis Prompts
COMPLEXITY_PROMPT = """Analyze the time and space complexity of the following {language} code:

{code}

Provide a detailed analysis including:
1. **Time Complexity**: Big O notation and explanation
2. **Space Complexity**: Memory usage analysis
3. **Algorithm Analysis**: What algorithms/data structures are used
4. **Optimization Opportunities**: How to improve performance
5. **Edge Cases**: Performance considerations for edge cases
6. **Practical Implications**: Real-world performance impact"""

# Project Template Generation Prompts
PROJECT_TEMPLATE_PROMPT = """Generate a complete project template for: {project_description}

Language: {language}

Requirements:
- Create a complete, runnable project structure
- Include all necessary files (main code, tests, documentation, etc.)
- Follow {language} project conventions and best practices
- Include proper error handling and logging
- Add comprehensive documentation
- Include example usage and setup instructions
- Make it production-ready with proper configuration"""

# Debug Mode Prompts
DEBUG_PROMPT = """Debug the following {language} code. The user reports: {bug_description}

Code with bug:
{code}

Provide a detailed analysis including:
1. **Bug Identification**: What's causing the issue
2. **Root Cause**: Why the bug occurs
3. **Fix**: Corrected code with explanation
4. **Prevention**: How to avoid similar bugs
5. **Testing**: How to verify the fix works"""

# Safe Code Execution Validation Prompts
SAFETY_VALIDATION_PROMPT = """Analyze the following {language} code for safety before execution:

{code}

Check for:
1. **File System Access**: Any file read/write operations
2. **Network Access**: Any network requests
3. **System Commands**: Any system-level operations
4. **Infinite Loops**: Potential infinite loops
5. **Resource Usage**: Memory or CPU intensive operations
6. **Security Risks**: Any security vulnerabilities

Provide a safety assessment and recommend if it's safe to execute."""

# Language-specific prompts
LANGUAGE_SPECIFIC_PROMPTS = {
    "python": {
        "style_guide": "Follow PEP 8 style guidelines",
        "common_patterns": "Use list comprehensions, context managers, and type hints where appropriate",
        "testing": "Use pytest for testing",
        "documentation": "Use Google-style docstrings"
    },
    "javascript": {
        "style_guide": "Follow ESLint and Prettier standards",
        "common_patterns": "Use ES6+ features, async/await, and functional programming where appropriate",
        "testing": "Use Jest for testing",
        "documentation": "Use JSDoc comments"
    },
    "java": {
        "style_guide": "Follow Google Java Style Guide",
        "common_patterns": "Use streams, optionals, and modern Java features",
        "testing": "Use JUnit for testing",
        "documentation": "Use JavaDoc comments"
    },
    "cpp": {
        "style_guide": "Follow Google C++ Style Guide",
        "common_patterns": "Use RAII, smart pointers, and modern C++ features",
        "testing": "Use Google Test or Catch2",
        "documentation": "Use Doxygen comments"
    },
    "rust": {
        "style_guide": "Follow Rust style guidelines",
        "common_patterns": "Use ownership, borrowing, and Result types",
        "testing": "Use built-in testing framework",
        "documentation": "Use Rust doc comments"
    },
    "go": {
        "style_guide": "Follow Go style guidelines (gofmt)",
        "common_patterns": "Use goroutines, channels, and interfaces",
        "testing": "Use built-in testing package",
        "documentation": "Use Go doc comments"
    },
    "sql": {
        "style_guide": "Use consistent naming and formatting",
        "common_patterns": "Use CTEs, window functions, and proper indexing",
        "testing": "Use database-specific testing tools",
        "documentation": "Use inline comments for complex queries"
    },
    "bash": {
        "style_guide": "Follow Shell Style Guide",
        "common_patterns": "Use proper quoting, error handling, and functions",
        "testing": "Use shellcheck and manual testing",
        "documentation": "Use inline comments for complex scripts"
    }
}

def get_language_specific_prompt(language: str, prompt_type: str) -> str:
    """Get language-specific prompt enhancement."""
    if language.lower() in LANGUAGE_SPECIFIC_PROMPTS:
        return LANGUAGE_SPECIFIC_PROMPTS[language.lower()].get(prompt_type, "")
    return ""

def format_prompt(template: str, **kwargs) -> str:
    """Format a prompt template with the given parameters."""
    return template.format(**kwargs) 