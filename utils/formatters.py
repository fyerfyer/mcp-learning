"""
Utility functions to format weather data into human-readable text.
"""
from typing import Any, Dict

def format_alert(feature: Dict[str, Any]) -> str:
    """
    Format a single weather alert feature into a readable string.
    
    Args:
        feature: Alert feature from NWS API
        
    Returns:
        Formatted alert text
    """
    try:
        props = feature.get("properties", {})
        
        # Extract key information
        event = props.get("event", "Unknown Event")
        headline = props.get("headline", "")
        area_desc = props.get("areaDesc", "Unknown Area")
        severity = props.get("severity", "Unknown")
        certainty = props.get("certainty", "Unknown")
        urgency = props.get("urgency", "Unknown")
        description = props.get("description", "No description available")
        instruction = props.get("instruction", "No specific instructions provided")
        
        # Format the alert with the most important information first
        formatted_alert = f"""
ALERT: {event}
{headline}

AREA: {area_desc}
SEVERITY: {severity}
URGENCY: {urgency}
CERTAINTY: {certainty}

DESCRIPTION:
{description}

INSTRUCTIONS:
{instruction}
"""
        return formatted_alert.strip()
    except Exception as e:
        return f"Error formatting alert: {e}"

def format_alerts_summary(data: Dict[str, Any]) -> str:
    """
    Format all weather alerts into a readable summary.
    
    Args:
        data: Full alerts response from NWS API
        
    Returns:
        Formatted alerts summary text
    """
    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."
    
    features = data.get("features", [])
    if not features:
        return "No active alerts for this area."
    
    alert_count = len(features)
    alerts_text = [format_alert(feature) for feature in features]
    
    summary = f"Found {alert_count} active weather alert{'s' if alert_count != 1 else ''}:\n\n"
    summary += "\n\n" + "-" * 40 + "\n\n".join(alerts_text)
    
    return summary

def format_forecast_period(period: Dict[str, Any]) -> str:
    """
    Format a single forecast period into a readable string.
    
    Args:
        period: Forecast period data from NWS API
        
    Returns:
        Formatted forecast period text
    """
    try:
        name = period.get("name", "Unknown Period")
        temp = period.get("temperature", "?")
        temp_unit = period.get("temperatureUnit", "F")
        wind_speed = period.get("windSpeed", "Unknown")
        wind_direction = period.get("windDirection", "")
        short_forecast = period.get("shortForecast", "")
        detailed_forecast = period.get("detailedForecast", "No detailed forecast available")
        
        formatted_period = f"""
{name}
Temperature: {temp}°{temp_unit}
Wind: {wind_speed} {wind_direction}
{short_forecast}

{detailed_forecast}
"""
        return formatted_period.strip()
    except Exception as e:
        return f"Error formatting forecast period: {e}"

def format_forecast(data: Dict[str, Any], limit: int = 5) -> str:
    """
    Format weather forecast data into a readable summary.
    
    Args:
        data: Full forecast response from NWS API
        limit: Maximum number of periods to include
        
    Returns:
        Formatted forecast text
    """
    if not data or "properties" not in data or "periods" not in data["properties"]:
        return "Unable to fetch forecast data."
    
    try:
        location = data.get("properties", {}).get("location", {}).get("name", "the requested location")
        periods = data.get("properties", {}).get("periods", [])
        
        if not periods:
            return f"No forecast data available for {location}."
        
        # Limit the number of periods
        periods = periods[:limit]
        
        forecast_periods = [format_forecast_period(period) for period in periods]
        
        summary = f"Weather forecast for {location}:\n\n"
        summary += "\n\n" + "-" * 40 + "\n\n".join(forecast_periods)
        
        return summary
    except Exception as e:
        return f"Error formatting forecast: {e}"