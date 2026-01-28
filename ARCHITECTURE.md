## System Architecture: The "Agentic Operating System"

The Enterprise Context Mesh sits between the **Intelligence Layer** (Claude 3.5/GPT-5) and the **Data Layer**.

### Workflow:
1. **Request:** Client (e.g., Cursor/Custom Agent) requests data.
2. **Auth Layer:** ECM verifies credentials via my [AI Ops Agent] middleware.
3. **MCP Routing:** ECM determines if the data lives in SQL (Postgres) or Cloud (Salesforce).
4. **Execution:** The specific MCP Adapter executes a least-privilege query.
5. **Validation:** Results are passed through the [Eval Platform] for drift/safety checks before reaching the LLM.
