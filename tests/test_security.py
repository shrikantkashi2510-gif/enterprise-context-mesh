import pytest

@pytest.mark.asyncio
async def test_sql_injection_protection(mcp_client):
    """Verifies that destructive SQL commands are blocked."""
    malicious_queries = [
        "DROP TABLE users;",
        "DELETE FROM records WHERE id = 1;",
        "UPDATE accounts SET balance = 999999;",
        "SELECT * FROM users; DROP TABLE metadata;"
    ]

    for sql in malicious_queries:
        # The tool catches the ValueError and returns a "Governance Violation" string
        result = await mcp_client.call_tool("query_internal_db", {"query": sql})
        
        # Check that the governance logic worked
        assert "Governance Violation" in str(result) or "prohibited" in str(result).lower()

@pytest.mark.asyncio
async def test_read_only_enforcement(mcp_client, mocker):
    """Verifies that INSERT queries are blocked."""
    result = await mcp_client.call_tool("query_internal_db", {
        "query": "INSERT INTO logs (event) VALUES ('hack');"
    })
    assert "Governance Violation" in str(result)
