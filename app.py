"""
AnyLang AI Code Writer - Main Application
A Streamlit web application that converts natural language requests into working code in any programming language.
"""

import streamlit as st
import os
from dotenv import load_dotenv
from src.llm_client import LLMClient
from src.code_executor import CodeExecutor
from src.utils import clean_code, format_error_message
from components.language_selector import language_selector, language_selector_with_default, dual_language_selector, language_info_display
from components.code_display import (
    display_code, display_code_with_execution, display_code_comparison,
    display_code_with_metadata, display_error_message, display_success_message
)

# Import RAG components with error handling
try:
    from components.code_library_tab import code_library_tab
    from components.code_search_tab import code_search_tab
    from components.rag_settings import rag_settings_tab
    RAG_AVAILABLE = True
except ImportError as e:
    RAG_AVAILABLE = False
    # Create placeholder functions
    def code_library_tab():
        st.error("Code Library component not available")
        st.info("RAG features require additional dependencies. Please check the installation.")
    def code_search_tab():
        st.error("Code Search component not available")
        st.info("RAG features require additional dependencies. Please check the installation.")
    def rag_settings_tab():
        st.error("RAG Settings component not available")
        st.info("RAG features require additional dependencies. Please check the installation.")

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AnyLang AI Code Writer",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .rate-limit-info {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 0.5rem;
        padding: 0.75rem;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function."""
    
    # Header
    st.markdown('<h1 class="main-header">AnyLang AI Code Writer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Transform natural language into working code in any programming language</p>', unsafe_allow_html=True)
    
    # Initialize LLM client
    llm_client = LLMClient()
    
    # Check if any LLM is available
    if not llm_client.is_available():
        st.error("No LLM clients available. Please check your API keys in the .env file.")
        st.info("""
        **Setup Instructions:**
        1. Create a .env file in the project root
        2. Add your API keys:
           ```
           GROQ_API_KEY=your_groq_api_key_here
           GEMINI_API_KEY=your_gemini_api_key_here
           ```
        3. Restart the application
        """)
        return
    
    # Sidebar
    with st.sidebar:
        st.header("Settings")
        
        # Model selection
        available_models = llm_client.get_available_models()
        if len(available_models) > 1:
            selected_model = st.selectbox(
                "Choose LLM Model",
                available_models,
                index=0,
                help="Select which LLM to use for code generation"
            )
        else:
            selected_model = available_models[0] if available_models else "groq"
        
        st.info(f"Using: {selected_model.title()}")
        
        # Rate limit information
        st.header("Rate Limits")
        rate_info = llm_client.get_rate_limit_info()
        st.markdown(f"""
        <div class="rate-limit-info">
        <strong>Free Tier Limits:</strong><br>
        • <strong>Groq:</strong> {rate_info['groq_free_tier']}<br>
        • <strong>Gemini:</strong> {rate_info['gemini_free_tier']}<br>
        <br>
        <strong>Tip:</strong> Switch models in the dropdown if you hit limits!
        </div>
        """, unsafe_allow_html=True)
        
        # Language info
        st.header("Language Info")
        language_info_display(st.session_state.get("current_language", ""))
        
        # Features
        st.header("Features")
        st.markdown("""
        - **Code Generation**: Natural language to code
        - **Code Translation**: Convert between languages
        - **Code Explanation**: Line-by-line explanations
        - **Safe Execution**: Run Python/SQL/Bash code
        - **Syntax Highlighting**: Beautiful code display
        - **Copy & Download**: Easy code sharing
        - **Auto Fallback**: Switches models if one fails
        """)
    
    # Main content
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "Code Generation", "Code Translation", "Code Explanation", "Code Execution", 
        "Code Library", "Semantic Search", "RAG Settings"
    ])
    
    # Tab 1: Code Generation
    with tab1:
        st.header("Generate Code from Natural Language")
        
        # Language selection
        language = language_selector_with_default("python", "gen_language")
        st.session_state["current_language"] = language
        
        # Task input
        task = st.text_area(
            "Describe what you want to code:",
            placeholder="e.g., Create a function to reverse a linked list, or Build a simple calculator with addition and subtraction",
            height=100,
            key="task_input"
        )
        
        # RAG Settings for Code Generation
        rag_enabled = st.session_state.get('rag_enabled', False)
        
        if rag_enabled and 'rag_engine' in st.session_state:
            rag_engine = st.session_state.rag_engine
            stats = rag_engine.get_index_stats()
            
            if stats['total_chunks'] > 0:
                st.success(f"RAG Mode Enabled - Using {stats['total_chunks']} code chunks for context")
                
                # RAG context options
                col1, col2 = st.columns(2)
                with col1:
                    use_rag = st.checkbox("Use RAG Context", value=True, help="Include relevant code from your codebase")
                with col2:
                    context_chunks = st.slider("Context Chunks", 1, 5, 3, help="Number of relevant code chunks to include")
            else:
                st.warning("RAG Mode enabled but no code indexed. Upload code in the Code Library tab.")
                use_rag = False
                context_chunks = 3
        else:
            use_rag = False
            context_chunks = 3
        
        # Generate button
        if st.button("Generate Code", type="primary", key="generate_btn"):
            if not task:
                st.warning("Please enter a task description.")
            elif not language:
                st.warning("Please select a programming language.")
            else:
                with st.spinner("Generating code..."):
                    try:
                        # Get RAG context if enabled
                        rag_context = ""
                        if use_rag and 'rag_engine' in st.session_state:
                            rag_engine = st.session_state.rag_engine
                            rag_context = rag_engine.get_code_context(task, context_chunks)
                        
                        result = llm_client.generate_code(task, language, selected_model, use_rag, rag_context)
                        
                        if "error" in result:
                            # Check if it's a rate limit error
                            if "quota" in result["error"].lower() or "429" in result["error"]:
                                st.error("Rate Limit Exceeded")
                                st.info("""
                                **Solutions:**
                                1. **Wait a few minutes** and try again
                                2. **Switch to the other model** in the sidebar
                                3. **Upgrade your API plan** for higher limits
                                """)
                                st.code(result["error"], language="text")
                            else:
                                display_error_message(result["error"], "Code Generation Failed")
                        else:
                            display_code_with_execution(
                                result["code"], 
                                language, 
                                f"Generated {language.title()} Code"
                            )
                            
                            # Show metadata
                            with st.expander("Generation Details", expanded=False):
                                st.write(f"**Model:** {result.get('model', 'Unknown')}")
                                if result.get('tokens_used'):
                                    st.write(f"**Tokens Used:** {result['tokens_used']}")
                                st.write(f"**Language:** {language.title()}")
                                if result.get('rag_used'):
                                    st.write(f"**RAG Used:** Yes")
                                    if rag_context:
                                        st.write(f"**Context Chunks:** {context_chunks}")
                            
                            # Store in session state for other tabs
                            st.session_state["generated_code"] = result["code"]
                            st.session_state["generated_language"] = language
                            
                    except Exception as e:
                        display_error_message(str(e), "Code Generation Error")
    
    # Tab 2: Code Translation
    with tab2:
        st.header("Translate Code Between Languages")
        
        # Language selection
        source_lang, target_lang = dual_language_selector("trans_source", "trans_target")
        
        # Code input
        source_code = st.text_area(
            "Paste your code here:",
            placeholder="Paste the code you want to translate...",
            height=200,
            key="translation_input"
        )
        
        # RAG Settings for Code Translation
        rag_enabled = st.session_state.get('rag_enabled', False)
        
        if rag_enabled and 'rag_engine' in st.session_state:
            rag_engine = st.session_state.rag_engine
            stats = rag_engine.get_index_stats()
            
            if stats['total_chunks'] > 0:
                st.success(f"RAG Mode Enabled - Using {stats['total_chunks']} code chunks for context")
                use_rag = st.checkbox("Use RAG Context", value=True, help="Include relevant code from your codebase", key="trans_rag")
            else:
                st.warning("RAG Mode enabled but no code indexed. Upload code in the Code Library tab.")
                use_rag = False
        else:
            use_rag = False
        
        # Translate button
        if st.button("Translate Code", type="primary", key="translate_btn"):
            if not source_code:
                st.warning("Please paste some code to translate.")
            elif not source_lang or not target_lang:
                st.warning("Please select both source and target languages.")
            elif source_lang == target_lang:
                st.warning("Source and target languages must be different.")
            else:
                with st.spinner("Translating code..."):
                    try:
                        # Get RAG context if enabled
                        rag_context = ""
                        if use_rag and 'rag_engine' in st.session_state:
                            rag_engine = st.session_state.rag_engine
                            rag_context = rag_engine.get_code_context(f"translate from {source_lang} to {target_lang}", 3)
                        
                        result = llm_client.translate_code(source_code, source_lang, target_lang, selected_model, use_rag, rag_context)
                        
                        if "error" in result:
                            if "quota" in result["error"].lower() or "429" in result["error"]:
                                st.error("Rate Limit Exceeded")
                                st.info("Try switching models or wait a few minutes.")
                                st.code(result["error"], language="text")
                            else:
                                display_error_message(result["error"], "Translation Failed")
                        else:
                            # Display comparison
                            display_code_comparison(
                                source_code,
                                result["translated_code"],
                                source_lang,
                                target_lang,
                                f"Original {source_lang.title()} Code",
                                f"Translated {target_lang.title()} Code"
                            )
                            
                            # Show metadata
                            with st.expander("Translation Details", expanded=False):
                                st.write(f"**Model:** {result.get('model', 'Unknown')}")
                                if result.get('tokens_used'):
                                    st.write(f"**Tokens Used:** {result['tokens_used']}")
                                st.write(f"**From:** {source_lang.title()}")
                                st.write(f"**To:** {target_lang.title()}")
                                if result.get('rag_used'):
                                    st.write(f"**RAG Used:** Yes")
                            
                    except Exception as e:
                        display_error_message(str(e), "Translation Error")
    
    # Tab 3: Code Explanation
    with tab3:
        st.header("Explain Code Line by Line")
        
        # Code input
        code_to_explain = st.text_area(
            "Paste code to explain:",
            placeholder="Paste the code you want explained...",
            height=200,
            key="explanation_input"
        )
        
        # Language for explanation
        explain_language = language_selector_with_default("python", "explain_language")
        
        # RAG Settings for Code Explanation
        rag_enabled = st.session_state.get('rag_enabled', False)
        
        if rag_enabled and 'rag_engine' in st.session_state:
            rag_engine = st.session_state.rag_engine
            stats = rag_engine.get_index_stats()
            
            if stats['total_chunks'] > 0:
                st.success(f"RAG Mode Enabled - Using {stats['total_chunks']} code chunks for context")
                use_rag = st.checkbox("Use RAG Context", value=True, help="Include relevant code from your codebase", key="explain_rag")
            else:
                st.warning("RAG Mode enabled but no code indexed. Upload code in the Code Library tab.")
                use_rag = False
        else:
            use_rag = False
        
        # Explain button
        if st.button("Explain Code", type="primary", key="explain_btn"):
            if not code_to_explain:
                st.warning("Please paste some code to explain.")
            elif not explain_language:
                st.warning("Please select the programming language.")
            else:
                with st.spinner("Generating explanation..."):
                    try:
                        # Get RAG context if enabled
                        rag_context = ""
                        if use_rag and 'rag_engine' in st.session_state:
                            rag_engine = st.session_state.rag_engine
                            rag_context = rag_engine.get_code_context(f"explain {explain_language} code", 3)
                        
                        result = llm_client.explain_code(code_to_explain, explain_language, selected_model, use_rag, rag_context)
                        
                        if "error" in result:
                            if "quota" in result["error"].lower() or "429" in result["error"]:
                                st.error("Rate Limit Exceeded")
                                st.info("Try switching models or wait a few minutes.")
                                st.code(result["error"], language="text")
                            else:
                                display_error_message(result["error"], "Explanation Failed")
                        else:
                            # Display the original code
                            display_code(code_to_explain, explain_language, "Original Code")
                            
                            # Display explanation
                            st.subheader("Code Explanation")
                            # The LLM client returns the explanation in the "code" field
                            explanation_text = result.get("code", result.get("explanation", "No explanation available"))
                            st.markdown(explanation_text)
                            
                            # Show metadata
                            with st.expander("Explanation Details", expanded=False):
                                st.write(f"**Model:** {result.get('model', 'Unknown')}")
                                if result.get('tokens_used'):
                                    st.write(f"**Tokens Used:** {result['tokens_used']}")
                                st.write(f"**Language:** {explain_language.title()}")
                                if result.get('rag_used'):
                                    st.write(f"**RAG Used:** Yes")
                            
                    except Exception as e:
                        display_error_message(str(e), "Explanation Error")
    
    # Tab 4: Code Execution
    with tab4:
        st.header("Execute Code Safely")
        
        from src.utils import is_executable_language
        
        # Code input
        code_to_execute = st.text_area(
            "Paste code to execute:",
            placeholder="Paste Python, SQL, or Bash code to execute safely...",
            height=200,
            key="execution_input"
        )
        
        # Language selection for execution
        exec_language = st.selectbox(
            "Select language:",
            ["python", "sql", "bash"],
            key="exec_language"
        )
        
        # Execution info
        if is_executable_language(exec_language):
            st.info(f"{exec_language.title()} code can be executed safely within the app.")
        else:
            st.warning(f"{exec_language.title()} code cannot be executed safely.")
            return
        
        # Execute button
        if st.button("Execute Code", type="primary", key="execute_btn"):
            if not code_to_execute:
                st.warning("Please paste some code to execute.")
            else:
                with st.spinner("Executing code..."):
                    try:
                        executor = CodeExecutor()
                        result = executor.execute_code(code_to_execute, exec_language)
                        
                        if result["success"]:
                            st.success("Code executed successfully!")
                            st.subheader("Output:")
                            st.code(result["output"], language="text")
                            
                            if result.get("error"):
                                st.warning("Warnings/Errors:")
                                st.code(result["error"], language="text")
                        else:
                            st.error("Code execution failed!")
                            st.code(result["output"], language="text")
                            
                    except Exception as e:
                        display_error_message(str(e), "Execution Error")
    
    # Tab 5: Code Library
    with tab5:
        code_library_tab()
    
    # Tab 6: Semantic Search
    with tab6:
        from components.code_search_tab import code_search_tab
        code_search_tab()
    
    # Tab 7: RAG Settings
    with tab7:
        from components.rag_settings import rag_settings_tab
        rag_settings_tab()

if __name__ == "__main__":
    main() 