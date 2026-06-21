from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather")

@mcp.tool()
def get_weather(location:str) -> dict:
    """_summary_
    Gets the weather for a city
    """
    return {
        "location": location,
        "temperature": "25°C",
        "condition": "Sunny"
    }

if __name__ == "__main__":
    mcp.run(transport="streamable-http")



