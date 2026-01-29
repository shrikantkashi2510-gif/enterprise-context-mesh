import os
import logging
from mcp.server.fastmcp import FastMCP
from app.adapters.postgres_adapter import PostgresAdapter
from app.adapters.api_proxy import APIProxyAdapter
from app.schema.models import SQLQueryRequest

# Setup Enterprise Logging
logger = logging.getLogger("ECM-Server")

class EnterpriseContextMesh:
    """
    The Core Engine of the Enterprise Context Mesh.
    """

    def __init__(self):
        # Initialize FastMCP without deprecated arguments
        self.mcp = FastMCP("Enterprise-Context-Mesh")

        # Instantiate Modular Adapters
        self.db = PostgresAdapter()
        self.crm_proxy = APIProxyAdapter(base_url=os.getenv("CRM_API_BASE_URL", "https://api.crm.internal"))

        # Register Global Tools
        self._register_tools()

    def _register_tools(self):
        """
        Standardizes adapter methods into AI-discoverable tools.
        """

        @self.mcp.tool()
        async def query_internal_db(query: str) -> str:  # <--- CHANGED: Now accepts a simple string
            """
            Fetch live enterprise data from the internal PostgreSQL cluster.
            Enforces Read-Only governance and SQL injection protection.
            
            Args:
                query: The SQL SELECT statement to execute. Must be Read-Only.
            """
            try:
                # We manually validate the string using the Pydantic model here.
                # This keeps the API simple for the LLM, but safe for the Enterprise.
                validated_req = SQLQueryRequest(query=query)
                
                logger.info(f"Executing Governed SQL Query: {validated_req.query[:50]}...")
                results = await self.db.execute_read_only(validated_req.query)
                return f"Results from Internal DB:\n{results}"
            except ValueError as e:
                # Return the validation error clearly so the Agent can self-correct
                return f"Governance Violation: {str(e)}"
            except Exception as e:
                return f"System Error: {str(e)}"

        @self.mcp.tool()
        async def fetch_crm_context(endpoint: str) -> str:
            """
            Retrieves customer/lead context from the external CRM API.
            """
            logger.info(f"Fetching External CRM Context: {endpoint}")
            results = await self.crm_proxy.execute_read_only(endpoint)
            return f"CRM Context Data:\n{results}"

        @self.mcp.resource("mesh://config/governance")
        def get_governance_policy() -> str:
            return "Policy: Zero-Trust | Access: Read-Only | Residency: India (Remote Operation)"

    def get_server_instance(self) -> FastMCP:
        return self.mcp
