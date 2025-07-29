"""
Unit Test Generator Extension for AnyLang AI Code Writer
Generates unit tests for code using LLM.
"""

import streamlit as st
from src.llm_client import LLMClient
from src.prompts import UNIT_TEST_PROMPT, format_prompt

def generate_unit_tests(code: str, language: str, model: str = "groq") -> dict:
    """
    Generate unit tests for the given code.
    
    Args:
        code: Code to generate tests for
        language: Programming language
        model: LLM model to use
    
    Returns:
        Dict with generated tests and metadata
    """
    llm_client = LLMClient()
    
    # Create prompt
    prompt = format_prompt(UNIT_TEST_PROMPT, language=language, code=code)
    
    try:
        # Use the generate_code method which handles the correct models
        result = llm_client.generate_code(prompt, language, model)
        return result
    except Exception as e:
        return {
            "code": f"# Error generating unit tests: {str(e)}",
            "language": language,
            "model": model,
            "error": str(e)
        }

def display_unit_test_generator():
    """Display the unit test generator interface."""
    st.header("Unit Test Generator")
    
    # Code input
    code = st.text_area(
        "Paste code to generate tests for:",
        placeholder="Paste the code you want to generate unit tests for...",
        height=200,
        key="unit_test_input"
    )
    
    # Language selection
    from components.language_selector import language_selector_with_default
    language = language_selector_with_default("python", "unit_test_language")
    
    # Generate button
    if st.button("Generate Unit Tests", type="primary", key="unit_test_btn"):
        if not code:
            st.warning("Please paste some code to generate tests for.")
        elif not language:
            st.warning("Please select a programming language.")
        else:
            with st.spinner("Generating unit tests..."):
                try:
                    result = generate_unit_tests(code, language)
                    
                    if "error" in result:
                        st.error(f"Failed to generate unit tests: {result['error']}")
                    else:
                        from components.code_display import display_code
                        display_code(result["code"], language, "Generated Unit Tests")
                        
                        # Show metadata
                        with st.expander("Test Generation Details", expanded=False):
                            st.write(f"**Model:** {result.get('model', 'Unknown')}")
                            if result.get('tokens_used'):
                                st.write(f"**Tokens Used:** {result['tokens_used']}")
                            st.write(f"**Language:** {language.title()}")
                        
                except Exception as e:
                    st.error(f"Error generating unit tests: {str(e)}") 