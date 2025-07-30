"""
RAG Engine for AnyLang AI Code Writer
Handles code chunking, embedding generation, vector storage, and retrieval.
"""

import os
import re
import ast
import json
import logging
import zipfile
import tempfile
import shutil
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

logger = logging.getLogger(__name__)

class CodeChunker:
    """Handles code parsing and chunking for different programming languages."""
    
    def __init__(self):
        self.supported_extensions = {
            '.py': self._parse_python,
            '.js': self._parse_javascript,
            '.ts': self._parse_typescript,
            '.java': self._parse_java,
            '.cpp': self._parse_cpp,
            '.cs': self._parse_csharp,
            '.rs': self._parse_rust,
            '.go': self._parse_go,
            '.php': self._parse_php,
            '.rb': self._parse_ruby,
            '.swift': self._parse_swift,
            '.kt': self._parse_kotlin,
            '.scala': self._parse_scala,
            '.dart': self._parse_dart,
            '.r': self._parse_r,
            '.m': self._parse_matlab,
            '.sql': self._parse_sql,
            '.sh': self._parse_bash,
            '.html': self._parse_html,
            '.css': self._parse_css,
            '.vue': self._parse_vue,
            '.jsx': self._parse_jsx,
            '.tsx': self._parse_tsx
        }
    
    def chunk_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Chunk a single file into logical code blocks."""
        file_path = Path(file_path)
        extension = file_path.suffix.lower()
        
        if extension not in self.supported_extensions:
            return self._parse_generic(file_path)
        
        try:
            return self.supported_extensions[extension](file_path)
        except Exception as e:
            logger.warning(f"Failed to parse {file_path}: {e}")
            return self._parse_generic(file_path)
    
    def _parse_python(self, file_path: Path) -> List[Dict[str, Any]]:
        """Parse Python file into functions, classes, and modules."""
        chunks = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    chunk = {
                        'type': 'function',
                        'name': node.name,
                        'code': ast.unparse(node),
                        'start_line': node.lineno,
                        'end_line': node.end_lineno if hasattr(node, 'end_lineno') else node.lineno,
                        'docstring': ast.get_docstring(node) or ''
                    }
                    chunks.append(chunk)
                
                elif isinstance(node, ast.ClassDef):
                    chunk = {
                        'type': 'class',
                        'name': node.name,
                        'code': ast.unparse(node),
                        'start_line': node.lineno,
                        'end_line': node.end_lineno if hasattr(node, 'end_lineno') else node.lineno,
                        'docstring': ast.get_docstring(node) or ''
                    }
                    chunks.append(chunk)
            
            # If no functions/classes found, create a module chunk
            if not chunks:
                chunks.append({
                    'type': 'module',
                    'name': file_path.stem,
                    'code': content,
                    'start_line': 1,
                    'end_line': len(content.split('\n')),
                    'docstring': ''
                })
                
        except Exception as e:
            logger.error(f"Error parsing Python file {file_path}: {e}")
            # Fallback to generic parsing
            return self._parse_generic(file_path)
        
        return chunks
    
    def _parse_javascript(self, file_path: Path) -> List[Dict[str, Any]]:
        """Parse JavaScript file into functions and classes."""
        return self._parse_generic_with_regex(file_path, [
            r'(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*\([^)]*\)\s*\{[^}]*\}',
            r'(?:export\s+)?class\s+(\w+)\s*\{[^}]*\}',
            r'const\s+(\w+)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>\s*\{[^}]*\}',
            r'let\s+(\w+)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>\s*\{[^}]*\}',
            r'var\s+(\w+)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>\s*\{[^}]*\}'
        ])
    
    def _parse_typescript(self, file_path: Path) -> List[Dict[str, Any]]:
        """Parse TypeScript file (similar to JavaScript but with types)."""
        return self._parse_javascript(file_path)
    
    def _parse_java(self, file_path: Path) -> List[Dict[str, Any]]:
        """Parse Java file into classes and methods."""
        return self._parse_generic_with_regex(file_path, [
            r'(?:public\s+)?class\s+(\w+)\s*\{[^}]*\}',
            r'(?:public\s+|private\s+|protected\s+)?(?:static\s+)?(?:final\s+)?(?:synchronized\s+)?(?:native\s+)?(?:abstract\s+)?(?:default\s+)?(?:<[^>]*>\s+)?(?:[\w\[\]<>]+\s+)?(\w+)\s*\([^)]*\)\s*\{[^}]*\}'
        ])
    
    def _parse_cpp(self, file_path: Path) -> List[Dict[str, Any]]:
        """Parse C++ file into classes and functions."""
        return self._parse_generic_with_regex(file_path, [
            r'class\s+(\w+)\s*\{[^}]*\}',
            r'(?:template\s*<[^>]*>\s*)?(?:inline\s+)?(?:static\s+)?(?:const\s+)?(?:virtual\s+)?(?:explicit\s+)?(?:[\w:<>]+\s+)?(\w+)\s*\([^)]*\)\s*\{[^}]*\}'
        ])
    
    def _parse_csharp(self, file_path: Path) -> List[Dict[str, Any]]:
        """Parse C# file into classes and methods."""
        return self._parse_generic_with_regex(file_path, [
            r'(?:public\s+|private\s+|protected\s+|internal\s+)?(?:abstract\s+)?(?:sealed\s+)?(?:partial\s+)?(?:static\s+)?class\s+(\w+)\s*\{[^}]*\}',
            r'(?:public\s+|private\s+|protected\s+|internal\s+)?(?:virtual\s+)?(?:override\s+)?(?:abstract\s+)?(?:static\s+)?(?:async\s+)?(?:[\w<>]+\s+)?(\w+)\s*\([^)]*\)\s*\{[^}]*\}'
        ])
    
    def _parse_rust(self, file_path: Path) -> List[Dict[str, Any]]:
        """Parse Rust file into functions and structs."""
        return self._parse_generic_with_regex(file_path, [
            r'fn\s+(\w+)\s*\([^)]*\)\s*\{[^}]*\}',
            r'struct\s+(\w+)\s*\{[^}]*\}',
            r'impl\s+(\w+)\s*\{[^}]*\}'
        ])
    
    def _parse_go(self, file_path: Path) -> List[Dict[str, Any]]:
        """Parse Go file into functions and structs."""
        return self._parse_generic_with_regex(file_path, [
            r'func\s+(\w+)\s*\([^)]*\)\s*\{[^}]*\}',
            r'type\s+(\w+)\s+struct\s*\{[^}]*\}'
        ])
    
    def _parse_php(self, file_path: Path) -> List[Dict[str, Any]]:
        """Parse PHP file into functions and classes."""
        return self._parse_generic_with_regex(file_path, [
            r'function\s+(\w+)\s*\([^)]*\)\s*\{[^}]*\}',
            r'class\s+(\w+)\s*\{[^}]*\}'
        ])
    
    def _parse_ruby(self, file_path: Path) -> List[Dict[str, Any]]:
        """Parse Ruby file into methods and classes."""
        return self._parse_generic_with_regex(file_path, [
            r'def\s+(\w+)[^}]*end',
            r'class\s+(\w+)[^}]*end'
        ])
    
    def _parse_swift(self, file_path: Path) -> List[Dict[str, Any]]:
        """Parse Swift file into functions and classes."""
        return self._parse_generic_with_regex(file_path, [
            r'func\s+(\w+)\s*\([^)]*\)\s*\{[^}]*\}',
            r'class\s+(\w+)\s*\{[^}]*\}',
            r'struct\s+(\w+)\s*\{[^}]*\}'
        ])
    
    def _parse_kotlin(self, file_path: Path) -> List[Dict[str, Any]]:
        """Parse Kotlin file into functions and classes."""
        return self._parse_generic_with_regex(file_path, [
            r'fun\s+(\w+)\s*\([^)]*\)\s*\{[^}]*\}',
            r'class\s+(\w+)\s*\{[^}]*\}',
            r'data\s+class\s+(\w+)\s*\([^)]*\)'
        ])
    
    def _parse_scala(self, file_path: Path) -> List[Dict[str, Any]]:
        """Parse Scala file into functions and classes."""
        return self._parse_generic_with_regex(file_path, [
            r'def\s+(\w+)\s*\([^)]*\)\s*\{[^}]*\}',
            r'class\s+(\w+)\s*\{[^}]*\}',
            r'object\s+(\w+)\s*\{[^}]*\}'
        ])
    
    def _parse_dart(self, file_path: Path) -> List[Dict[str, Any]]:
        """Parse Dart file into functions and classes."""
        return self._parse_generic_with_regex(file_path, [
            r'(?:void\s+|int\s+|String\s+|bool\s+|double\s+|dynamic\s+)?(\w+)\s*\([^)]*\)\s*\{[^}]*\}',
            r'class\s+(\w+)\s*\{[^}]*\}'
        ])
    
    def _parse_r(self, file_path: Path) -> List[Dict[str, Any]]:
        """Parse R file into functions."""
        return self._parse_generic_with_regex(file_path, [
            r'(\w+)\s*<-\s*function\s*\([^)]*\)\s*\{[^}]*\}'
        ])
    
    def _parse_matlab(self, file_path: Path) -> List[Dict[str, Any]]:
        """Parse MATLAB file into functions."""
        return self._parse_generic_with_regex(file_path, [
            r'function\s+(\w+)\s*\([^)]*\)[^}]*end'
        ])
    
    def _parse_sql(self, file_path: Path) -> List[Dict[str, Any]]:
        """Parse SQL file into statements."""
        return self._parse_generic_with_regex(file_path, [
            r'(?:CREATE|INSERT|UPDATE|DELETE|SELECT)\s+[^;]+;'
        ])
    
    def _parse_bash(self, file_path: Path) -> List[Dict[str, Any]]:
        """Parse Bash file into functions."""
        return self._parse_generic_with_regex(file_path, [
            r'(\w+)\s*\(\)\s*\{[^}]*\}'
        ])
    
    def _parse_html(self, file_path: Path) -> List[Dict[str, Any]]:
        """Parse HTML file into sections."""
        return self._parse_generic_with_regex(file_path, [
            r'<[^>]+>[^<]*</[^>]+>',
            r'<[^>]+/>'
        ])
    
    def _parse_css(self, file_path: Path) -> List[Dict[str, Any]]:
        """Parse CSS file into rules."""
        return self._parse_generic_with_regex(file_path, [
            r'[^{}]+\{[^}]*\}'
        ])
    
    def _parse_vue(self, file_path: Path) -> List[Dict[str, Any]]:
        """Parse Vue file into template, script, and style sections."""
        return self._parse_generic_with_regex(file_path, [
            r'<template>[^<]*</template>',
            r'<script>[^<]*</script>',
            r'<style>[^<]*</style>'
        ])
    
    def _parse_jsx(self, file_path: Path) -> List[Dict[str, Any]]:
        """Parse JSX file into components."""
        return self._parse_generic_with_regex(file_path, [
            r'(?:export\s+)?(?:default\s+)?(?:function\s+)?(\w+)\s*\([^)]*\)\s*\{[^}]*\}',
            r'(?:export\s+)?(?:default\s+)?class\s+(\w+)\s*\{[^}]*\}'
        ])
    
    def _parse_tsx(self, file_path: Path) -> List[Dict[str, Any]]:
        """Parse TSX file (similar to JSX but with TypeScript)."""
        return self._parse_jsx(file_path)
    
    def _parse_generic_with_regex(self, file_path: Path, patterns: List[str]) -> List[Dict[str, Any]]:
        """Parse file using regex patterns."""
        chunks = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            for pattern in patterns:
                matches = re.finditer(pattern, content, re.DOTALL | re.MULTILINE)
                for match in matches:
                    chunk = {
                        'type': 'code_block',
                        'name': match.group(1) if match.groups() else f"block_{len(chunks)}",
                        'code': match.group(0),
                        'start_line': content[:match.start()].count('\n') + 1,
                        'end_line': content[:match.end()].count('\n') + 1,
                        'docstring': ''
                    }
                    chunks.append(chunk)
            
            # If no matches found, create a single chunk
            if not chunks:
                chunks.append({
                    'type': 'file',
                    'name': file_path.stem,
                    'code': content,
                    'start_line': 1,
                    'end_line': len(content.split('\n')),
                    'docstring': ''
                })
                
        except Exception as e:
            logger.error(f"Error parsing file {file_path}: {e}")
            return self._parse_generic(file_path)
        
        return chunks
    
    def _parse_generic(self, file_path: Path) -> List[Dict[str, Any]]:
        """Generic parser for unsupported file types."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return [{
                'type': 'file',
                'name': file_path.stem,
                'code': content,
                'start_line': 1,
                'end_line': len(content.split('\n')),
                'docstring': ''
            }]
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return []

class RAGEngine:
    """Main RAG engine for code search and retrieval."""
    
    def __init__(self, storage_path: str = "code_library"):
        """Initialize RAG engine with storage paths."""
        self.storage_path = Path(storage_path)
        self.embeddings_path = self.storage_path / "embeddings"
        self.vector_db_path = self.storage_path / "vector_db"
        self.user_uploads_path = self.storage_path / "user_uploads"
        
        # Create directories if they don't exist
        self.storage_path.mkdir(exist_ok=True)
        self.embeddings_path.mkdir(exist_ok=True)
        self.vector_db_path.mkdir(exist_ok=True)
        self.user_uploads_path.mkdir(exist_ok=True)
        
        # Initialize components
        self.chunker = CodeChunker()
        
        # Initialize the embedding model with error handling
        try:
            logger.info("Loading SentenceTransformer model...")
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("SentenceTransformer model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load SentenceTransformer model: {e}")
            raise RuntimeError(f"Failed to initialize embedding model: {e}. This might be due to network issues or insufficient memory.")
        
        self.index = None
        self.metadata = []
        
        # Load existing index
        self._load_index()
    
    def _load_index(self):
        """Load existing FAISS index and metadata."""
        # Define index and metadata paths
        self.index_path = self.vector_db_path / "faiss_index.bin"
        self.metadata_path = self.vector_db_path / "metadata.json"
        
        try:
            if self.index_path.exists() and self.metadata_path.exists():
                self.index = faiss.read_index(str(self.index_path))
                with open(self.metadata_path, 'r') as f:
                    self.metadata = json.load(f)
                logger.info(f"Loaded existing index with {len(self.metadata)} chunks")
            else:
                # Create new index
                dimension = self.model.get_sentence_embedding_dimension()
                self.index = faiss.IndexFlatIP(dimension)
                self.metadata = []
                logger.info("Created new FAISS index")
        except Exception as e:
            logger.error(f"Error loading index: {e}")
            dimension = self.model.get_sentence_embedding_dimension()
            self.index = faiss.IndexFlatIP(dimension)
            self.metadata = []
    
    def _save_index(self):
        """Save FAISS index and metadata."""
        try:
            faiss.write_index(self.index, str(self.index_path))
            with open(self.metadata_path, 'w') as f:
                json.dump(self.metadata, f, indent=2)
            logger.info("Index saved successfully")
        except Exception as e:
            logger.error(f"Error saving index: {e}")
    
    def process_uploaded_files(self, uploaded_files: List[Any]) -> Dict[str, Any]:
        """Process uploaded files and add them to the vector database."""
        processed_files = []
        total_chunks = 0
        
        for uploaded_file in uploaded_files:
            try:
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name
                
                # Process the file
                file_result = self._process_single_file(tmp_path, uploaded_file.name)
                processed_files.append(file_result)
                total_chunks += file_result['chunks_added']
                
                # Clean up temporary file
                os.unlink(tmp_path)
                
            except Exception as e:
                logger.error(f"Error processing file {uploaded_file.name}: {e}")
                processed_files.append({
                    'filename': uploaded_file.name,
                    'status': 'error',
                    'error': str(e),
                    'chunks_added': 0
                })
        
        # Save the updated index
        self._save_index()
        
        return {
            'processed_files': processed_files,
            'total_chunks_added': total_chunks,
            'total_chunks_in_index': len(self.metadata)
        }
    
    def _process_single_file(self, file_path: str, original_name: str) -> Dict[str, Any]:
        """Process a single file and add its chunks to the index."""
        file_path = Path(file_path)
        
        # Check if it's a supported file type
        if file_path.suffix.lower() not in self.chunker.supported_extensions:
            return {
                'filename': original_name,
                'status': 'skipped',
                'reason': 'Unsupported file type',
                'chunks_added': 0
            }
        
        # Chunk the file
        chunks = self.chunker.chunk_file(file_path)
        
        if not chunks:
            return {
                'filename': original_name,
                'status': 'error',
                'error': 'No chunks extracted',
                'chunks_added': 0
            }
        
        # Generate embeddings and add to index
        chunks_added = 0
        for chunk in chunks:
            try:
                # Create text representation for embedding
                text_for_embedding = f"{chunk['name']} {chunk['type']} {chunk['code']}"
                
                # Generate embedding
                embedding = self.model.encode([text_for_embedding])[0]
                
                # Add to FAISS index
                self.index.add(np.array([embedding], dtype=np.float32))
                
                # Store metadata
                chunk_metadata = {
                    'filename': original_name,
                    'file_path': str(file_path),
                    'chunk_type': chunk['type'],
                    'chunk_name': chunk['name'],
                    'code': chunk['code'],
                    'start_line': chunk['start_line'],
                    'end_line': chunk['end_line'],
                    'docstring': chunk['docstring'],
                    'index_id': len(self.metadata)
                }
                self.metadata.append(chunk_metadata)
                chunks_added += 1
                
            except Exception as e:
                logger.error(f"Error processing chunk {chunk['name']}: {e}")
        
        return {
            'filename': original_name,
            'status': 'success',
            'chunks_added': chunks_added,
            'total_chunks': len(chunks)
        }
    
    def search_code(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search for relevant code chunks using semantic similarity."""
        if not self.metadata or self.index is None:
            return []
        
        try:
            # Generate query embedding
            query_embedding = self.model.encode([query])[0]
            
            # Search the index
            scores, indices = self.index.search(
                np.array([query_embedding], dtype=np.float32), 
                min(top_k, len(self.metadata))
            )
            
            # Return results with metadata
            results = []
            for score, idx in zip(scores[0], indices[0]):
                if idx < len(self.metadata):
                    result = self.metadata[idx].copy()
                    result['similarity_score'] = float(score)
                    results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching code: {e}")
            return []
    
    def get_code_context(self, query: str, top_k: int = 3) -> str:
        """Get relevant code context for LLM prompts."""
        results = self.search_code(query, top_k)
        
        if not results:
            return ""
        
        context_parts = []
        for i, result in enumerate(results, 1):
            context_parts.append(f"Code Example {i} (from {result['filename']}):")
            context_parts.append(f"Function/Class: {result['chunk_name']}")
            if result['docstring']:
                context_parts.append(f"Description: {result['docstring']}")
            context_parts.append(f"Code:\n{result['code']}\n")
        
        return "\n".join(context_parts)
    
    def clear_index(self):
        """Clear the entire index."""
        try:
            dimension = self.model.get_sentence_embedding_dimension()
            self.index = faiss.IndexFlatIP(dimension)
            self.metadata = []
            self._save_index()
            logger.info("Index cleared successfully")
        except Exception as e:
            logger.error(f"Error clearing index: {e}")
    
    def get_index_stats(self) -> Dict[str, Any]:
        """Get statistics about the current index."""
        return {
            'total_chunks': len(self.metadata),
            'index_size': self.index.ntotal if self.index else 0,
            'files_processed': len(set(chunk['filename'] for chunk in self.metadata))
        } 