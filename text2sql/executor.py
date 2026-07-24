import os
import time
import duckdb
import pandas as pd
from typing import Dict, Any, Tuple

DEFAULT_DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "duckdb_warehouse",
    "warehouse.duckdb",
)


def execute_sql(
    sql_query: str, db_path: str = DEFAULT_DB_PATH
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Execute SQL query safely in DuckDB read-only mode and return DataFrame with metadata."""
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"DuckDB database file not found at: {db_path}")

    # Safety check: Block data definition and mutation queries
    upper_query = sql_query.upper().strip()
    forbidden_keywords = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE"]
    for kw in forbidden_keywords:
        if f" {kw} " in f" {upper_query} " or upper_query.startswith(kw):
            raise ValueError(
                f"Security Alert: Destructive operation '{kw}' is strictly prohibited."
            )

    start_time = time.time()
    conn = duckdb.connect(db_path, read_only=True)
    try:
        df = conn.execute(sql_query).fetchdf()
        execution_time_ms = round((time.time() - start_time) * 1000, 2)

        metadata = {
            "row_count": len(df),
            "col_count": len(df.columns),
            "execution_time_ms": execution_time_ms,
            "columns": list(df.columns),
        }
        return df, metadata
    finally:
        conn.close()


if __name__ == "__main__":
    query = "SELECT total_revenue, total_profit FROM main.total_revenue_profit;"
    df, meta = execute_sql(query)
    print("Metadata:", meta)
    print("DataFrame:\n", df)
