from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Some service")

@mcp.tool()
def some_tool(inp: str) -> str:
    return f"Output of some tool for {inp}."

mcp.run()
