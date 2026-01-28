from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Optional
import re

class SQLQueryRequest(BaseModel):
    """Schema for incoming SQL query requests via MCP."""
    query: str = Field(
        ..., 
        description="The SQL SELECT query to execute. Must be read-only.",
        example="SELECT * FROM users LIMIT 10;"
    )

    @validator('query')
    def enforce_read_only(cls, v):
        """Strategic validation to block write operations at the schema level."""
        forbidden = ["INSERT", "UPDATE", "DELETE", "DROP", "TRUNCATE", "ALTER"]
        if any(keyword in v.upper() for keyword in forbidden):
            raise ValueError("Only SELECT operations are permitted for security governance.")
        return v

class APIContextRequest(BaseModel):
    """Schema for fetching context from external enterprise APIs."""
    endpoint: str = Field(..., description="The relative path of the API endpoint to fetch.")
    params: Optional[Dict[str, Any]] = Field(None, description="Optional query parameters.")

class MeshResponse(BaseModel):
    """Standardized response format for all Mesh operations."""
    status: str = Field("success", description="The status of the operation.")
    data: List[Any] = Field(..., description="The resulting data payload.")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Audit and performance metadata.")
