"""
Client for Deepseek AI API integration.
"""
import sys
from typing import Dict, List, Optional
from openai import OpenAI
from pathlib import Path

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).parent))
import config


class DeepseekClient:
    """A client for interacting with the Deepseek AI API."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Deepseek API client.
        
        Args:
            api_key: Deepseek API key (defaults to config.DEEPSEEK_API_KEY)
        """
        self.api_key = api_key or config.DEEPSEEK_API_KEY
        if not self.api_key:
            print("WARNING: No Deepseek API key provided. LLM features will be unavailable.", 
                  file=sys.stderr)
            self.client = None
        else:
            self.client = OpenAI(api_key=self.api_key, base_url=config.DEEPSEEK_API_BASE)

    def is_available(self) -> bool:
        """Check if the Deepseek API client is available."""
        return self.client is not None

    async def enhance_weather_interpretation(self, 
                                       weather_data: str, 
                                       query: Optional[str] = None) -> str:
        """
        Use Deepseek to enhance weather data with interpretations and advice.
        
        Args:
            weather_data: Raw or formatted weather data
            query: Optional user query for more specific interpretation
            
        Returns:
            Enhanced interpretation of the weather data
        """
        if not self.is_available():
            return weather_data
        
        prompt = self._build_enhancement_prompt(weather_data, query)
        
        try:
            response = self.client.chat.completions.create(
                model=config.DEEPSEEK_MODEL,
                messages=prompt,
                max_tokens=500
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error enhancing weather data with Deepseek: {e}", file=sys.stderr)
            # Fall back to returning original data
            return weather_data
    
    def _build_enhancement_prompt(self, 
                                 weather_data: str, 
                                 query: Optional[str] = None) -> List[Dict[str, str]]:
        """
        Build a prompt for enhancing weather data.
        
        Args:
            weather_data: Weather data to enhance
            query: Optional user query
            
        Returns:
            List of message dictionaries for the chat completion API
        """
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful weather assistant that provides relevant interpretations "
                    "of weather data. Enhance the provided weather information with useful context, "
                    "practical advice, and explanations of meteorological terms where appropriate. "
                    "Keep your response concise and focused on the most important aspects of the weather data."
                )
            },
            {
                "role": "user",
                "content": f"Here is some weather data:\n\n{weather_data}"
            }
        ]
        
        if query:
            messages.append({
                "role": "user",
                "content": f"I'm specifically interested in: {query}"
            })
            
        return messages