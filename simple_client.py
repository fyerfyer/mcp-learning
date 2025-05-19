import asyncio
import sys
import argparse
import traceback
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

def format_content(content):
    """Format content that could be a list of TextContent objects or other types."""
    if isinstance(content, list):
        # Handle list of TextContent objects
        try:
            # Combine text from all TextContent objects
            return ''.join(item.text for item in content)
        except AttributeError:
            # If items don't have text attribute, join as strings
            return ''.join(str(item) for item in content)
    # Return content directly if it's not a list
    return content

async def run_client(command, args):
    """Run the MCP client with the specified command and arguments."""
    # Set up an async exit stack for managing resources
    try:
        async with AsyncExitStack() as exit_stack:
            # Start the server process as a subprocess
            server_params = StdioServerParameters(
                command=sys.executable,
                args=["weather_server.py"],
                env=None
            )
            
            print("Connecting to weather server...")
            
            # Connect to the server using stdio transport
            stdio_transport = await exit_stack.enter_async_context(stdio_client(server_params))
            stdio_reader, stdio_writer = stdio_transport
            
            print("Creating client session...")
            
            # Create and initialize the client session
            session = await exit_stack.enter_async_context(ClientSession(stdio_reader, stdio_writer))
            
            print("Initializing session...")
            await session.initialize()
            
            # Get available tools to confirm connection is working
            print("Getting available tools...")
            tools_response = await session.list_tools()
            print(f"Connected to server with {len(tools_response.tools)} available tools\n")
            
            # Execute the requested command
            if command == "alerts":
                state = args.state.upper()
                print(f"Getting weather alerts for {state}...")
                result = await session.call_tool("get_alerts", {"state": state})
                # Format the TextContent objects in the list
                formatted_content = format_content(result.content)
                print("\n" + formatted_content)
                
            elif command == "forecast":
                lat, lon = float(args.latitude), float(args.longitude)
                print(f"Getting weather forecast for coordinates ({lat}, {lon})...")
                result = await session.call_tool("get_forecast", {
                    "latitude": lat,
                    "longitude": lon
                })
                # Format the TextContent objects in the list
                formatted_content = format_content(result.content)
                print("\n" + formatted_content)
                
            elif command == "help":
                resources_response = await session.list_resources()
                help_found = False
                
                # Use uri attribute instead of path
                for resource in resources_response.resources:
                    if str(resource.uri) == "weather://help":
                        print(f"Found help resource: {resource.name}")
                        # Use read_resource with the URI
                        response = await session.read_resource(str(resource.uri))
                        # Format the content which might be a list
                        formatted_content = format_content(response.contents)
                        print("\n" + formatted_content)
                        help_found = True
                        break
                
                if not help_found:
                    print("Help resource not found. Available resources:")
                    for resource in resources_response.resources:
                        print(f"- {resource.name} (URI: {resource.uri})")
                        
            elif command == "list":
                print("Available tools:")
                tools_response = await session.list_tools()
                for tool in tools_response.tools:
                    print(f"- {tool.name}: {tool.description}")
                
                print("\nAvailable resources:")
                resources_response = await session.list_resources()
                if not resources_response.resources:
                    print("No resources available.")
                else:
                    for resource in resources_response.resources:
                        # Display name and URI
                        print(f"- {resource.name} (URI: {resource.uri})")
                    
    except Exception as e:
        print(f"\nDetailed error information:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("\nTraceback:")
        traceback.print_exc()

def main():
    parser = argparse.ArgumentParser(description="Weather MCP Client")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    subparsers.required = True  # Make command argument required
    
    # Alerts command
    alerts_parser = subparsers.add_parser("alerts", help="Get weather alerts for a state")
    alerts_parser.add_argument("state", help="Two-letter US state code (e.g. CA)")
    
    # Forecast command
    forecast_parser = subparsers.add_parser("forecast", help="Get weather forecast for coordinates")
    forecast_parser.add_argument("latitude", help="Latitude coordinate")
    forecast_parser.add_argument("longitude", help="Longitude coordinate")
    
    # Help command
    subparsers.add_parser("help", help="Show help information")
    
    # List command
    subparsers.add_parser("list", help="List available tools and resources")
    
    args = parser.parse_args()
    
    try:
        asyncio.run(run_client(args.command, args))
    except KeyboardInterrupt:
        print("\nClient terminated by user")
    except Exception as e:
        print(f"Error in main: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()