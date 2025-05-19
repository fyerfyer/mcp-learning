"""
MCP Weather Server - Main implementation
"""
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# Import our modules
sys.path.append(str(Path(__file__).parent))
import config
from utils import weather_api, formatters
from deepseek_client import DeepseekClient

# Initialize the MCP server
mcp = FastMCP(config.SERVER_NAME)

# Initialize Deepseek client (if API key is available)
deepseek = DeepseekClient()

@mcp.tool()
async def get_alerts(state: str) -> str:
    """
    Get weather alerts for a US state.
    
    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    # Validate state code format (basic validation)
    if not state or len(state) != 2 or not state.isalpha():
        return "Please provide a valid two-letter US state code (e.g. CA, NY)"
    
    # Get alerts data
    alerts_data = await weather_api.get_alerts_for_state(state)
    
    # Format alerts into readable text
    formatted_alerts = formatters.format_alerts_summary(alerts_data)
    
    # Enhance with Deepseek if available
    if deepseek.is_available():
        enhanced_alerts = await deepseek.enhance_weather_interpretation(
            formatted_alerts,
            f"Summarize the weather alerts for {state} and explain their significance."
        )
        return enhanced_alerts
    
    return formatted_alerts

@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """
    Get weather forecast for a location.
    
    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # Validate coordinates (basic validation)
    if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
        return "Please provide valid latitude (-90 to 90) and longitude (-180 to 180) coordinates."
    
    # Get forecast data
    forecast_data = await weather_api.get_forecast_for_location(latitude, longitude)
    
    # Format forecast into readable text
    formatted_forecast = formatters.format_forecast(forecast_data)
    
    # Enhance with Deepseek if available
    if deepseek.is_available():
        enhanced_forecast = await deepseek.enhance_weather_interpretation(
            formatted_forecast,
            f"Provide key takeaways from this forecast and any notable weather patterns."
        )
        return enhanced_forecast
    
    return formatted_forecast

@mcp.resource("weather://help")
def get_help() -> str:
    """Provides help information about using the weather server."""
    return """
# Weather MCP Server

This server provides weather information through the following tools:

## Tools

- **get_alerts(state)**: Get weather alerts for a US state (use two-letter state code)
  Example: get_alerts("CA") for California alerts

- **get_forecast(latitude, longitude)**: Get weather forecast for a specific location
  Example: get_forecast(37.7749, -122.4194) for San Francisco

## Usage Tips

- For forecasts, you'll need to know the latitude and longitude coordinates
- Alerts are organized by state and include severity and instructions
- This server uses data from the US National Weather Service API
    """

if __name__ == "__main__":
    print("Starting Weather MCP Server...", file=sys.stderr)
    
    # Check if Deepseek integration is available
    if deepseek.is_available():
        print("Deepseek API integration enabled.", file=sys.stderr)
    else:
        print("Deepseek API integration disabled (no API key provided).", file=sys.stderr)
    
    # Run the server with configured transport
    mcp.run(transport=config.DEFAULT_TRANSPORT)