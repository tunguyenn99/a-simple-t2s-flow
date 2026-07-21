import os
import pyodbc
import dlt
from dotenv import load_dotenv

load_dotenv()

SQL_SERVER_DRIVER = os.getenv("SQL_SERVER_DRIVER", "ODBC Driver 18 for SQL Server")
OLTP_HOST = os.getenv("OLTP_HOST")
OLTP_PORT = os.getenv("OLTP_PORT", "1433")
OLTP_DATABASE = os.getenv("OLTP_DATABASE")
OLTP_USERNAME = os.getenv("OLTP_USERNAME")
OLTP_PASSWORD = os.getenv("OLTP_PASSWORD")
DUCKDB_PATH = os.getenv("DUCKDB_PATH", "data/warehouse.duckdb")

if not all([OLTP_HOST, OLTP_DATABASE, OLTP_USERNAME, OLTP_PASSWORD]):
    raise ValueError(
        "Please configure OLTP_HOST, OLTP_DATABASE, OLTP_USERNAME, OLTP_PASSWORD in .env"
    )


def get_sql_server_connection():
    conn_str = (
        f"DRIVER={{{SQL_SERVER_DRIVER}}};"
        f"SERVER={OLTP_HOST},{OLTP_PORT};"
        f"DATABASE={OLTP_DATABASE};"
        f"UID={OLTP_USERNAME};"
        f"PWD={OLTP_PASSWORD};"
        "Trusted_Connection=no;"
    )
    return pyodbc.connect(conn_str)


def query_table(table_name):
    with get_sql_server_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        columns = [col[0] for col in cursor.description]
        for row in cursor:
            yield dict(zip(columns, row))


@dlt.source
def sqlserver_source():
    @dlt.resource(write_disposition="replace")
    def customer():
        return query_table("customer")

    @dlt.resource(write_disposition="replace")
    def ecom_sales():
        return query_table("ecom_sales")

    @dlt.resource(write_disposition="replace")
    def product():
        return query_table("product")

    @dlt.resource(write_disposition="replace")
    def region():
        return query_table("region")

    return {
        "customer": customer,
        "ecom_sales": ecom_sales,
        "product": product,
        "region": region,
    }


def run_dlt_pipeline():
    pipeline = dlt.pipeline(
        pipeline_name="xom_ecom_warehouse",
        destination="duckdb",
        dataset_name="xom_ecom",
        full_refresh=True,
    )
    pipeline.run(sqlserver_source())
    return pipeline


if __name__ == "__main__":
    run_dlt_pipeline()
