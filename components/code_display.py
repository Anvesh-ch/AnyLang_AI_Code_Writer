"""
Code Display Component for AnyLang AI Code Writer
Provides syntax highlighting and copy functionality for code.
"""

import streamlit as st
from src.utils import clean_code, get_file_extension, create_download_filename

def display_code(code: str, language: str, title: str = "Generated Code", show_copy: bool = True, show_download: bool = True):
    """
    Display code with syntax highlighting and copy/download options.
    
    Args:
        code: Code to display
        language: Programming language for syntax highlighting
        title: Title for the code section
        show_copy: Whether to show copy button
        show_download: Whether to show download button
    """
    if not code:
        st.warning("No code to display.")
        return
    
    # Clean the code
    cleaned_code = clean_code(code)
    
    # Create columns for buttons
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        st.subheader(title)
    
    with col2:
        if show_copy:
            if st.button("Copy", key=f"copy_{title.lower().replace(' ', '_')}"):
                st.write("```" + language + "\n" + cleaned_code + "\n```")
                st.success("Code copied to clipboard!")
    
    with col3:
        if show_download:
            if st.button("Download", key=f"download_{title.lower().replace(' ', '_')}"):
                filename = create_download_filename(language, title)
                st.download_button(
                    label="Save File",
                    data=cleaned_code,
                    file_name=filename,
                    mime="text/plain",
                    key=f"save_{title.lower().replace(' ', '_')}"
                )
    
    # Display code using Streamlit's built-in syntax highlighting
    st.code(cleaned_code, language=language)

def display_code_with_execution(code: str, language: str, title: str = "Generated Code"):
    """
    Display code with execution option for supported languages.
    
    Args:
        code: Code to display
        language: Programming language
        title: Title for the code section
    """
    from src.utils import is_executable_language
    from src.code_executor import CodeExecutor
    
    # Display the code
    display_code(code, language, title)
    
    # Add execution option for supported languages
    if is_executable_language(language):
        st.markdown("---")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            execute_button = st.button("Run Code", key=f"execute_{title.lower().replace(' ', '_')}")
        
        with col2:
            st.info(f"This {language.title()} code can be executed safely within the app.")
        
        if execute_button:
            with st.spinner("Executing code..."):
                executor = CodeExecutor()
                result = executor.execute_code(code, language)
                
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
    else:
        st.info(f"{language.title()} code cannot be executed safely. You can copy and run it in your local environment.")

def display_code_comparison(code1: str, code2: str, language1: str, language2: str, 
                          title1: str = "Original Code", title2: str = "Translated Code"):
    """
    Display two code blocks side by side for comparison.
    
    Args:
        code1: First code block
        code2: Second code block
        language1: Language of first code block
        language2: Language of second code block
        title1: Title for first code block
        title2: Title for second code block
    """
    col1, col2 = st.columns(2)
    
    with col1:
        display_code(code1, language1, title1)
    
    with col2:
        display_code(code2, language2, title2)

def display_code_with_metadata(code: str, language: str, metadata: dict, title: str = "Generated Code"):
    """
    Display code with additional metadata.
    
    Args:
        code: Code to display
        language: Programming language
        metadata: Additional metadata (model, tokens, etc.)
        title: Title for the code section
    """
    # Display the code
    display_code(code, language, title)
    
    # Display metadata
    if metadata:
        with st.expander("Code Generation Details", expanded=False):
            if "model" in metadata:
                st.write(f"**Model:** {metadata['model']}")
            if "tokens_used" in metadata and metadata["tokens_used"]:
                st.write(f"**Tokens Used:** {metadata['tokens_used']}")
            if "language" in metadata:
                st.write(f"**Language:** {metadata['language']}")
            if "error" in metadata:
                st.error(f"**Error:** {metadata['error']}")

def display_error_message(error: str, title: str = "Error"):
    """
    Display error message in a formatted way.
    
    Args:
        error: Error message
        title: Title for the error section
    """
    st.error(f"{title}")
    st.code(error, language="text")
    
    # Provide helpful suggestions
    st.info("Troubleshooting Tips:")
    st.markdown("""
    - Check your API keys in the .env file
    - Ensure you have a stable internet connection
    - Try a simpler or more specific request
    - Check if the selected language is supported
    """)

def display_success_message(message: str, title: str = "Success"):
    """
    Display success message.
    
    Args:
        message: Success message
        title: Title for the success section
    """
    st.success(f"{title}")
    st.info(message) 