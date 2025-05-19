"""
Configuration settings for the Weather MCP server.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
dotenv_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path)

# API Keys
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
NWS_API_KEY = os.getenv('NWS_API_KEY')  # Currently NWS doesn't require an API key, but including for future-proofing

# Weather API configuration
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-mcp-server/1.0 (your-email@example.com)"  # Replace with your contact info

# Request settings
REQUEST_TIMEOUT = 30.0  # Timeout for API requests in seconds
MAX_RETRIES = 3  # Maximum number of retries for failed requests

# Deepseek API configuration
DEEPSEEK_API_BASE = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-chat"  # Default model

# MCP Server settings
SERVER_NAME = "weather"
DEFAULT_TRANSPORT = "stdio"  # Default transport protocol (stdio, sse, streamable-http)

# Cache settings
ENABLE_CACHE = True
CACHE_TTL = 300  # Time-to-live for cached data in seconds (5 minutes)