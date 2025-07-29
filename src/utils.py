"""
Utility functions for AnyLang AI Code Writer
Helper functions for parsing, formatting, and other utilities.
"""

import re
import logging
from typing import Dict, Any, List, Optional
from pygments import highlight
from pygments.lexers import get_lexer_by_name, TextLexer
from pygments.formatters import HtmlFormatter

logger = logging.getLogger(__name__)

# Supported programming languages
SUPPORTED_LANGUAGES = {
    "python": "Python",
    "javascript": "JavaScript",
    "java": "Java",
    "cpp": "C++",
    "csharp": "C#",
    "rust": "Rust",
    "go": "Go",
    "sql": "SQL",
    "bash": "Bash",
    "php": "PHP",
    "ruby": "Ruby",
    "swift": "Swift",
    "kotlin": "Kotlin",
    "typescript": "TypeScript",
    "html": "HTML",
    "css": "CSS",
    "scala": "Scala",
    "perl": "Perl",
    "r": "R",
    "matlab": "MATLAB",
    "dart": "Dart",
    "elixir": "Elixir",
    "clojure": "Clojure",
    "haskell": "Haskell",
    "lua": "Lua",
    "assembly": "Assembly",
    "fortran": "Fortran",
    "cobol": "COBOL",
    "pascal": "Pascal",
    "basic": "BASIC",
    "ada": "Ada",
    "lisp": "Lisp",
    "prolog": "Prolog",
    "erlang": "Erlang",
    "ocaml": "OCaml",
    "fsharp": "F#",
    "groovy": "Groovy",
    "julia": "Julia",
    "nim": "Nim",
    "zig": "Zig",
    "v": "V",
    "crystal": "Crystal",
    "nim": "Nim",
    "zig": "Zig",
    "v": "V",
    "crystal": "Crystal",
    "odin": "Odin",
    "carbon": "Carbon",
    "mojo": "Mojo",
    "vlang": "V",
    "carbon": "Carbon",
    "mojo": "Mojo"
}

def get_language_name(language_key: str) -> str:
    """Get display name for language key."""
    return SUPPORTED_LANGUAGES.get(language_key.lower(), language_key.title())

def get_language_key(display_name: str) -> str:
    """Get language key from display name."""
    for key, name in SUPPORTED_LANGUAGES.items():
        if name.lower() == display_name.lower():
            return key
    return display_name.lower()

def get_supported_languages() -> List[str]:
    """Get list of supported language names."""
    return list(SUPPORTED_LANGUAGES.values())

def get_language_keys() -> List[str]:
    """Get list of supported language keys."""
    return list(SUPPORTED_LANGUAGES.keys())

def highlight_code(code: str, language: str) -> str:
    """Apply syntax highlighting to code."""
    try:
        # Map language names to Pygments lexer names
        lexer_mapping = {
            "python": "python",
            "javascript": "javascript",
            "java": "java",
            "cpp": "cpp",
            "csharp": "csharp",
            "rust": "rust",
            "go": "go",
            "sql": "sql",
            "bash": "bash",
            "php": "php",
            "ruby": "ruby",
            "swift": "swift",
            "kotlin": "kotlin",
            "typescript": "typescript",
            "html": "html",
            "css": "css",
            "scala": "scala",
            "perl": "perl",
            "r": "r",
            "matlab": "matlab",
            "dart": "dart",
            "elixir": "elixir",
            "clojure": "clojure",
            "haskell": "haskell",
            "lua": "lua",
            "assembly": "asm",
            "fortran": "fortran",
            "cobol": "cobol",
            "pascal": "pascal",
            "basic": "basic",
            "ada": "ada",
            "lisp": "lisp",
            "prolog": "prolog",
            "erlang": "erlang",
            "ocaml": "ocaml",
            "fsharp": "fsharp",
            "groovy": "groovy",
            "julia": "julia",
            "nim": "nim",
            "zig": "zig",
            "v": "v",
            "crystal": "crystal",
            "odin": "odin",
            "carbon": "cpp",
            "mojo": "python"
        }
        
        lexer_name = lexer_mapping.get(language.lower(), "text")
        lexer = get_lexer_by_name(lexer_name)
        formatter = HtmlFormatter(style='monokai')
        highlighted = highlight(code, lexer, formatter)
        return highlighted
    except Exception as e:
        logger.warning(f"Failed to highlight code for {language}: {e}")
        return code

def extract_code_blocks(text: str) -> List[str]:
    """Extract code blocks from text (markdown-style)."""
    pattern = r'```(?:\w+)?\n(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)
    return [match.strip() for match in matches]

def clean_code(code: str) -> str:
    """Clean and format code."""
    # Remove leading/trailing whitespace
    code = code.strip()
    
    # Remove markdown code block markers if present
    code = re.sub(r'^```\w*\n', '', code)
    code = re.sub(r'\n```$', '', code)
    
    return code

def format_execution_time(seconds: float) -> str:
    """Format execution time in a human-readable format."""
    if seconds < 1:
        return f"{seconds * 1000:.1f}ms"
    elif seconds < 60:
        return f"{seconds:.2f}s"
    else:
        minutes = int(seconds // 60)
        remaining_seconds = seconds % 60
        return f"{minutes}m {remaining_seconds:.1f}s"

def validate_api_key(api_key: str) -> bool:
    """Validate API key format."""
    if not api_key:
        return False
    
    # Basic validation - check if it looks like a valid API key
    # Groq API keys are typically 64 characters
    # Gemini API keys are typically 39 characters
    if len(api_key) < 20:
        return False
    
    return True

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file operations."""
    # Remove or replace unsafe characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    filename = re.sub(r'\s+', '_', filename)
    return filename[:100]  # Limit length

def get_file_extension(language: str) -> str:
    """Get file extension for a programming language."""
    extensions = {
        "python": ".py",
        "javascript": ".js",
        "java": ".java",
        "cpp": ".cpp",
        "csharp": ".cs",
        "rust": ".rs",
        "go": ".go",
        "sql": ".sql",
        "bash": ".sh",
        "php": ".php",
        "ruby": ".rb",
        "swift": ".swift",
        "kotlin": ".kt",
        "typescript": ".ts",
        "html": ".html",
        "css": ".css",
        "scala": ".scala",
        "perl": ".pl",
        "r": ".r",
        "matlab": ".m",
        "dart": ".dart",
        "elixir": ".ex",
        "clojure": ".clj",
        "haskell": ".hs",
        "lua": ".lua",
        "assembly": ".asm",
        "fortran": ".f90",
        "cobol": ".cob",
        "pascal": ".pas",
        "basic": ".bas",
        "ada": ".adb",
        "lisp": ".lisp",
        "prolog": ".pl",
        "erlang": ".erl",
        "ocaml": ".ml",
        "fsharp": ".fs",
        "groovy": ".groovy",
        "julia": ".jl",
        "nim": ".nim",
        "zig": ".zig",
        "v": ".v",
        "crystal": ".cr",
        "odin": ".odin",
        "carbon": ".carbon",
        "mojo": ".mojo"
    }
    return extensions.get(language.lower(), ".txt")

def create_download_filename(language: str, task: str) -> str:
    """Create a filename for code download."""
    # Clean the task description
    clean_task = re.sub(r'[^\w\s-]', '', task)
    clean_task = re.sub(r'\s+', '_', clean_task)
    clean_task = clean_task[:50]  # Limit length
    
    extension = get_file_extension(language)
    return f"{clean_task}{extension}"

def format_error_message(error: str) -> str:
    """Format error message for display."""
    # Remove sensitive information
    error = re.sub(r'api_key["\']?\s*[:=]\s*["\'][^"\']*["\']', 'api_key="***"', error)
    error = re.sub(r'token["\']?\s*[:=]\s*["\'][^"\']*["\']', 'token="***"', error)
    
    return error

def is_executable_language(language: str) -> bool:
    """Check if language supports safe execution."""
    executable_languages = ["python", "sql", "bash"]
    return language.lower() in executable_languages

def get_language_info(language: str) -> Dict[str, Any]:
    """Get information about a programming language."""
    info = {
        "name": get_language_name(language),
        "key": language.lower(),
        "executable": is_executable_language(language),
        "extension": get_file_extension(language),
        "description": get_language_description(language)
    }
    return info

def get_language_description(language: str) -> str:
    """Get description of a programming language."""
    descriptions = {
        "python": "High-level, interpreted programming language known for simplicity and readability",
        "javascript": "Dynamic programming language primarily used for web development",
        "java": "Object-oriented programming language with strong typing and platform independence",
        "cpp": "General-purpose programming language with high performance and low-level control",
        "csharp": "Modern object-oriented language developed by Microsoft",
        "rust": "Systems programming language focused on safety and performance",
        "go": "Statically typed, compiled language designed for simplicity and efficiency",
        "sql": "Structured Query Language for database management and data manipulation",
        "bash": "Command-line shell and scripting language for Unix-like systems",
        "php": "Server-side scripting language designed for web development",
        "ruby": "Dynamic, object-oriented programming language with elegant syntax",
        "swift": "Modern programming language for iOS, macOS, and other Apple platforms",
        "kotlin": "Modern programming language that runs on the Java Virtual Machine",
        "typescript": "Typed superset of JavaScript that compiles to plain JavaScript",
        "html": "Markup language for creating web pages and applications",
        "css": "Style sheet language used for describing the presentation of documents",
        "scala": "Object-oriented and functional programming language for the JVM",
        "perl": "High-level, general-purpose programming language",
        "r": "Programming language and environment for statistical computing",
        "matlab": "Numerical computing environment and programming language",
        "dart": "Client-optimized language for fast apps on any platform",
        "elixir": "Functional, concurrent programming language built on the Erlang VM",
        "clojure": "Dynamic, general-purpose programming language",
        "haskell": "Purely functional programming language with strong static typing",
        "lua": "Lightweight, high-level programming language designed for embedded use",
        "assembly": "Low-level programming language that provides direct hardware control",
        "fortran": "General-purpose programming language especially suited to numeric computation",
        "cobol": "Business-oriented programming language",
        "pascal": "Imperative and procedural programming language",
        "basic": "High-level programming language designed for beginners",
        "ada": "Statically typed, imperative programming language",
        "lisp": "Family of programming languages with a distinctive parenthesized syntax",
        "prolog": "Logic programming language associated with artificial intelligence",
        "erlang": "General-purpose, concurrent programming language",
        "ocaml": "General-purpose programming language with an emphasis on expressiveness",
        "fsharp": "Functional-first programming language",
        "groovy": "Dynamic language for the Java platform",
        "julia": "High-level, high-performance programming language for technical computing",
        "nim": "Statically typed, compiled programming language",
        "zig": "General-purpose programming language and toolchain",
        "v": "Simple, fast, compiled language for developing maintainable software",
        "crystal": "Statically typed, compiled programming language",
        "odin": "Data-oriented programming language",
        "carbon": "Experimental successor to C++",
        "mojo": "Programming language for AI developers"
    }
    return descriptions.get(language.lower(), "Programming language") 