import os
import duckdb

DEFAULT_DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "duckdb_warehouse",
    "warehouse.duckdb",
)


def get_warehouse_schema(db_path: str = DEFAULT_DB_PATH) -> str:
    """Introspect DuckDB database tables, columns, and data types to construct LLM context."""
    if not os.path.exists(db_path):
        return "Database file not found."

    conn = duckdb.connect(db_path, read_only=True)
    try:
        tables = conn.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'main' ORDER BY table_name"
        ).fetchall()

        schema_ddl = []
        for (table_name,) in tables:
            cols = conn.execute(
                f"""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = '{table_name}' AND table_schema = 'main'
                ORDER BY ordinal_position
            """
            ).fetchall()

            col_defs = [f"  {col} {dtype}" for col, dtype in cols]
            table_ddl = (
                f"CREATE TABLE main.{table_name} (\n" + ",\n".join(col_defs) + "\n);"
            )
            schema_ddl.append(table_ddl)

        return "\n\n".join(schema_ddl)
    finally:
        conn.close()


if __name__ == "__main__":
    print(get_warehouse_schema())
