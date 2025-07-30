"""
Code Library Tab Component
Handles file uploads, processing, and management of user's codebase for RAG functionality.
"""

import streamlit as st
import pandas as pd
from typing import List, Dict, Any
from src.rag_engine import RAGEngine

def code_library_tab():
    """Main code library tab for file uploads and management."""
    
    st.header("Code Library")
    st.markdown("Upload your code files to enable RAG-powered code generation and search.")
    
    # Initialize RAG engine
    if 'rag_engine' not in st.session_state:
        st.session_state.rag_engine = RAGEngine()
    
    rag_engine = st.session_state.rag_engine
    
    # File upload section
    st.subheader("Upload Code Files")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_files = st.file_uploader(
            "Choose code files to upload",
            type=['py', 'js', 'ts', 'java', 'cpp', 'cs', 'rs', 'go', 'php', 'rb', 
                  'swift', 'kt', 'scala', 'dart', 'r', 'm', 'sql', 'sh', 'html', 
                  'css', 'vue', 'jsx', 'tsx'],
            accept_multiple_files=True,
            help="Supported file types: Python, JavaScript, TypeScript, Java, C++, C#, Rust, Go, PHP, Ruby, Swift, Kotlin, Scala, Dart, R, MATLAB, SQL, Bash, HTML, CSS, Vue, JSX, TSX"
        )
    
    with col2:
        st.markdown("**Supported Languages:**")
        st.markdown("""
        - Python (.py)
        - JavaScript (.js, .jsx)
        - TypeScript (.ts, .tsx)
        - Java (.java)
        - C++ (.cpp)
        - C# (.cs)
        - Rust (.rs)
        - Go (.go)
        - PHP (.php)
        - Ruby (.rb)
        - Swift (.swift)
        - Kotlin (.kt)
        - Scala (.scala)
        - Dart (.dart)
        - R (.r)
        - MATLAB (.m)
        - SQL (.sql)
        - Bash (.sh)
        - HTML (.html)
        - CSS (.css)
        - Vue (.vue)
        """)
    
    # Process uploaded files
    if uploaded_files:
        if st.button("Process Files", type="primary"):
            with st.spinner("Processing files and generating embeddings..."):
                result = rag_engine.process_uploaded_files(uploaded_files)
                
                # Display results
                st.success(f"Processed {len(uploaded_files)} files!")
                st.info(f"Added {result['total_chunks_added']} code chunks to the index")
                
                # Show detailed results
                with st.expander("Processing Details"):
                    for file_result in result['processed_files']:
                        if file_result['status'] == 'success':
                            st.success(f"{file_result['filename']}: {file_result['chunks_added']} chunks added")
                        elif file_result['status'] == 'skipped':
                            st.warning(f"{file_result['filename']}: {file_result['reason']}")
                        else:
                            st.error(f"{file_result['filename']}: {file_result['error']}")
    
    # Index statistics
    st.subheader("Code Library Statistics")
    
    stats = rag_engine.get_index_stats()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Code Chunks", stats['total_chunks'])
    
    with col2:
        st.metric("Files Processed", stats['files_processed'])
    
    with col3:
        st.metric("Index Size", stats['index_size'])
    
    # Index management
    st.subheader("Index Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Clear Index", type="secondary"):
            if st.checkbox("I understand this will delete all indexed code"):
                rag_engine.clear_index()
                st.success("Index cleared successfully!")
                st.rerun()
    
    with col2:
        if st.button("Refresh Index", type="secondary"):
            st.info("Index refreshed!")
            st.rerun()
    
    # Show indexed files (if any)
    if stats['total_chunks'] > 0:
        st.subheader("Indexed Files")
        
        # Get unique files from metadata
        files_info = {}
        for chunk in rag_engine.metadata:
            filename = chunk['filename']
            if filename not in files_info:
                files_info[filename] = {
                    'chunks': 0,
                    'types': set()
                }
            files_info[filename]['chunks'] += 1
            files_info[filename]['types'].add(chunk['chunk_type'])
        
        # Create DataFrame for display
        files_data = []
        for filename, info in files_info.items():
            files_data.append({
                'Filename': filename,
                'Chunks': info['chunks'],
                'Types': ', '.join(sorted(info['types']))
            })
        
        if files_data:
            df = pd.DataFrame(files_data)
            st.dataframe(df, use_container_width=True)
    
    # Tips and information
    st.subheader("Tips")
    st.markdown("""
    - **Upload multiple files**: You can upload multiple files at once to build a comprehensive code library
    - **Supported formats**: The system automatically parses functions, classes, and modules from your code
    - **Privacy**: All code and embeddings are stored locally on your machine
    - **Performance**: Larger codebases may take longer to process initially
    - **RAG Mode**: Once you have uploaded code, enable RAG mode in other tabs for grounded code generation
    """)

def display_code_search_results(results: List[Dict[str, Any]]):
    """Display code search results in a formatted way."""
    
    if not results:
        st.info("No relevant code found. Try a different search query.")
        return
    
    for i, result in enumerate(results, 1):
        with st.expander(f"{result['filename']} - {result['chunk_name']} (Score: {result['similarity_score']:.3f})"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**Type:** {result['chunk_type']}")
                st.markdown(f"**Function/Class:** {result['chunk_name']}")
                if result['docstring']:
                    st.markdown(f"**Description:** {result['docstring']}")
                st.markdown(f"**Lines:** {result['start_line']}-{result['end_line']}")
            
            with col2:
                if st.button(f"Copy Code {i}", key=f"copy_{i}"):
                    st.session_state.copied_code = result['code']
                    st.success("Code copied to clipboard!")
            
            # Display the code
            st.code(result['code'], language='python')
            
            # Add to generation context button
            if st.button(f"Add to Context {i}", key=f"context_{i}"):
                if 'selected_context' not in st.session_state:
                    st.session_state.selected_context = []
                st.session_state.selected_context.append(result)
                st.success(f"Added {result['chunk_name']} to generation context!")

def get_selected_context() -> List[Dict[str, Any]]:
    """Get the currently selected context for code generation."""
    return st.session_state.get('selected_context', [])

def clear_selected_context():
    """Clear the selected context."""
    if 'selected_context' in st.session_state:
        del st.session_state.selected_context 