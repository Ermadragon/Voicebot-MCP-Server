from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Personal VoiceBot")

@mcp.tool()
def hello(name: str) -> str:
    return f"Hello, {name}!"

@mcp.resource("ping://check")
def ping_check() -> str:
    return "Pong from MCP!"

if __name__ == "__main__":
    mcp.run()

