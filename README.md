# AnyLang AI Code Writer

A powerful Streamlit web application that converts natural language requests into working code in any programming language. Built with free LLM APIs (Groq and Gemini) and enhanced with RAG (Retrieval-Augmented Generation) for personalized, grounded code generation.

## Features

### Core Features
- **Natural Language to Code**: Convert plain English requests into working code
- **Multi-Language Support**: Python, JavaScript, C++, Java, Rust, Go, SQL, Bash, and more
- **Language Switch & Regeneration**: Change languages and regenerate code instantly
- **Code Explanation**: Get line-by-line explanations of generated code
- **Code Translation**: Translate code between different programming languages
- **Syntax Highlighting**: Beautiful code display with proper syntax highlighting
- **Safe Code Execution**: Run Python/SQL/Bash code safely within the app

### RAG-Enhanced Features
- **Personal Code Library**: Upload your own code files for personalized generation
- **Semantic Code Search**: Search your codebase using natural language queries
- **Grounded Code Generation**: Generate code that matches your coding style and patterns
- **Context-Aware Translation**: Translate code while preserving your project's conventions
- **Style-Consistent Explanations**: Get explanations that reference your existing code patterns
- **Local Vector Database**: All embeddings and search stored locally for privacy

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

### RAG-Enhanced Usage
1. **Upload Your Code**: Go to the "Code Library" tab and upload your code files
2. **Enable RAG Mode**: Go to "RAG Settings" and enable RAG mode
3. **Search Your Code**: Use "Semantic Search" to find relevant code in your codebase
4. **Generate Grounded Code**: Your code generation will now use your codebase for context
5. **Style-Consistent Results**: Generated code will match your coding patterns and conventions

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
- **RAG Components**: 
  - **Embeddings**: SentenceTransformers (all-MiniLM-L6-v2)
  - **Vector Database**: FAISS (local storage)
  - **Code Chunking**: Language-specific parsers (AST for Python, regex for others)
- **Code Execution**: Safe sandboxed execution for Python/SQL/Bash
- **Syntax Highlighting**: Built-in Streamlit highlighting
- **Utilities**: Python standard library + requests

## Project Structure

```
AnyLang_AI_Code_Writer/
├── app.py                          # Main Streamlit application
├── requirements.txt                 # Python dependencies
├── README.md                       # Project documentation
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
├── code_library/                   # RAG storage directory (NEW)
│   ├── user_uploads/              # User uploaded code files
│   ├── embeddings/                # Generated embeddings
│   └── vector_db/                 # FAISS index and metadata
├── src/                           # Core application logic
│   ├── __init__.py
│   ├── llm_client.py              # LLM API integration (Groq/Gemini)
│   ├── rag_engine.py              # RAG functionality (NEW)
│   ├── code_executor.py           # Safe code execution
│   ├── prompts.py                 # Prompt templates (enhanced with RAG)
│   └── utils.py                   # Utility functions
├── components/                     # UI components
│   ├── __init__.py
│   ├── language_selector.py       # Language selection widgets
│   ├── code_display.py            # Code display components
│   ├── code_library_tab.py       # Code library management (NEW)
│   ├── code_search_tab.py        # Semantic search interface (NEW)
│   └── rag_settings.py           # RAG configuration (NEW)
├── extensions/                     # Additional features
│   ├── __init__.py
│   └── unit_test_generator.py    # Unit test generation
└── assets/                        # Static assets
    └── custom.css                 # Custom CSS styles
```

## Deployment

### Streamlit Cloud
1. Push your code to GitHub
2. Connect your repository to [Streamlit Cloud](https://streamlit.io/cloud)
3. Add your API keys in the Streamlit Cloud dashboard
4. Deploy automatically

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Run the app
streamlit run app.py
```

## Rate Limits

### Free Tier Limits
- **Groq**: 100 requests/minute
- **Gemini**: 15 requests/minute

### Solutions for Rate Limits
1. **Automatic Fallback**: The app automatically switches between APIs
2. **Manual Switch**: Use the model dropdown in the sidebar
3. **Wait**: Rate limits reset after a few minutes
4. **Upgrade**: Consider paid plans for higher limits

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

- **Issues**: Report bugs and feature requests on GitHub
- **Documentation**: Check the README and inline code comments
- **API Keys**: Ensure your API keys are correctly set in the .env file

## Changelog

### Version 2.0.0
- **RAG Integration**: Added Retrieval-Augmented Generation for personalized code generation
- **Code Library**: Upload and manage your own code files
- **Semantic Search**: Search your codebase using natural language queries
- **Grounded Generation**: Generate code that matches your coding style and patterns
- **Local Vector Database**: FAISS-based local storage for privacy
- **Enhanced Prompts**: RAG-enhanced prompts for better context-aware generation
- **Code Context**: Include relevant code snippets in generation and translation

### Version 1.0.0
- Initial release with core code generation features
- Support for 40+ programming languages
- Safe code execution for Python/SQL/Bash
- Automatic API fallback between Groq and Gemini
- Rate limit handling and user-friendly error messages 