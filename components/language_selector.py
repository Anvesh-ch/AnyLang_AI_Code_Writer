"""
Language Selector Component for AnyLang AI Code Writer
Provides a dropdown for selecting programming languages.
"""

import streamlit as st
from src.utils import get_supported_languages, get_language_keys

def language_selector(key: str = "language_selector") -> str:
    """
    Create a language selector dropdown.
    
    Args:
        key: Unique key for the Streamlit component
    
    Returns:
        Selected language key
    """
    languages = get_supported_languages()
    
    # Add a default option
    options = ["Select a language..."] + languages
    
    selected = st.selectbox(
        "Choose Programming Language",
        options,
        key=key,
        help="Select the programming language for code generation"
    )
    
    if selected == "Select a language...":
        return ""
    
    # Convert display name back to key
    from src.utils import get_language_key
    return get_language_key(selected)

def language_selector_with_default(default_language: str = "python", key: str = "language_selector") -> str:
    """
    Create a language selector with a default value.
    
    Args:
        default_language: Default language to select
        key: Unique key for the Streamlit component
    
    Returns:
        Selected language key
    """
    languages = get_supported_languages()
    
    # Find the default language display name
    from src.utils import get_language_name
    default_display = get_language_name(default_language)
    
    selected = st.selectbox(
        "Choose Programming Language",
        languages,
        index=languages.index(default_display) if default_display in languages else 0,
        key=key,
        help="Select the programming language for code generation"
    )
    
    # Convert display name back to key
    from src.utils import get_language_key
    return get_language_key(selected)

def dual_language_selector(source_key: str = "source_language", target_key: str = "target_language") -> tuple:
    """
    Create two language selectors for translation.
    
    Args:
        source_key: Key for source language selector
        target_key: Key for target language selector
    
    Returns:
        Tuple of (source_language, target_language)
    """
    col1, col2 = st.columns(2)
    
    with col1:
        source_language = language_selector_with_default("python", source_key)
    
    with col2:
        target_language = language_selector_with_default("javascript", target_key)
    
    return source_language, target_language

def language_info_display(language: str):
    """
    Display information about the selected language.
    
    Args:
        language: Language key
    """
    if not language:
        return
    
    from src.utils import get_language_info
    info = get_language_info(language)
    
    with st.expander(f"ℹ️ About {info['name']}", expanded=False):
        st.write(f"**Description:** {info['description']}")
        st.write(f"**File Extension:** {info['extension']}")
        st.write(f"**Safe Execution:** {'✅ Supported' if info['executable'] else '❌ Not supported'}")
        
        if info['executable']:
            st.info("This language supports safe code execution within the app.")
        else:
            st.warning("This language doesn't support safe execution. You can still generate and view code.") 