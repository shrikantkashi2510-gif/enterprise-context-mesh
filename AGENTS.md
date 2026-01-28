# AGENTS.md - System Instructions for AI Coding Agents 🤖

## 🎯 Project Intent
You are assisting an **AI Systems Advisor** in maintaining the **Enterprise Context Mesh (ECM)**. This repository is part of a high-integrity ecosystem designed for $800k+ enterprise consulting. Your goal is to maintain absolute architectural consistency and Zero-Trust security.

## 🛠️ Critical Tech Stack
* **Runtime:** Python 3.12+ (Asyncio-driven)
* **Protocol:** Model Context Protocol (MCP) 1.0 (FastMCP 3.0)
* **Persistence:** PostgreSQL 16+ via `asyncpg`
* **Infrastructure:** Docker & Docker Compose (Zero-Trust isolation)

## 📋 Development Workflows
* **Setup:** `pip install -r requirements.txt`
* **Test:** `pytest tests/` (Mandatory before any PR)
* **Lint:** `ruff check .` (Strict enforcement of arrow functions and guard clauses)
* **Run:** `python main.py` or `docker-compose up --build -d`

## 🛡️ Non-Negotiable Rules (The Laws)
1. **Zero-Trust SQL:** Never suggest an `UPDATE`, `DELETE`, or `INSERT` query within the ECM adapters. All data retrieval must be strictly `SELECT` (Read-Only).
2. **Modular Adapters:** New data sources must inherit from `app.adapters.base.BaseAdapter`.
3. **Pydantic Contracts:** Every tool input must be validated via a model in `app/schema/models.py`.
4. **Audit Logs:** Every database interaction must include structured JSON logging via the `logger`.
5. **No Hallucinations:** If you do not know the schema of a connected legacy database, use the `list_tools` capability to discover it; do not guess column names.

## 📂 Project Tribal Knowledge
* **ECM Hub:** The central nervous system for context interoperability.
* **AI-Ops-Agent:** The external manager handling cost and governance (Interface via `.env`).
* **Eval-Platform:** The background auditor for drift detection.
* **Cursor Rules:** Refer to `.cursor/rules/*.mdc` for UI and styling preferences.

## 🤝 PR Requirements
* Every feature must include a corresponding test in `tests/test_tools.py`.
* Updates to logic require simultaneous updates to `ARCHITECTURE.md` and `GOVERNANCE.md`.
