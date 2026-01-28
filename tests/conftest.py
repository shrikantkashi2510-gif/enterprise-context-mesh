import pytest
import asyncio
from mcp.server.fastmcp import FastMCP, Client
from app.core.server import EnterpriseContextMesh

@pytest.fixture
def mesh_server():
    """Returns the initialized Enterprise Context Mesh instance."""
    mesh = EnterpriseContextMesh()
    return mesh.get_server_instance()

@pytest.fixture
async def mcp_client(mesh_server):
    """Provides an in-memory client to call tools without networking overhead."""
    async with Client(mesh_server) as client:
        yield client
