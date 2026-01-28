import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from app.adapters.postgres_adapter import PostgresAdapter

# Initialize the High-Ticket Hub
server = Server("enterprise-context-mesh")

@server.list_tools()
async def handle_list_tools():
    """Exposes the internal database capabilities to the LLM."""
    return [
        {
            "name": "query_enterprise_db",
            "description": "Execute governed read-only SQL queries on the internal PostgreSQL cluster.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The SQL query to run"}
                },
                "required": ["query"]
            }
        }
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict):
    if name == "query_enterprise_db":
        # Integrating your existing high-ticket Postgres logic
        db = PostgresAdapter()
        result = await db.execute_read_only(arguments["query"])
        return [{"type": "text", "text": str(result)}]
    raise ValueError(f"Tool not found: {name}")

async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
