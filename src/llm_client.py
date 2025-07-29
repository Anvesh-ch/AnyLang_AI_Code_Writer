"""
LLM Client Module for AnyLang AI Code Writer
Handles API interactions with Groq and Gemini for code generation tasks.
"""

import os
import logging
import time
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
        Generate code using the specified LLM with automatic fallback.
        
        Args:
            prompt: The prompt for code generation
            language: Target programming language
            model: Which model to use ("groq" or "gemini")
        
        Returns:
            Dict containing the generated code and metadata
        """
        # Try the requested model first
        if model == "groq" and self.groq_client:
            try:
                return self._generate_with_groq(prompt, language)
            except Exception as e:
                logger.warning(f"Groq failed, trying Gemini: {e}")
                if self.gemini_client:
                    try:
                        return self._generate_with_gemini(prompt, language)
                    except Exception as gemini_error:
                        logger.error(f"Both Groq and Gemini failed: {gemini_error}")
                        return self._create_error_response(str(gemini_error), language, "both")
                else:
                    return self._create_error_response(str(e), language, "groq")
        
        elif model == "gemini" and self.gemini_client:
            try:
                return self._generate_with_gemini(prompt, language)
            except Exception as e:
                logger.warning(f"Gemini failed, trying Groq: {e}")
                if self.groq_client:
                    try:
                        return self._generate_with_groq(prompt, language)
                    except Exception as groq_error:
                        logger.error(f"Both Gemini and Groq failed: {groq_error}")
                        return self._create_error_response(str(groq_error), language, "both")
                else:
                    return self._create_error_response(str(e), language, "gemini")
        
        else:
            # Auto-select available model
            if self.groq_client:
                try:
                    return self._generate_with_groq(prompt, language)
                except Exception as e:
                    logger.error(f"Groq failed: {e}")
                    if self.gemini_client:
                        try:
                            return self._generate_with_gemini(prompt, language)
                        except Exception as gemini_error:
                            return self._create_error_response(str(gemini_error), language, "both")
                    else:
                        return self._create_error_response(str(e), language, "groq")
            elif self.gemini_client:
                try:
                    return self._generate_with_gemini(prompt, language)
                except Exception as e:
                    return self._create_error_response(str(e), language, "gemini")
            else:
                return self._create_error_response("No LLM clients available", language, "none")
    
    def _create_error_response(self, error_msg: str, language: str, failed_models: str) -> Dict[str, Any]:
        """Create a standardized error response."""
        if "quota" in error_msg.lower() or "429" in error_msg:
            if failed_models == "both":
                return {
                    "code": f"""# API Rate Limit Exceeded

Both Groq and Gemini APIs have hit their rate limits.

## Solutions:
1. **Wait a few minutes** and try again
2. **Upgrade your API plan** for higher limits
3. **Use a different API key** if available

## Current Limits:
- **Groq Free Tier**: 100 requests/minute
- **Gemini Free Tier**: 15 requests/minute

Error: {error_msg}""",
                    "language": language,
                    "model": "error",
                    "error": error_msg
                }
            else:
                return {
                    "code": f"""# API Rate Limit Exceeded

The {failed_models.title()} API has hit its rate limit.

## Solutions:
1. **Wait a few minutes** and try again
2. **Switch to the other model** in the sidebar
3. **Upgrade your API plan** for higher limits

Error: {error_msg}""",
                    "language": language,
                    "model": "error",
                    "error": error_msg
                }
        else:
            return {
                "code": f"# Error generating code: {error_msg}\n# Please check your API keys and try again.",
                "language": language,
                "model": "error",
                "error": error_msg
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
        Explain code line by line with automatic fallback.
        
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
        
        # Use the same fallback logic as generate_code
        return self.generate_code(prompt, language, model)
    
    def translate_code(self, code: str, source_language: str, target_language: str, model: str = "groq") -> Dict[str, Any]:
        """
        Translate code from one language to another with automatic fallback.
        
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
        
        # Use the same fallback logic as generate_code
        result = self.generate_code(prompt, target_language, model)
        
        # Rename the key for translation
        if "code" in result:
            result["translated_code"] = result.pop("code")
        
        return result
    
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
    
    def get_rate_limit_info(self) -> Dict[str, Any]:
        """Get information about current rate limits."""
        return {
            "groq_free_tier": "100 requests/minute",
            "gemini_free_tier": "15 requests/minute",
            "groq_paid_tier": "1000+ requests/minute",
            "gemini_paid_tier": "1000+ requests/minute"
        } 