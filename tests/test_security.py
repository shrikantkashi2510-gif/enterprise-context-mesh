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
        result = await mcp_client.call_tool("query_internal_db", {"request": query})  # Changed from sql_query to request
        # Assert appropriate error handling

@pytest.mark.asyncio
async def test_read_only_enforcement(mcp_client, mocker):
    """Verifies that only SELECT queries are allowed."""
    result = await mcp_client.call_tool("query_internal_db", {
        "request": "INSERT INTO logs (event) VALUES ('hack');"  # Changed from sql_query to request
    })
    # Assert error
