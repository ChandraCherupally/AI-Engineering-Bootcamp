from mcp.server.fastmcp import FastMCP
import sys

mcp = FastMCP("Math")

@mcp.tool()
def add(a:int, b:int) ->int:
    """_summary_
    Adds two numbers
    """
    print(f"add Tool Called: {a} + {b}")
    return a + b

@mcp.tool()
def multiply(a:int, b:int) ->str:
    """_summary_
    Multiplication of two numbers
    """
    print("MULTIPLY TOOL EXECUTED", file=sys.stderr)
    return f"Multiplication of {a} and {b} is {a*b}"

#The transport = "stdio" argument is used to specify the transport protocol.
#Use standard input/output(stdin and stdout) to recieve and responde to tool functional calls
#Used when the MCP server is running as a child process of the client.

@mcp.tool()
def secret_tool() -> str:
    print("SECRET TOOL CALLED", file=sys.stderr)
    return "MCP_WORKS_AND_EXECUTED_Perfectly"

if __name__ == "__main__":
    mcp.run(transport="stdio")