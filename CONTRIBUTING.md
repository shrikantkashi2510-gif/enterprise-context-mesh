# Contributing to Enterprise Context Mesh (ECM) 🛠️

Thank you for contributing to the ECM ecosystem. To maintain the **$800k-tier architectural standards** required for enterprise AI governance, we follow a strict "Professional-Grade" development workflow.

## 1. Our Engineering Philosophy
* **Safety Over Speed:** Security and governance checks are mandatory. We never trade off Zero-Trust principles for feature velocity.
* **Modular First:** Data adapters must remain decoupled from core logic.
* **Documentation is Code:** A feature is not complete until its corresponding `ARCHITECTURE.md` and `GOVERNANCE.md` sections are updated.

## 2. Development Workflow (The SOP)
We follow a structured Git-Flow process to ensure production stability:

1. **Branching:** Create a feature branch using the following naming convention:
   * `feat/feature-name` (for new adapters/tools)
   * `fix/issue-name` (for security/logic bug fixes)
   * `docs/update-name` (for governance/architecture updates)
2. **Coding Standards:** We use **Cursor** as our primary IDE. Ensure your local environment is configured with our `.cursorignore` and `ruff` linting rules.
3. **Tests First:** Every PR must include passing unit tests in the `tests/` directory, specifically covering **Schema Validation** and **Security Guardrails**.

## 3. Tool Development Guidelines (MCP Adapters)
When building a new data adapter (e.g., MongoDB, Snowflake):
* **Inheritance:** It MUST inherit from `app.adapters.base.BaseAdapter`.
* **Read-Only:** You must explicitly enforce a read-only session in the connection logic.
* **Schema:** You must define a corresponding Pydantic model in `app/schema/models.py`.

## 4. Quality Gate Checklist
Before submitting a Pull Request, ensure:
- [ ] `pytest tests/` returns 100% pass rate.
- [ ] `ruff check .` passes without errors (Linting).
- [ ] Docker build succeeds: `docker-compose build`.
- [ ] No secrets or `.env` files are tracked in git history.
- [ ] All new MCP tools have detailed docstrings for LLM intent discovery.

## 5. Security & Disclosure
If you discover a security vulnerability, **do not open a public issue.** Please email the Lead Advisor directly at [advisory.shrikant@gmail.com] to initiate a coordinated disclosure.

---
**Lead Advisor:** [Shrikant Kashi/AI Architect Advisor]  
**Operating Standard:** 2026 Enterprise-Grade AI Operations
