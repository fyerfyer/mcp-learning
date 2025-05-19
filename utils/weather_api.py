"""
Weather API client for the National Weather Service API.
"""
from typing import Any, Dict, Optional, List, Tuple
import httpx
from httpx import Response
import json
import sys
import asyncio
from pathlib import Path

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).parent.parent))
import config

async def make_nws_request(url: str) -> Optional[Dict[str, Any]]:
    """
    Make a request to the NWS API with proper error handling.
    
    Args:
        url: The full URL to request from NWS API
        
    Returns:
        Dict containing the JSON response or None if the request failed
    """
    headers = {
        "User-Agent": config.USER_AGENT,
        "Accept": "application/geo+json"
    }
    
    for attempt in range(config.MAX_RETRIES):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url, 
                    headers=headers, 
                    timeout=config.REQUEST_TIMEOUT
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                print(f"Resource not found: {url}", file=sys.stderr)
                return None
            if attempt == config.MAX_RETRIES - 1:
                print(f"Failed to fetch {url}: {e}", file=sys.stderr)
                return None
            # Wait before retry (with exponential backoff)
            await asyncio.sleep(2 ** attempt)
        except Exception as e:
            print(f"Error fetching {url}: {e}", file=sys.stderr)
            return None

async def get_alerts_for_state(state: str) -> Optional[Dict[str, Any]]:
    """
    Get weather alerts for a US state.
    
    Args:
        state: Two-letter US state code (e.g. CA, NY)
        
    Returns:
        Dict containing alerts data or None if the request failed
    """
    url = f"{config.NWS_API_BASE}/alerts/active/area/{state.upper()}"
    return await make_nws_request(url)

async def get_points_data(latitude: float, longitude: float) -> Optional[Dict[str, Any]]:
    """
    Get grid points data for a location, which is needed to fetch the forecast.
    
    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
        
    Returns:
        Dict containing points data or None if the request failed
    """
    url = f"{config.NWS_API_BASE}/points/{latitude},{longitude}"
    return await make_nws_request(url)

async def get_forecast_from_points_data(points_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Get detailed forecast using the forecast URL from points data.
    
    Args:
        points_data: Points data from get_points_data()
        
    Returns:
        Dict containing forecast data or None if the request failed
    """
    try:
        forecast_url = points_data["properties"]["forecast"]
        return await make_nws_request(forecast_url)
    except (KeyError, TypeError):
        print("Invalid points data or missing forecast URL", file=sys.stderr)
        return None

async def get_forecast_for_location(latitude: float, longitude: float) -> Optional[Dict[str, Any]]:
    """
    Get weather forecast for a specific location.
    
    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
        
    Returns:
        Dict containing forecast data or None if the request failed
    """
    points_data = await get_points_data(latitude, longitude)
    if not points_data:
        return None
    
    return await get_forecast_from_points_data(points_data)

async def get_location_from_address(address: str) -> Optional[Tuple[float, float]]:
    """
    Get latitude and longitude for a given address using NWS API.
    This is a placeholder - NWS doesn't provide geocoding.
    In a real implementation, you'd integrate with a geocoding service.
    
    Args:
        address: Address or location name
        
    Returns:
        Tuple of (latitude, longitude) or None if geocoding failed
    """
    # This would normally use a geocoding API like Google Maps, OpenStreetMap, etc.
    # For now, we'll just return None to indicate this isn't implemented
    print(f"Geocoding not implemented for: {address}", file=sys.stderr)
    return None