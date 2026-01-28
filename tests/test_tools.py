import pytest

@pytest.mark.asyncio
async def test_query_internal_db_happy_path(mcp_client, mocker):
    """Verifies that a valid SQL query returns the expected results."""
    # Mock the DB adapter so we don't need a real Postgres running
    mock_results = [{"id": 1, "name": "Global Corp", "revenue": 5000000}]
    mocker.patch("app.adapters.postgres_adapter.PostgresAdapter.execute_read_only", 
                 return_value=mock_results)

    # Call the tool via MCP
    # CHANGED: Argument name is now 'query' to match the function signature
    result = await mcp_client.call_tool("query_internal_db", {
        "query": "SELECT * FROM companies LIMIT 1;"
    })

    assert "Global Corp" in result
    assert "revenue" in result

@pytest.mark.asyncio
async def test_schema_validation_blocks_bad_input(mcp_client):
    """Verifies that Pydantic catches malformed inputs immediately."""
    with pytest.raises(Exception):
        # Passing an integer instead of a string query
        await mcp_client.call_tool("query_internal_db", {"sql_query": 12345})
