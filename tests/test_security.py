import pytest

@pytest.mark.asyncio
async def test_sql_injection_protection(mcp_client):
    """Verifies that destructive SQL commands are blocked by the schema + adapter."""
    malicious_queries = [
        "DROP TABLE users;",
        "DELETE FROM records WHERE id = 1;",
        "UPDATE accounts SET balance = 999999;",
        "SELECT * FROM users; DROP TABLE metadata;"
    ]

    for query in malicious_queries:
        result = await mcp_client.call_tool("query_internal_db", {"sql_query": query})
        # The tool should return an error message rather than executing
        assert "Security Violation" in str(result) or "prohibited" in str(result).lower()

@pytest.mark.asyncio
async def test_read_only_enforcement(mcp_client, mocker):
    """Verifies that only SELECT queries are allowed."""
    result = await mcp_client.call_tool("query_internal_db", {
        "sql_query": "INSERT INTO logs (event) VALUES ('hack');"
    })
    assert "Only SELECT operations are permitted" in str(result)
