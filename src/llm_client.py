"""
LLM Client Module for AnyLang AI Code Writer
Handles API interactions with Groq and Gemini for code generation tasks.
"""

import os
import logging
from typing import Optional, Dict, Any
from dotenv import load_dotenv
import groq
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMClient:
    """Client for interacting with LLM APIs (Groq and Gemini)."""
    
    def __init__(self):
        self.groq_client = None
        self.gemini_client = None
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize API clients."""
        # Initialize Groq client
        groq_api_key = os.getenv('GROQ_API_KEY')
        if groq_api_key:
            try:
                self.groq_client = groq.Groq(api_key=groq_api_key)
                logger.info("Groq client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Groq client: {e}")
        
        # Initialize Gemini client
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        if gemini_api_key:
            try:
                genai.configure(api_key=gemini_api_key)
                self.gemini_client = genai.GenerativeModel('gemini-1.5-pro')
                logger.info("Gemini client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini client: {e}")
    
    def generate_code(self, prompt: str, language: str, model: str = "groq") -> Dict[str, Any]:
        """
        Generate code using the specified LLM.
        
        Args:
            prompt: The prompt for code generation
            language: Target programming language
            model: Which model to use ("groq" or "gemini")
        
        Returns:
            Dict containing the generated code and metadata
        """
        try:
            if model == "groq" and self.groq_client:
                return self._generate_with_groq(prompt, language)
            elif model == "gemini" and self.gemini_client:
                return self._generate_with_gemini(prompt, language)
            else:
                # Fallback to available model
                if self.groq_client:
                    return self._generate_with_groq(prompt, language)
                elif self.gemini_client:
                    return self._generate_with_gemini(prompt, language)
                else:
                    raise Exception("No LLM clients available")
        except Exception as e:
            logger.error(f"Error generating code: {e}")
            return {
                "code": f"# Error generating code: {str(e)}\n# Please check your API keys and try again.",
                "language": language,
                "model": model,
                "error": str(e)
            }
    
    def _generate_with_groq(self, prompt: str, language: str) -> Dict[str, Any]:
        """Generate code using Groq API."""
        try:
            # Use llama3-70b-8192 (current recommended model) instead of decommissioned mixtral-8x7b-32768
            response = self.groq_client.chat.completions.create(
                model="llama3-70b-8192",  # Updated to current model
                messages=[
                    {
                        "role": "system",
                        "content": f"You are an expert programmer. Write clean, idiomatic code in {language}. Add concise comments for clarity. Output only the code block, no extra explanation."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,
                max_tokens=2048
            )
            
            code = response.choices[0].message.content.strip()
            return {
                "code": code,
                "language": language,
                "model": "groq-llama3-70b-8192",
                "tokens_used": response.usage.total_tokens if response.usage else None
            }
        except Exception as e:
            logger.error(f"Groq API error: {e}")
            raise
    
    def _generate_with_gemini(self, prompt: str, language: str) -> Dict[str, Any]:
        """Generate code using Gemini API."""
        try:
            system_prompt = f"You are an expert programmer. Write clean, idiomatic code in {language}. Add concise comments for clarity. Output only the code block, no extra explanation."
            full_prompt = f"{system_prompt}\n\nTask: {prompt}"
            
            response = self.gemini_client.generate_content(full_prompt)
            
            code = response.text.strip()
            return {
                "code": code,
                "language": language,
                "model": "gemini-1.5-pro",
                "tokens_used": None  # Gemini doesn't provide token usage in free tier
            }
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise
    
    def explain_code(self, code: str, language: str, model: str = "groq") -> Dict[str, Any]:
        """
        Explain code line by line.
        
        Args:
            code: The code to explain
            language: Programming language of the code
            model: Which model to use
        
        Returns:
            Dict containing the explanation
        """
        prompt = f"""Explain the following {language} code line by line in plain English, suitable for a beginner:

{code}

Provide a clear, educational explanation that helps understand what each part does."""
        
        try:
            if model == "groq" and self.groq_client:
                return self._explain_with_groq(code, language)
            elif model == "gemini" and self.gemini_client:
                return self._explain_with_gemini(code, language)
            else:
                # Fallback
                if self.groq_client:
                    return self._explain_with_groq(code, language)
                elif self.gemini_client:
                    return self._explain_with_gemini(code, language)
                else:
                    raise Exception("No LLM clients available")
        except Exception as e:
            logger.error(f"Error explaining code: {e}")
            return {
                "explanation": f"Error generating explanation: {str(e)}",
                "language": language,
                "model": model,
                "error": str(e)
            }
    
    def _explain_with_groq(self, code: str, language: str) -> Dict[str, Any]:
        """Explain code using Groq API."""
        try:
            response = self.groq_client.chat.completions.create(
                model="llama3-70b-8192",  # Updated to current model
                messages=[
                    {
                        "role": "system",
                        "content": f"You are an expert programming instructor. Explain {language} code in a clear, educational way suitable for beginners."
                    },
                    {
                        "role": "user",
                        "content": f"Explain this {language} code line by line:\n\n{code}"
                    }
                ],
                temperature=0.3,
                max_tokens=2048
            )
            
            explanation = response.choices[0].message.content.strip()
            return {
                "explanation": explanation,
                "language": language,
                "model": "groq-llama3-70b-8192",
                "tokens_used": response.usage.total_tokens if response.usage else None
            }
        except Exception as e:
            logger.error(f"Groq API error: {e}")
            raise
    
    def _explain_with_gemini(self, code: str, language: str) -> Dict[str, Any]:
        """Explain code using Gemini API."""
        try:
            prompt = f"""You are an expert programming instructor. Explain this {language} code line by line in a clear, educational way suitable for beginners:

{code}

Provide a detailed explanation that helps understand what each part does."""
            
            response = self.gemini_client.generate_content(prompt)
            
            explanation = response.text.strip()
            return {
                "explanation": explanation,
                "language": language,
                "model": "gemini-1.5-pro",
                "tokens_used": None
            }
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise
    
    def translate_code(self, code: str, source_language: str, target_language: str, model: str = "groq") -> Dict[str, Any]:
        """
        Translate code from one language to another.
        
        Args:
            code: Source code
            source_language: Original programming language
            target_language: Target programming language
            model: Which model to use
        
        Returns:
            Dict containing the translated code
        """
        prompt = f"""Translate the following code from {source_language} to {target_language}, preserving functionality and idiomatic style:

{code}

Write clean, idiomatic {target_language} code that performs the same function."""
        
        try:
            if model == "groq" and self.groq_client:
                return self._translate_with_groq(code, source_language, target_language)
            elif model == "gemini" and self.gemini_client:
                return self._translate_with_gemini(code, source_language, target_language)
            else:
                # Fallback
                if self.groq_client:
                    return self._translate_with_groq(code, source_language, target_language)
                elif self.gemini_client:
                    return self._translate_with_gemini(code, source_language, target_language)
                else:
                    raise Exception("No LLM clients available")
        except Exception as e:
            logger.error(f"Error translating code: {e}")
            return {
                "translated_code": f"# Error translating code: {str(e)}",
                "source_language": source_language,
                "target_language": target_language,
                "model": model,
                "error": str(e)
            }
    
    def _translate_with_groq(self, code: str, source_language: str, target_language: str) -> Dict[str, Any]:
        """Translate code using Groq API."""
        try:
            response = self.groq_client.chat.completions.create(
                model="llama3-70b-8192",  # Updated to current model
                messages=[
                    {
                        "role": "system",
                        "content": f"You are an expert programmer. Translate code from {source_language} to {target_language}, preserving functionality and using idiomatic {target_language} style."
                    },
                    {
                        "role": "user",
                        "content": f"Translate this {source_language} code to {target_language}:\n\n{code}"
                    }
                ],
                temperature=0.1,
                max_tokens=2048
            )
            
            translated_code = response.choices[0].message.content.strip()
            return {
                "translated_code": translated_code,
                "source_language": source_language,
                "target_language": target_language,
                "model": "groq-llama3-70b-8192",
                "tokens_used": response.usage.total_tokens if response.usage else None
            }
        except Exception as e:
            logger.error(f"Groq API error: {e}")
            raise
    
    def _translate_with_gemini(self, code: str, source_language: str, target_language: str) -> Dict[str, Any]:
        """Translate code using Gemini API."""
        try:
            prompt = f"""You are an expert programmer. Translate this {source_language} code to {target_language}, preserving functionality and using idiomatic {target_language} style:

{code}

Write clean, idiomatic {target_language} code that performs the same function."""
            
            response = self.gemini_client.generate_content(prompt)
            
            translated_code = response.text.strip()
            return {
                "translated_code": translated_code,
                "source_language": source_language,
                "target_language": target_language,
                "model": "gemini-1.5-pro",
                "tokens_used": None
            }
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise
    
    def is_available(self) -> bool:
        """Check if any LLM client is available."""
        return self.groq_client is not None or self.gemini_client is not None
    
    def get_available_models(self) -> list:
        """Get list of available models."""
        models = []
        if self.groq_client:
            models.append("groq")
        if self.gemini_client:
            models.append("gemini")
        return models 