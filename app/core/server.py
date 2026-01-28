import os
import logging
from mcp.server.fastmcp import FastMCP
from app.adapters.postgres_adapter import PostgresAdapter
from app.adapters.api_proxy import APIProxyAdapter
from app.schema.models import SQLQueryRequest, APIContextRequest

# Setup Enterprise Logging
logger = logging.getLogger("ECM-Server")

class EnterpriseContextMesh:
    """
    The Core Engine of the Enterprise Context Mesh.
    Orchestrates secure data access between LLM Agents and fragmented data sources.
    """

    def __init__(self):
        # 1. Initialize FastMCP (Fixed for compatibility)
        # We pass only the name here. Description/Version are handled in metadata or ignored in this version.
        self.mcp = FastMCP("Enterprise-Context-Mesh")

        # 2. Instantiate Modular Adapters
        self.db = PostgresAdapter()
        # Example External Service
        self.crm_proxy = APIProxyAdapter(base_url=os.getenv("CRM_API_BASE_URL", "https://api.crm.internal"))

        # 3. Register Global Tools
        self._register_tools()

    def _register_tools(self):
        """
        Standardizes adapter methods into AI-discoverable tools.
        """

        @self.mcp.tool()
        async def query_internal_db(request: SQLQueryRequest) -> str:
            """
            Fetch live enterprise data from the internal PostgreSQL cluster.
            Enforces Read-Only governance and SQL injection protection.
            """
            # The 'request' object is already validated by Pydantic before it reaches here
            logger.info(f"Executing Governed SQL Query: {request.query[:50]}...")
            results = await self.db.execute_read_only(request.query)
            return f"Results from Internal DB:\n{results}"

        @self.mcp.tool()
        async def fetch_crm_context(endpoint: str) -> str:
            """
            Retrieves customer/lead context from the external CRM API.
            Uses secure proxying with built-in rate-limiting and audit logging.
            """
            logger.info(f"Fetching External CRM Context: {endpoint}")
            results = await self.crm_proxy.execute_read_only(endpoint)
            return f"CRM Context Data:\n{results}"

        @self.mcp.resource("mesh://config/governance")
        def get_governance_policy() -> str:
            """Exposes the current AI safety and data-access policies as a resource."""
            return "Policy: Zero-Trust | Access: Read-Only | Residency: India (Remote Operation)"

    def get_server_instance(self) -> FastMCP:
        """Returns the configured FastMCP instance for deployment."""
        return self.mcp
