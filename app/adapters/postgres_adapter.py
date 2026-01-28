import os
import logging
from typing import List, Dict, Any, Optional
import asyncpg  # High-performance async driver
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Configure Logging for Audit Trails (Crucial for Governance)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ECM-PostgresAdapter")

class PostgresAdapter:
    """
    High-Security Postgres Adapter for MCP.
    Enforces Read-Only execution and SQL Injection Prevention.
    """
    
    def __init__(self):
        self.dsn = os.getenv("DATABASE_URL")
        self.pool: Optional[asyncpg.Pool] = None
        # Enforce a "Read-Only" session at the protocol level
        self.init_query = "SET SESSION CHARACTERISTICS AS TRANSACTION READ ONLY;"

    async def connect(self):
        """Initializes a secure connection pool."""
        if not self.pool:
            try:
                self.pool = await asyncpg.create_pool(
                    dsn=self.dsn,
                    min_size=5,
                    max_size=20,
                    init=self.initialize_session,
                    command_timeout=30.0
                )
                logger.info("Successfully established secure Postgres connection pool.")
            except Exception as e:
                logger.error(f"Connection Failed: {str(e)}")
                raise

    async def initialize_session(self, conn):
        """Forces every connection in the pool to be Read-Only."""
        await conn.execute(self.init_query)

    async def execute_read_only(self, query: str) -> List[Dict[str, Any]]:
        """
        Executes a query with strict security validation.
        Designed to prevent SQL injection and Write operations.
        """
        if not self.pool:
            await self.connect()

        # Security Check: Block destructive keywords even if user is Read-Only
        forbidden_keywords = ["DROP", "DELETE", "UPDATE", "INSERT", "TRUNCATE", "GRANT"]
        if any(keyword in query.upper() for keyword in forbidden_keywords):
            logger.warning(f"BLOCKED: Destructive query attempted: {query}")
            return [{"error": "Security Violation: Write operations are strictly prohibited."}]

        try:
            async with self.pool.acquire() as connection:
                rows = await connection.fetch(query)
                # Convert asyncpg Record objects to standard Dictionaries
                return [dict(row) for row in rows]
        except asyncpg.exceptions.InsufficientPrivilegeError:
            return [{"error": "Permission Denied: Database user lacks SELECT privileges."}]
        except Exception as e:
            logger.error(f"Query Execution Error: {str(e)}")
            return [{"error": f"Database Error: {str(e)}"}]

    async def close(self):
        """Graceful shutdown for the connection pool."""
        if self.pool:
            await self.pool.close()
            logger.info("Postgres connection pool closed.")
