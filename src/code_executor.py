"""
Safe Code Execution Module for AnyLang AI Code Writer
Handles safe execution of Python, SQL, and Bash code with security sandboxing.
"""

import subprocess
import sqlite3
import tempfile
import os
import re
import logging
from typing import Dict, Any, Optional
from io import StringIO
import sys
import contextlib
from io import UnsupportedOperation

logger = logging.getLogger(__name__)

class CodeExecutor:
    """Safe code executor for Python, SQL, and Bash."""
    
    def __init__(self):
        self.dangerous_patterns = [
            r'import\s+os\s*$',
            r'import\s+subprocess\s*$',
            r'import\s+sys\s*$',
            r'__import__\s*\(',
            r'eval\s*\(',
            r'exec\s*\(',
            r'open\s*\(',
            r'file\s*\(',
            r'input\s*\(',
            r'raw_input\s*\(',
            r'rm\s+-rf',
            r'del\s+/',
            r'format\s+\(c:\s*\)',
            r'rmdir\s+/s',
            r'chmod\s+777',
            r'chown\s+root',
            r'DROP\s+DATABASE',
            r'DELETE\s+FROM\s+.*\s+WHERE\s+1\s*=\s*1',
            r'TRUNCATE\s+TABLE',
        ]
    
    def is_safe_to_execute(self, code: str, language: str) -> Dict[str, Any]:
        """
        Check if code is safe to execute.
        
        Args:
            code: Code to check
            language: Programming language
        
        Returns:
            Dict with safety assessment
        """
        # Check for dangerous patterns
        for pattern in self.dangerous_patterns:
            if re.search(pattern, code, re.IGNORECASE | re.MULTILINE):
                return {
                    "safe": False,
                    "reason": f"Potentially dangerous pattern detected: {pattern}",
                    "code": code,
                    "language": language
                }
        
        # Language-specific checks
        if language.lower() == "python":
            return self._check_python_safety(code)
        elif language.lower() == "sql":
            return self._check_sql_safety(code)
        elif language.lower() == "bash":
            return self._check_bash_safety(code)
        else:
            return {
                "safe": False,
                "reason": f"Execution not supported for {language}",
                "code": code,
                "language": language
            }
    
    def _check_python_safety(self, code: str) -> Dict[str, Any]:
        """Check Python code safety."""
        dangerous_imports = ['os', 'subprocess', 'sys', 'shutil', 'glob']
        dangerous_functions = ['eval', 'exec', 'compile', '__import__']
        
        # Check for dangerous imports
        for imp in dangerous_imports:
            if re.search(rf'import\s+{imp}', code, re.IGNORECASE):
                return {
                    "safe": False,
                    "reason": f"Dangerous import detected: {imp}",
                    "code": code,
                    "language": "python"
                }
        
        # Check for dangerous functions
        for func in dangerous_functions:
            if re.search(rf'{func}\s*\(', code, re.IGNORECASE):
                return {
                    "safe": False,
                    "reason": f"Dangerous function detected: {func}",
                    "code": code,
                    "language": "python"
                }
        
        return {
            "safe": True,
            "reason": "Code appears safe for execution",
            "code": code,
            "language": "python"
        }
    
    def _check_sql_safety(self, code: str) -> Dict[str, Any]:
        """Check SQL code safety."""
        dangerous_patterns = [
            r'DROP\s+DATABASE',
            r'DELETE\s+FROM\s+.*\s+WHERE\s+1\s*=\s*1',
            r'TRUNCATE\s+TABLE',
            r'ALTER\s+TABLE',
            r'CREATE\s+TABLE',
            r'DROP\s+TABLE',
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                return {
                    "safe": False,
                    "reason": f"Dangerous SQL pattern detected: {pattern}",
                    "code": code,
                    "language": "sql"
                }
        
        return {
            "safe": True,
            "reason": "SQL code appears safe for execution",
            "code": code,
            "language": "sql"
        }
    
    def _check_bash_safety(self, code: str) -> Dict[str, Any]:
        """Check Bash code safety."""
        dangerous_commands = [
            'rm -rf',
            'del /',
            'format c:',
            'rmdir /s',
            'chmod 777',
            'chown root',
        ]
        
        for cmd in dangerous_commands:
            if cmd.lower() in code.lower():
                return {
                    "safe": False,
                    "reason": f"Dangerous command detected: {cmd}",
                    "code": code,
                    "language": "bash"
                }
        
        return {
            "safe": True,
            "reason": "Bash code appears safe for execution",
            "code": code,
            "language": "bash"
        }
    
    def execute_code(self, code: str, language: str) -> Dict[str, Any]:
        """
        Execute code safely.
        
        Args:
            code: Code to execute
            language: Programming language
        
        Returns:
            Dict with execution results
        """
        try:
            # Check if code is safe
            safety_check = self.is_safe_to_execute(code, language)
            if not safety_check["safe"]:
                return {
                    "success": False,
                    "output": f"Safety check failed: {safety_check['reason']}",
                    "error": safety_check["reason"],
                    "language": language
                }
            
            # Execute based on language
            if language.lower() == "python":
                return self._execute_python(code)
            elif language.lower() == "sql":
                return self._execute_sql(code)
            elif language.lower() == "bash":
                return self._execute_bash(code)
            else:
                return {
                    "success": False,
                    "output": f"Language {language} not supported for execution",
                    "error": f"Unsupported language: {language}",
                    "language": language
                }
                
        except Exception as e:
            return {
                "success": False,
                "output": f"Execution error: {str(e)}",
                "error": str(e),
                "language": language
            }
    
    def _execute_python(self, code: str) -> Dict[str, Any]:
        """Execute Python code safely."""
        output_buffer = StringIO()
        error_buffer = StringIO()
        
        try:
            with contextlib.redirect_stdout(output_buffer), contextlib.redirect_stderr(error_buffer):
                # Create a restricted globals dict
                restricted_globals = {
                    '__builtins__': {
                        'print': print,
                        'len': len,
                        'range': range,
                        'list': list,
                        'dict': dict,
                        'set': set,
                        'tuple': tuple,
                        'str': str,
                        'int': int,
                        'float': float,
                        'bool': bool,
                        'type': type,
                        'isinstance': isinstance,
                        'hasattr': hasattr,
                        'getattr': getattr,
                        'setattr': setattr,
                        'dir': dir,
                        'help': help,
                        'abs': abs,
                        'max': max,
                        'min': min,
                        'sum': sum,
                        'sorted': sorted,
                        'reversed': reversed,
                        'enumerate': enumerate,
                        'zip': zip,
                        'map': map,
                        'filter': filter,
                        'any': any,
                        'all': all,
                        'round': round,
                        'divmod': divmod,
                        'pow': pow,
                        'bin': bin,
                        'hex': hex,
                        'oct': oct,
                        'ord': ord,
                        'chr': chr,
                        'repr': repr,
                        'ascii': ascii,
                        'format': format,
                        'hash': hash,
                        'id': id,
                        'callable': callable,
                        'issubclass': issubclass,
                        'super': super,
                        'property': property,
                        'staticmethod': staticmethod,
                        'classmethod': classmethod,
                        'object': object,
                        'Exception': Exception,
                        'ValueError': ValueError,
                        'TypeError': TypeError,
                        'IndexError': IndexError,
                        'KeyError': KeyError,
                        'AttributeError': AttributeError,
                        'RuntimeError': RuntimeError,
                        'StopIteration': StopIteration,
                        'GeneratorExit': GeneratorExit,
                        'SystemExit': SystemExit,
                        'KeyboardInterrupt': KeyboardInterrupt,
                        'ImportError': ImportError,
                        'ModuleNotFoundError': ModuleNotFoundError,
                        'OSError': OSError,
                        'FileNotFoundError': FileNotFoundError,
                        'PermissionError': PermissionError,
                        'TimeoutError': TimeoutError,
                        'ConnectionError': ConnectionError,
                        'BlockingIOError': BlockingIOError,
                        'ChildProcessError': ChildProcessError,
                        'BrokenPipeError': BrokenPipeError,
                        'ConnectionAbortedError': ConnectionAbortedError,
                        'ConnectionRefusedError': ConnectionRefusedError,
                        'ConnectionResetError': ConnectionResetError,
                        'FileExistsError': FileExistsError,
                        'IsADirectoryError': IsADirectoryError,
                        'NotADirectoryError': NotADirectoryError,
                        'InterruptedError': InterruptedError,
                        'ProcessLookupError': ProcessLookupError,
                        'ZeroDivisionError': ZeroDivisionError,
                        'OverflowError': OverflowError,
                        'FloatingPointError': FloatingPointError,
                        'ArithmeticError': ArithmeticError,
                        'BufferError': BufferError,
                        'LookupError': LookupError,
                        'AssertionError': AssertionError,
                        'EOFError': EOFError,
                        'ImportWarning': ImportWarning,
                        'PendingDeprecationWarning': PendingDeprecationWarning,
                        'RuntimeWarning': RuntimeWarning,
                        'SyntaxWarning': SyntaxWarning,
                        'UserWarning': UserWarning,
                        'FutureWarning': FutureWarning,
                        'DeprecationWarning': DeprecationWarning,
                        'ResourceWarning': ResourceWarning,
                        'UnboundLocalError': UnboundLocalError,
                        'NameError': NameError,
                        'UnboundLocalError': UnboundLocalError,
                        'SyntaxError': SyntaxError,
                        'IndentationError': IndentationError,
                        'TabError': TabError,
                        'SystemError': SystemError,
                        'ReferenceError': ReferenceError,
                        'MemoryError': MemoryError,
                        'RecursionError': RecursionError,
                        'NotImplementedError': NotImplementedError,
                        'OSError': OSError,
                        'BlockingIOError': BlockingIOError,
                        'ChildProcessError': ChildProcessError,
                        'ConnectionError': ConnectionError,
                        'BrokenPipeError': BrokenPipeError,
                        'ConnectionAbortedError': ConnectionAbortedError,
                        'ConnectionRefusedError': ConnectionRefusedError,
                        'ConnectionResetError': ConnectionResetError,
                        'FileExistsError': FileExistsError,
                        'FileNotFoundError': FileNotFoundError,
                        'IsADirectoryError': IsADirectoryError,
                        'NotADirectoryError': NotADirectoryError,
                        'InterruptedError': InterruptedError,
                        'PermissionError': PermissionError,
                        'ProcessLookupError': ProcessLookupError,
                        'TimeoutError': TimeoutError,
                        'UnsupportedOperation': UnsupportedOperation,
                    }
                }
                
                # Execute the code
                exec(code, restricted_globals)
                
                # Get output
                output = output_buffer.getvalue()
                error_output = error_buffer.getvalue()
                
                # If no output but code executed successfully, try to get the result
                if not output and not error_output:
                    # Try to evaluate the last expression if it's a simple one
                    lines = code.strip().split('\n')
                    if lines:
                        last_line = lines[-1].strip()
                        # If the last line looks like a function call or expression
                        if '(' in last_line and ')' in last_line and not last_line.startswith('#'):
                            try:
                                result = eval(last_line, restricted_globals)
                                output = f"Result: {result}"
                            except:
                                output = "Code executed successfully (no output)"
                        else:
                            output = "Code executed successfully (no output)"
                elif not output:
                    output = "Code executed successfully (no output)"
                
                return {
                    "success": True,
                    "output": output,
                    "error": error_output if error_output else None,
                    "language": "python"
                }
                
        except Exception as e:
            error_output = error_buffer.getvalue()
            return {
                "success": False,
                "output": f"Python execution error: {str(e)}",
                "error": error_output if error_output else str(e),
                "language": "python"
            }
    
    def _execute_sql(self, code: str) -> Dict[str, Any]:
        """Execute SQL code safely using in-memory SQLite."""
        try:
            # Create in-memory database
            conn = sqlite3.connect(':memory:')
            cursor = conn.cursor()
            
            # Create some sample tables for testing
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    email TEXT,
                    age INTEGER
                )
            ''')
            
            cursor.execute('''
                INSERT INTO users (name, email, age) VALUES 
                ('Alice', 'alice@example.com', 25),
                ('Bob', 'bob@example.com', 30),
                ('Charlie', 'charlie@example.com', 35)
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    price REAL,
                    category TEXT
                )
            ''')
            
            cursor.execute('''
                INSERT INTO products (name, price, category) VALUES 
                ('Laptop', 999.99, 'Electronics'),
                ('Book', 19.99, 'Books'),
                ('Phone', 599.99, 'Electronics')
            ''')
            
            conn.commit()
            
            # Execute the user's SQL
            cursor.execute(code)
            
            # Get results
            try:
                results = cursor.fetchall()
                columns = [description[0] for description in cursor.description] if cursor.description else []
                
                # Format results
                if results:
                    output = "Results:\n"
                    if columns:
                        output += " | ".join(columns) + "\n"
                        output += "-" * (len(" | ".join(columns))) + "\n"
                    for row in results:
                        output += " | ".join(str(cell) for cell in row) + "\n"
                else:
                    output = "Query executed successfully (no results to display)"
                
                return {
                    "success": True,
                    "output": output,
                    "error": None,
                    "language": "sql"
                }
            except sqlite3.OperationalError as e:
                return {
                    "success": False,
                    "output": f"SQL error: {str(e)}",
                    "error": str(e),
                    "language": "sql"
                }
        except Exception as e:
            return {
                "success": False,
                "output": f"SQL execution error: {str(e)}",
                "error": str(e),
                "language": "sql"
            }
        finally:
            if 'conn' in locals():
                conn.close()
    
    def _execute_bash(self, code: str) -> Dict[str, Any]:
        """Execute Bash code safely with restrictions."""
        try:
            # Only allow safe commands
            safe_commands = ['echo', 'cat', 'ls', 'pwd', 'whoami', 'date', 'cal', 'bc', 'expr']
            
            # Check if code contains only safe commands
            lines = code.strip().split('\n')
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split()
                    if parts and parts[0] not in safe_commands:
                        return {
                            "success": False,
                            "output": f"Unsafe command detected: {parts[0]}",
                            "error": f"Command '{parts[0]}' is not allowed for security reasons",
                            "language": "bash"
                        }
            
            # Execute with timeout and restrictions
            result = subprocess.run(
                ['bash', '-c', code],
                capture_output=True,
                text=True,
                timeout=10,  # 10 second timeout
                cwd='/tmp'  # Safe working directory
            )
            
            output = result.stdout
            error = result.stderr
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "output": output if output else "Command executed successfully (no output)",
                    "error": error if error else None,
                    "language": "bash"
                }
            else:
                return {
                    "success": False,
                    "output": f"Bash error (exit code {result.returncode}): {error}",
                    "error": error,
                    "language": "bash"
                }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "output": "Command timed out after 10 seconds",
                "error": "Timeout",
                "language": "bash"
            }
        except Exception as e:
            return {
                "success": False,
                "output": f"Bash execution error: {str(e)}",
                "error": str(e),
                "language": "bash"
            } 