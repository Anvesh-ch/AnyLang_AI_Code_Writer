"""
AnyLang AI Code Writer - Main Application
A Streamlit web application that converts natural language to code in any programming language.
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

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AnyLang AI Code Writer",
    page_icon="🤖",
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
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function."""
    
    # Header
    st.markdown('<h1 class="main-header">🤖 AnyLang AI Code Writer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Transform natural language into working code in any programming language</p>', unsafe_allow_html=True)
    
    # Initialize LLM client
    llm_client = LLMClient()
    
    # Check if any LLM is available
    if not llm_client.is_available():
        st.error("❌ No LLM clients available. Please check your API keys in the `.env` file.")
        st.info("""
        **Setup Instructions:**
        1. Create a `.env` file in the project root
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
        st.header("⚙️ Settings")
        
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
        
        # Language info
        st.header("ℹ️ Language Info")
        language_info_display(st.session_state.get("current_language", ""))
        
        # Features
        st.header("🚀 Features")
        st.markdown("""
        - **Code Generation**: Natural language to code
        - **Code Translation**: Convert between languages
        - **Code Explanation**: Line-by-line explanations
        - **Safe Execution**: Run Python/SQL/Bash code
        - **Syntax Highlighting**: Beautiful code display
        - **Copy & Download**: Easy code sharing
        """)
    
    # Main content
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Code Generation", "🔄 Code Translation", "📖 Code Explanation", "⚡ Code Execution"])
    
    # Tab 1: Code Generation
    with tab1:
        st.header("🎯 Generate Code from Natural Language")
        
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
        
        # Generate button
        if st.button("🚀 Generate Code", type="primary", key="generate_btn"):
            if not task:
                st.warning("Please enter a task description.")
            elif not language:
                st.warning("Please select a programming language.")
            else:
                with st.spinner("Generating code..."):
                    try:
                        result = llm_client.generate_code(task, language, selected_model)
                        
                        if "error" in result:
                            display_error_message(result["error"], "Code Generation Failed")
                        else:
                            display_code_with_execution(
                                result["code"], 
                                language, 
                                f"Generated {language.title()} Code"
                            )
                            
                            # Show metadata
                            with st.expander("📊 Generation Details", expanded=False):
                                st.write(f"**Model:** {result.get('model', 'Unknown')}")
                                if result.get('tokens_used'):
                                    st.write(f"**Tokens Used:** {result['tokens_used']}")
                                st.write(f"**Language:** {language.title()}")
                            
                            # Store in session state for other tabs
                            st.session_state["generated_code"] = result["code"]
                            st.session_state["generated_language"] = language
                            
                    except Exception as e:
                        display_error_message(str(e), "Code Generation Error")
    
    # Tab 2: Code Translation
    with tab2:
        st.header("🔄 Translate Code Between Languages")
        
        # Language selection
        source_lang, target_lang = dual_language_selector("trans_source", "trans_target")
        
        # Code input
        source_code = st.text_area(
            "Paste your code here:",
            placeholder="Paste the code you want to translate...",
            height=200,
            key="translation_input"
        )
        
        # Translate button
        if st.button("🔄 Translate Code", type="primary", key="translate_btn"):
            if not source_code:
                st.warning("Please paste some code to translate.")
            elif not source_lang or not target_lang:
                st.warning("Please select both source and target languages.")
            elif source_lang == target_lang:
                st.warning("Source and target languages must be different.")
            else:
                with st.spinner("Translating code..."):
                    try:
                        result = llm_client.translate_code(source_code, source_lang, target_lang, selected_model)
                        
                        if "error" in result:
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
                            with st.expander("📊 Translation Details", expanded=False):
                                st.write(f"**Model:** {result.get('model', 'Unknown')}")
                                if result.get('tokens_used'):
                                    st.write(f"**Tokens Used:** {result['tokens_used']}")
                                st.write(f"**From:** {source_lang.title()}")
                                st.write(f"**To:** {target_lang.title()}")
                            
                    except Exception as e:
                        display_error_message(str(e), "Translation Error")
    
    # Tab 3: Code Explanation
    with tab3:
        st.header("📖 Explain Code Line by Line")
        
        # Code input
        code_to_explain = st.text_area(
            "Paste code to explain:",
            placeholder="Paste the code you want explained...",
            height=200,
            key="explanation_input"
        )
        
        # Language for explanation
        explain_language = language_selector_with_default("python", "explain_language")
        
        # Explain button
        if st.button("📖 Explain Code", type="primary", key="explain_btn"):
            if not code_to_explain:
                st.warning("Please paste some code to explain.")
            elif not explain_language:
                st.warning("Please select the programming language.")
            else:
                with st.spinner("Generating explanation..."):
                    try:
                        result = llm_client.explain_code(code_to_explain, explain_language, selected_model)
                        
                        if "error" in result:
                            display_error_message(result["error"], "Explanation Failed")
                        else:
                            # Display the original code
                            display_code(code_to_explain, explain_language, "Original Code")
                            
                            # Display explanation
                            st.subheader("📖 Code Explanation")
                            st.markdown(result["explanation"])
                            
                            # Show metadata
                            with st.expander("📊 Explanation Details", expanded=False):
                                st.write(f"**Model:** {result.get('model', 'Unknown')}")
                                if result.get('tokens_used'):
                                    st.write(f"**Tokens Used:** {result['tokens_used']}")
                                st.write(f"**Language:** {explain_language.title()}")
                            
                    except Exception as e:
                        display_error_message(str(e), "Explanation Error")
    
    # Tab 4: Code Execution
    with tab4:
        st.header("⚡ Execute Code Safely")
        
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
            st.info(f"✅ {exec_language.title()} code can be executed safely within the app.")
        else:
            st.warning(f"❌ {exec_language.title()} code cannot be executed safely.")
            return
        
        # Execute button
        if st.button("⚡ Execute Code", type="primary", key="execute_btn"):
            if not code_to_execute:
                st.warning("Please paste some code to execute.")
            else:
                with st.spinner("Executing code..."):
                    try:
                        executor = CodeExecutor()
                        result = executor.execute_code(code_to_execute, exec_language)
                        
                        if result["success"]:
                            st.success("✅ Code executed successfully!")
                            st.subheader("Output:")
                            st.code(result["output"], language="text")
                            
                            if result.get("error"):
                                st.warning("⚠️ Warnings/Errors:")
                                st.code(result["error"], language="text")
                        else:
                            st.error("❌ Code execution failed!")
                            st.code(result["output"], language="text")
                            
                    except Exception as e:
                        display_error_message(str(e), "Execution Error")

if __name__ == "__main__":
    main() 