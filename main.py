from mcp.server.fastmcp import FastMCP
import math

server = FastMCP(
    name="Arithmatic MCP Server",
    instructions="This server performs basic arithmatic operations."
)

@server.tool()
async def calculate(expression: str) -> dict:
    """
    evaluate a math expression
    """
    print(f"TOOL CALLED: calculate({expression})")
    try:
        result = eval(expression)
        print(f"result: ({result})")
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
async def square_root(value: float) -> dict:
    """Return the square root of a number"""
    print(f"TOOL CALLED: square_root({value})")
    try:
        result = math.sqrt(value)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@server.tool()
async def power(base: float, exponent: float) -> dict:
    """Return base raised to the power of exponent"""
    print(f"TOOL CALLED: power({base}, {exponent})")
    try:
        result = base ** exponent
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print("Starting MCP server...")
    server.run(transport="sse")
