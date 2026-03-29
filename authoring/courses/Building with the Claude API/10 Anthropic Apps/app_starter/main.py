from mcp.server.fastmcp import FastMCP
from tools.math import add

mcp = FastMCP("docs")

mcp.tool()(add)

if __name__ == "__main__":
    mcp.run()
