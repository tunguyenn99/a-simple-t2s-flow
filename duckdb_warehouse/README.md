# 💾 DuckDB Warehouse Directory (`duckdb_warehouse/`)

This directory serves as the centralized storage location for the **DuckDB Analytical Data Warehouse** file (`warehouse.duckdb`).

---

## 📁 Storage Structure

| Asset | Description |
| :--- | :--- |
| **`warehouse.duckdb`** | Central embedded DuckDB database storing all Bronze, Silver, and Gold analytical tables. |
| **`warehouse.duckdb.wal`** | DuckDB Write-Ahead Log (WAL) temporary transaction log file (if active). |

---

## 🔍 How to Inspect Database Directly

Using Python inside `.venv`:
```python
import duckdb

conn = duckdb.connect("duckdb_warehouse/warehouse.duckdb", read_only=True)
print(conn.execute("SHOW TABLES;").fetchdf())
```
