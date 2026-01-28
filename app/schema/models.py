from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Optional

class SQLQueryRequest(BaseModel):
    query: str = Field(
        ..., 
        description="The SQL SELECT query to execute. Must be read-only.",
        json_schema_extra={"example": "SELECT * FROM users LIMIT 10;"} # Fixed V2 syntax
    )

    @field_validator('query') # Fixed V2 syntax
    @classmethod
    def enforce_read_only(cls, v: str) -> str:
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
