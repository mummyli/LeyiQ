# 📘 LeyiQ: Trust Your Data, Simplify Quality

LeyiQ is a **modular, extensible data quality platform**.
It provides **unified rule definition, batch/stream execution, metrics & auditing**.

---

## 🚀 Features

* **Unified Rule Model** (YAML → internal `Rule`)
  * Supports row-level checks, SQL/aggregate rules, lookup-based validation.
  * Metadata-driven: severity, owner, tags, version, test cases.

* **Execution Modes**
  * **StreamExecutor** (Kafka): real-time event validation with DLQ & retry hooks.
  * **SparkExecutor** (batch): SQL compilation + aggregation + failure sampling.

* **Rule Governance**
  * Versioned rules stored in PostgreSQL (via `rule_registry_pg.py`).
  * REST API for rule CRUD & activation.

* **Observability & Auditing**
  * Prometheus metrics (`/metrics`) for processing stats & rule failures.
  * Audit log with sample export (JSON/CSV).

* **UI & API**
  * Lightweight static UI (upload rules, trigger jobs, view metrics).
  * FastAPI service for rule management & execution orchestration.

* **Production Ready**
  * Docker & Docker Compose (Postgres + API + UI + Prometheus).
  * Kubernetes manifests & Helm chart skeletons.
