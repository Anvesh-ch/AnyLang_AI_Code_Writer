# AnyLang AI Code Writer

A powerful Streamlit web application that converts natural language requests into working code in any programming language. Built with free LLM APIs (Groq and Gemini) for code generation, translation, and explanation.

## Features

### Core Features
- **Natural Language to Code**: Convert plain English requests into working code
- **Multi-Language Support**: Python, JavaScript, C++, Java, Rust, Go, SQL, Bash, and more
- **Language Switch & Regeneration**: Change languages and regenerate code instantly
- **Code Explanation**: Get line-by-line explanations of generated code
- **Code Translation**: Translate code between different programming languages
- **Syntax Highlighting**: Beautiful code display with proper syntax highlighting
- **Safe Code Execution**: Run Python/SQL/Bash code safely within the app

### Advanced Features
- **Unit Test Generator**: Auto-generate unit tests for your code
- **Code Refactoring**: Get suggestions for cleaner, more idiomatic code
- **Code Review Mode**: Senior developer-level code review and feedback
- **Documentation Generator**: Auto-generate docstrings and documentation
- **Complexity Analysis**: Time/space complexity analysis with explanations
- **Project Templates**: Generate complete project starter templates

## Setup

### Prerequisites
- Python 3.10+
- Groq API key (free tier available)
- Google Gemini API key (optional, for fallback)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd AnyLang_AI_Code_Writer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory:
```
GROQ_API_KEY=your_groq_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

4. Run the application:
```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`

## Usage

### Basic Code Generation
1. Enter your coding task in plain English (e.g., "Create a function to reverse a linked list")
2. Select your target programming language
3. Click "Generate Code" to get working code
4. Use "Explain Code" to get a line-by-line explanation

### Code Translation
1. Paste your existing code in the translation tab
2. Select source and target languages
3. Click "Translate" to convert between languages

### Advanced Features
- **Unit Tests**: Click "Generate Tests" to create unit tests for your code
- **Code Review**: Use "Review Code" for senior developer feedback
- **Refactor**: Click "Refactor" for cleaner, more idiomatic code suggestions
- **Execute**: Run Python/SQL/Bash code safely within the app

## API Keys

### Groq API (Primary)
- Sign up at [Groq Console](https://console.groq.com/)
- Get your API key from the dashboard
- Free tier includes generous usage limits

### Google Gemini API (Fallback)
- Sign up at [Google AI Studio](https://aistudio.google.com/)
- Get your API key from the API section
- Free tier available

## Tech Stack

- **Frontend**: Streamlit
- **LLM APIs**: Groq (primary), Google Gemini (fallback)
- **Code Execution**: Safe sandboxed execution for Python/SQL/Bash
- **Syntax Highlighting**: Pygments
- **Utilities**: Python standard library + requests

## Project Structure

```
anylang_code_writer/
├── app.py                   # Main Streamlit app
├── requirements.txt         # Dependencies
├── README.md               # This file
├── src/                    # Core business logic
│   ├── llm_client.py       # API interactions
│   ├── prompts.py          # LLM prompts
│   ├── code_executor.py    # Safe code execution
│   └── utils.py            # Utilities
├── components/             # UI components
│   ├── language_selector.py
│   ├── code_display.py
│   └── ...
├── extensions/             # Advanced features
│   ├── unit_test_generator.py
│   ├── code_reviewer.py
│   └── ...
└── assets/                 # Static assets
    ├── custom.css
    └── ...
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
- Create an issue on GitHub
- Check the documentation in the app
- Review the code examples in the assets folder 