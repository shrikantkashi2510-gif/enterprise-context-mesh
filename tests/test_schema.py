import pytest
from pydantic import ValidationError
from app.schema.models import SQLQueryRequest, APIContextRequest

def test_sql_request_valid_query():
    """Confirms that a standard SELECT query passes validation."""
    request = SQLQueryRequest(query="SELECT name FROM users WHERE id = 10;")
    assert request.query == "SELECT name FROM users WHERE id = 10;"

def test_sql_request_blocks_malicious_keywords():
    """Verifies that the Pydantic validator catches 'DELETE' before it leaves the schema."""
    with pytest.raises(ValidationError) as excinfo:
        SQLQueryRequest(query="DELETE FROM users;")
    
    assert "Only SELECT operations are permitted" in str(excinfo.value)

def test_sql_request_blocks_ddl_commands():
    """Ensures structural changes like 'DROP' are caught at the contract level."""
    with pytest.raises(ValidationError) as excinfo:
        SQLQueryRequest(query="DROP TABLE metadata;")
    
    assert "Only SELECT operations are permitted" in str(excinfo.value)

def test_api_context_request_validation():
    """Verifies the CRM API schema handles paths and parameters correctly."""
    request = APIContextRequest(endpoint="/v1/leads", params={"status": "warm"})
    assert request.endpoint == "/v1/leads"
    assert request.params["status"] == "warm"

def test_sql_request_case_insensitivity():
    """Ensures that lowercase 'delete' or 'update' is also blocked."""
    with pytest.raises(ValidationError):
        SQLQueryRequest(query="select * from users; update users set admin=true;")
