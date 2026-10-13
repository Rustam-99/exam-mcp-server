
import hashlib
import os

from mcp.server.fastmcp import FastMCP, Context

EMAIL = "23f1000351@ds.study.iitm.ac.in"

mcp = FastMCP(
    "Exam MCP Server",
    stateless_http=True,
    host="0.0.0.0",
    port=int(os.environ.get("PORT", "8000")),
)

@mcp.tool()
def solve_challenge(ctx: Context) -> str:
    """Return the first 16 hex characters of the required SHA-256 hash."""

    headers = ctx.request_context.request.headers
    challenge = headers.get("x-exam-challenge")

    if not challenge:
        raise ValueError("Missing X-Exam-Challenge header")

    message = f"{challenge}:{EMAIL.strip().lower()}"
    result = hashlib.sha256(message.encode("utf-8")).hexdigest()

    return result[:16]


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
