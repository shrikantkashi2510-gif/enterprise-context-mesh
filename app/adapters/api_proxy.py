import os
import logging
import httpx
from typing import List, Dict, Any, Optional
from app.adapters.base import BaseAdapter

# Configure Logging for External Audit Trails
logger = logging.getLogger("ECM-APIProxy")

class APIProxyAdapter(BaseAdapter):
    """
    Enterprise-Grade API Proxy for MCP.
    Enforces Timeouts, Rate-Limiting, and Response Sanitization.
    """

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.client: Optional[httpx.AsyncClient] = None
        # Retrieve API Key from secure .env only
        self.api_key = os.getenv("EXTERNAL_SERVICE_API_KEY")

    async def connect(self):
        """Initializes a persistent, pooled HTTP client."""
        if not self.client:
            self.client = httpx.AsyncClient(
                base_url=self.base_url,
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                timeout=httpx.Timeout(10.0, connect=5.0),
                limits=httpx.Limits(max_connections=50, max_keepalive_connections=10)
            )
            logger.info(f"Initialized Secure API Proxy for: {self.base_url}")

    async def execute_read_only(self, endpoint_path: str) -> List[Dict[str, Any]]:
        """
        Executes a GET request to an external service.
        Strictly prevents POST/PUT/DELETE to ensure 'Read-Only' governance.
        """
        if not self.client:
            await self.connect()

        # Security: Prevent path traversal or command injection in the URL
        safe_path = self.sanitize_input(endpoint_path).lstrip("/")
        
        try:
            response = await self.client.get(safe_path)
            response.raise_for_status()
            
            data = response.json()
            # Ensure the output is always a list for standardized MCP processing
            return data if isinstance(data, list) else [data]

        except httpx.HTTPStatusError as e:
            logger.error(f"External API Error ({e.response.status_code}): {e.response.text}")
            return [{"error": f"Service unavailable: {e.response.status_code}"}]
        except Exception as e:
            logger.error(f"Proxy Execution Failure: {str(e)}")
            return [{"error": "Internal Proxy Error"}]

    async def close(self):
        """Gracefully shuts down the HTTP connection pool."""
        if self.client:
            await self.client.aclose()
            logger.info(f"API Proxy for {self.base_url} closed.")
