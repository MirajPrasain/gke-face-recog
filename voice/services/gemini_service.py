import google.generativeai as genai
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class GeminiService:
    """Service for handling interactions with Google's Gemini-2.5-Flash API."""
    
    def __init__(self):
        """Initialize the Gemini service."""
        self.api_key = os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            logger.error("GOOGLE_API_KEY environment variable not set")
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        
        # Configure the API
        genai.configure(api_key=self.api_key)
        
        # Initialize the model
        try:
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            logger.info("Gemini-1.5-Flash model initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini model: {str(e)}")
            raise
    
    def get_response(self, prompt: str, context: str = None) -> Optional[str]:
        """
        Get a response from Gemini for the given prompt.
        
        Args:
            prompt (str): The user's input/question
            context (str, optional): Additional context for the conversation
            
        Returns:
            str: Gemini's response or None if failed
        """
        try:
            # Prepare the full prompt
            if context:
                full_prompt = f"Context: {context}\n\nUser: {prompt}\n\nPlease provide a helpful and concise response:"
            else:
                full_prompt = f"User: {prompt}\n\nPlease provide a helpful and concise response:"
            
            # Generate response
            response = self.model.generate_content(full_prompt)
            
            if response and response.text:
                logger.info(f"Gemini response generated successfully for prompt: {prompt[:50]}...")
                return response.text.strip()
            else:
                logger.warning("Gemini returned empty response")
                return None
                
        except Exception as e:
            logger.error(f"Error getting Gemini response: {str(e)}")
            return None
    
    def get_voice_navigation_response(self, command: str) -> Optional[str]:
        """
        Get a response specifically for voice navigation commands.
        
        Args:
            command (str): The voice command for navigation
            
        Returns:
            str: Navigation response or None if failed
        """
        try:
            # Create a specialized prompt for navigation
            navigation_prompt = f"""
            You are a voice navigation assistant. The user has given you the following voice command: "{command}"
            
            Please interpret this command and provide a helpful response. If it's a navigation command (like "go to", "navigate to", "find", "search for"), 
            provide clear directions or information. If it's a general question, answer it concisely.
            
            Keep your response conversational and helpful, as it will be converted to speech.
            """
            
            response = self.model.generate_content(navigation_prompt)
            
            if response and response.text:
                logger.info(f"Navigation response generated for command: {command}")
                return response.text.strip()
            else:
                logger.warning("Gemini returned empty navigation response")
                return None
                
        except Exception as e:
            logger.error(f"Error getting navigation response: {str(e)}")
            return None
    
    def get_contextual_response(self, current_text: str, conversation_history: list = None) -> Optional[str]:
        """
        Get a contextual response based on conversation history.
        
        Args:
            current_text (str): The current user input
            conversation_history (list, optional): Previous conversation turns
            
        Returns:
            str: Contextual response or None if failed
        """
        try:
            # Build context from conversation history
            context_parts = []
            if conversation_history:
                for turn in conversation_history[-5:]:  # Last 5 turns for context
                    if 'user' in turn and 'assistant' in turn:
                        context_parts.append(f"User: {turn['user']}")
                        context_parts.append(f"Assistant: {turn['assistant']}")
            
            # Create full prompt with context
            if context_parts:
                context_str = "\n".join(context_parts)
                full_prompt = f"""
                Previous conversation:
                {context_str}
                
                Current user input: {current_text}
                
                Please provide a helpful response that takes into account the conversation context.
                Keep it conversational as it will be converted to speech.
                """
            else:
                full_prompt = f"""
                User input: {current_text}
                
                Please provide a helpful and conversational response.
                """
            
            response = self.model.generate_content(full_prompt)
            
            if response and response.text:
                logger.info(f"Contextual response generated successfully")
                return response.text.strip()
            else:
                logger.warning("Gemini returned empty contextual response")
                return None
                
        except Exception as e:
            logger.error(f"Error getting contextual response: {str(e)}")
            return None
    
    def test_connection(self) -> bool:
        """
        Test the connection to Gemini API.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            test_response = self.model.generate_content("Hello, please respond with 'Connection successful'")
            if test_response and test_response.text:
                logger.info("Gemini API connection test successful")
                return True
            return False
        except Exception as e:
            logger.error(f"Gemini API connection test failed: {str(e)}")
            return False