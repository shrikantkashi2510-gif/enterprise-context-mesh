import pytest
import asyncio
from app.core.server import EnterpriseContextMesh

@pytest.fixture
def mesh_instance():
    """Returns the initialized Enterprise Context Mesh instance."""
    return EnterpriseContextMesh()

@pytest.fixture
def mcp_server(mesh_instance):
    """Provides the FastMCP server instance."""
    return mesh_instance.get_server_instance()

@pytest.fixture
def mcp_client(mcp_server):
    """
    Simulates an MCP Client. 
    By defining this here, 'fixture mcp_client not found' is resolved.
    """
    class MockClient:
        async def call_tool(self, name: str, arguments: dict):
            # Directly invokes the tool logic within the server instance
            return await mcp_server.call_tool(name, arguments)
            
    return MockClient()
