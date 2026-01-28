import os
import logging
from mcp.server.fastmcp import FastMCP
from app.adapters.postgres_adapter import PostgresAdapter
from app.adapters.api_proxy import APIProxyAdapter

# Setup Enterprise Logging
logger = logging.getLogger("ECM-Server")

class EnterpriseContextMesh:
    """
    The Core Engine of the Enterprise Context Mesh.
    Orchestrates secure data access between LLM Agents and fragmented data sources.
    """

    def __init__(self):
        # 1. Initialize FastMCP with 2026 Production Standards
        self.mcp = FastMCP(
            "Enterprise-Context-Mesh",
            description="High-security data mesh for Agentic Workflows",
            version="1.0.0"
        )

        # 2. Instantiate Modular Adapters
        self.db = PostgresAdapter()
        # Example External Service (e.g., Salesforce or Internal CRM)
        self.crm_proxy = APIProxyAdapter(base_url=os.getenv("CRM_API_BASE_URL", "https://api.crm.internal"))

        # 3. Register Global Tools
        self._register_tools()

    def _register_tools(self):
        """
        Standardizes adapter methods into AI-discoverable tools.
        The docstrings below are read by the LLM to understand 'Intent'.
        """

        @self.mcp.tool()
        async def query_internal_db(sql_query: str) -> str:
            """
            Fetch live enterprise data from the internal PostgreSQL cluster.
            Enforces Read-Only governance and SQL injection protection.
            """
            logger.info(f"Executing Governed SQL Query: {sql_query[:50]}...")
            results = await self.db.execute_read_only(sql_query)
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
