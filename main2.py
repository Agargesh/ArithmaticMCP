from mcp.server.fastmcp import FastMCP
import math

server = FastMCP(name="Airthmatic MCP Server", instructions="Perfroms math operations")

@server.tool()
async def calculate(expression: str) -> dict:
    try:
        return {"result": eval(expression)}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
async def square_root(value: float) -> dict:
    try:
        return {"results": math.sqrt(value)}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
async def power(base: float, exponent: float) -> dict:
    try:
        return {"result": base ** exponent}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print("Starting MCP server...")
    server.run(transport="sse")
