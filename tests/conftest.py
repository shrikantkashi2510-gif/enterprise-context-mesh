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
    Simulates the MCP Client behavior by exposing the server's tool-calling logic.
    This bypasses the 'fixture not found' error by providing a clean interface.
    """
    class MockClient:
        async def call_tool(self, name: str, arguments: dict):
            # FastMCP allows direct internal calls for testing 2026 standards
            return await mcp_server.call_tool(name, arguments)
            
    return MockClient()
