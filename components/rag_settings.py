"""
RAG Settings Component
Provides configuration options for RAG functionality and system information.
"""

import streamlit as st
from typing import Dict, Any

def rag_settings_tab():
    """Main RAG settings tab for configuration and system info."""
    
    st.header("RAG Settings")
    st.markdown("Configure RAG behavior and view system information.")
    
    # RAG Mode Toggle
    st.subheader("RAG Configuration")
    
    # Enable/disable RAG mode
    rag_enabled = st.checkbox(
        "Enable RAG Mode",
        value=st.session_state.get('rag_enabled', False),
        help="When enabled, code generation will use your uploaded codebase for context and grounding"
    )
    st.session_state.rag_enabled = rag_enabled
    
    if rag_enabled:
        st.success("RAG Mode is enabled. Code generation will use your codebase for context.")
    else:
        st.warning("RAG Mode is disabled. Code generation will use standard LLM-only mode.")
    
    # RAG behavior settings
    if rag_enabled:
        st.subheader("RAG Behavior")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Number of context chunks to include
            context_chunks = st.slider(
                "Context Chunks",
                min_value=1,
                max_value=10,
                value=st.session_state.get('context_chunks', 3),
                help="Number of relevant code chunks to include in prompts"
            )
            st.session_state.context_chunks = context_chunks
            
            # Similarity threshold
            similarity_threshold = st.slider(
                "Similarity Threshold",
                min_value=0.0,
                max_value=1.0,
                value=st.session_state.get('similarity_threshold', 0.3),
                step=0.05,
                help="Minimum similarity score for including code chunks"
            )
            st.session_state.similarity_threshold = similarity_threshold
        
        with col2:
            # Context strategy
            context_strategy = st.selectbox(
                "Context Strategy",
                options=['automatic', 'manual', 'hybrid'],
                index=['automatic', 'manual', 'hybrid'].index(st.session_state.get('context_strategy', 'automatic')),
                help="How to select context for code generation"
            )
            st.session_state.context_strategy = context_strategy
            
            # Fallback behavior
            fallback_behavior = st.selectbox(
                "Fallback Behavior",
                options=['llm_only', 'use_any_context', 'error'],
                index=['llm_only', 'use_any_context', 'error'].index(st.session_state.get('fallback_behavior', 'llm_only')),
                help="What to do when no relevant context is found"
            )
            st.session_state.fallback_behavior = fallback_behavior
    
    # System Information
    st.subheader("System Information")
    
    # Check RAG engine status
    if 'rag_engine' in st.session_state:
        rag_engine = st.session_state.rag_engine
        stats = rag_engine.get_index_stats()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Indexed Chunks", stats['total_chunks'])
        
        with col2:
            st.metric("Files Processed", stats['files_processed'])
        
        with col3:
            st.metric("Index Size", stats['index_size'])
        
        # Index health
        if stats['total_chunks'] > 0:
            st.success("Code library is available and ready for RAG")
        else:
            st.warning("No code has been indexed yet")
    else:
        st.warning("RAG engine not initialized")
    
    # Model information
    st.subheader("Model Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Embedding Model:**")
        st.markdown("- Model: all-MiniLM-L6-v2")
        st.markdown("- Dimensions: 384")
        st.markdown("- Type: Sentence Transformers")
    
    with col2:
        st.markdown("**Vector Database:**")
        st.markdown("- Type: FAISS")
        st.markdown("- Index: FlatIP")
        st.markdown("- Storage: Local")
    
    # Performance settings
    st.subheader("Performance Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Cache embeddings
        cache_embeddings = st.checkbox(
            "Cache Embeddings",
            value=st.session_state.get('cache_embeddings', True),
            help="Cache embeddings for faster repeated searches"
        )
        st.session_state.cache_embeddings = cache_embeddings
        
        # Batch processing
        batch_size = st.number_input(
            "Batch Size",
            min_value=1,
            max_value=100,
            value=st.session_state.get('batch_size', 10),
            help="Number of files to process in a batch"
        )
        st.session_state.batch_size = batch_size
    
    with col2:
        # Search timeout
        search_timeout = st.number_input(
            "Search Timeout (seconds)",
            min_value=1,
            max_value=60,
            value=st.session_state.get('search_timeout', 10),
            help="Maximum time to wait for search results"
        )
        st.session_state.search_timeout = search_timeout
        
        # Max results
        max_results = st.number_input(
            "Max Search Results",
            min_value=1,
            max_value=100,
            value=st.session_state.get('max_results', 20),
            help="Maximum number of search results to return"
        )
        st.session_state.max_results = max_results
    
    # Advanced settings
    with st.expander("Advanced Settings"):
        st.markdown("""
        **Embedding Settings:**
        - Model: all-MiniLM-L6-v2 (optimized for code)
        - Normalization: L2 normalization
        - Similarity: Cosine similarity
        
        **Index Settings:**
        - Type: FAISS FlatIP (Inner Product)
        - Storage: Local filesystem
        - Persistence: Automatic save/load
        
        **Chunking Settings:**
        - Language-specific parsers
        - Function/class extraction
        - Docstring preservation
        - Line number tracking
        """)
    
    # Tips and best practices
    st.subheader("Best Practices")
    
    st.markdown("""
    **For Best RAG Performance:**
    
    **Upload Relevant Code:**
    - Include files that represent your coding style
    - Upload libraries and utilities you commonly use
    - Include both simple and complex examples
    
    **Effective Search Queries:**
    - Use specific function names or patterns
    - Include language-specific terms
    - Describe the functionality you need
    
    **Optimal Settings:**
    - Start with 3-5 context chunks
    - Use similarity threshold of 0.3-0.5
    - Enable automatic context strategy for most use cases
    
    **Monitoring:**
    - Check index statistics regularly
    - Clear old code when adding new files
    - Monitor search result quality
    """)
    
    # Troubleshooting
    with st.expander("Troubleshooting"):
        st.markdown("""
        **Common Issues:**
        
        **No search results:**
        - Check if files are properly uploaded and processed
        - Try more general search terms
        - Verify file types are supported
        
        **Poor code generation:**
        - Increase number of context chunks
        - Lower similarity threshold
        - Upload more relevant code files
        
        **Slow performance:**
        - Reduce batch size for large codebases
        - Clear old index and re-process
        - Check available memory
        
        **Index errors:**
        - Clear index and re-upload files
        - Check file encoding (UTF-8 recommended)
        - Verify file permissions
        """)

def get_rag_settings() -> Dict[str, Any]:
    """Get current RAG settings."""
    return {
        'enabled': st.session_state.get('rag_enabled', False),
        'context_chunks': st.session_state.get('context_chunks', 3),
        'similarity_threshold': st.session_state.get('similarity_threshold', 0.3),
        'context_strategy': st.session_state.get('context_strategy', 'automatic'),
        'fallback_behavior': st.session_state.get('fallback_behavior', 'llm_only'),
        'cache_embeddings': st.session_state.get('cache_embeddings', True),
        'batch_size': st.session_state.get('batch_size', 10),
        'search_timeout': st.session_state.get('search_timeout', 10),
        'max_results': st.session_state.get('max_results', 20)
    }

def is_rag_enabled() -> bool:
    """Check if RAG mode is enabled."""
    return st.session_state.get('rag_enabled', False) 