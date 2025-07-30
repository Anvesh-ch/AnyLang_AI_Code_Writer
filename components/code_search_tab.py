"""
Code Search Tab Component
Provides semantic search functionality for the user's uploaded codebase.
"""

import streamlit as st
from typing import List, Dict, Any
from components.code_library_tab import display_code_search_results

def code_search_tab():
    """Main code search tab for semantic code search."""
    
    st.header("Semantic Code Search")
    st.markdown("Search your uploaded codebase using natural language queries.")
    
    # Check if RAG engine is available
    if 'rag_engine' not in st.session_state:
        st.warning("No code library found. Please upload some code files first in the Code Library tab.")
        return
    
    rag_engine = st.session_state.rag_engine
    
    # Check if there's any indexed code
    stats = rag_engine.get_index_stats()
    if stats['total_chunks'] == 0:
        st.warning("No code has been indexed yet. Please upload and process some code files in the Code Library tab.")
        return
    
    # Search interface
    st.subheader("Search Your Codebase")
    
    # Search query input
    search_query = st.text_input(
        "Enter your search query",
        placeholder="e.g., 'Show all functions for data cleaning', 'Find recursive algorithms', 'Database connection code'",
        help="Use natural language to describe what you're looking for in your codebase"
    )
    
    # Search options
    col1, col2 = st.columns(2)
    
    with col1:
        top_k = st.slider("Number of results", min_value=1, max_value=20, value=5, help="Maximum number of results to return")
    
    with col2:
        search_button = st.button("Search", type="primary")
    
    # Example queries
    with st.expander("Example Search Queries"):
        st.markdown("""
        **Function/Feature Search:**
        - "Show all functions for data cleaning"
        - "Find authentication functions"
        - "Database connection code"
        - "API endpoint handlers"
        
        **Algorithm/Pattern Search:**
        - "Recursive algorithms"
        - "Sorting functions"
        - "Binary search implementation"
        - "Tree traversal code"
        
        **Language-Specific Search:**
        - "Python decorators"
        - "JavaScript async functions"
        - "React components"
        - "SQL queries"
        
        **Error Handling:**
        - "Exception handling code"
        - "Error logging functions"
        - "Try-catch blocks"
        
        **Data Processing:**
        - "CSV file processing"
        - "JSON parsing functions"
        - "Data validation code"
        """)
    
    # Perform search
    if search_button and search_query:
        with st.spinner("Searching your codebase..."):
            results = rag_engine.search_code(search_query, top_k)
            
            if results:
                st.success(f"Found {len(results)} relevant code snippets")
                
                # Display results
                display_code_search_results(results)
                
                # Show search statistics
                with st.expander("Search Statistics"):
                    st.markdown(f"**Query:** {search_query}")
                    st.markdown(f"**Results found:** {len(results)}")
                    if results:
                        avg_score = sum(r['similarity_score'] for r in results) / len(results)
                        st.markdown(f"**Average similarity score:** {avg_score:.3f}")
                        
                        # Show file distribution
                        files = {}
                        for result in results:
                            filename = result['filename']
                            files[filename] = files.get(filename, 0) + 1
                        
                        st.markdown("**Results by file:**")
                        for filename, count in files.items():
                            st.markdown(f"- {filename}: {count} results")
            else:
                st.info("No relevant code found for your query. Try a different search term.")
    
    # Recent searches (if any)
    if 'recent_searches' in st.session_state and st.session_state.recent_searches:
        st.subheader("Recent Searches")
        
        for i, (query, results_count) in enumerate(st.session_state.recent_searches[-5:]):
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"**{query}**")
            
            with col2:
                st.markdown(f"{results_count} results")
            
            with col3:
                if st.button(f"Search Again {i}", key=f"recent_{i}"):
                    st.session_state.search_query = query
                    st.rerun()
    
    # Advanced search options
    with st.expander("Advanced Search Options"):
        st.markdown("""
        **Search Tips:**
        - Use specific terms related to your codebase
        - Include function names, class names, or file types
        - Describe the functionality you're looking for
        - Use technical terms that might appear in your code
        
        **Search works best when:**
        - You have uploaded relevant code files
        - Your code has meaningful function/class names
        - You use descriptive search terms
        - Your codebase is well-structured
        """)
    
    # Code context management
    st.subheader("Selected Context")
    
    selected_context = st.session_state.get('selected_context', [])
    
    if selected_context:
        st.info(f"You have {len(selected_context)} code snippets selected for use in code generation.")
        
        # Show selected context
        for i, context_item in enumerate(selected_context):
            with st.expander(f"{context_item['filename']} - {context_item['chunk_name']}"):
                st.code(context_item['code'], language='python')
                if st.button(f"Remove {i}", key=f"remove_context_{i}"):
                    selected_context.pop(i)
                    st.rerun()
        
        # Clear all context
        if st.button("Clear All Context"):
            st.session_state.selected_context = []
            st.rerun()
    else:
        st.info("No code snippets selected. Use the 'Add to Context' buttons in search results to include code in generation.")

def get_search_context(query: str, top_k: int = 3) -> str:
    """Get search context for a query to use in code generation."""
    if 'rag_engine' not in st.session_state:
        return ""
    
    rag_engine = st.session_state.rag_engine
    return rag_engine.get_code_context(query, top_k) 