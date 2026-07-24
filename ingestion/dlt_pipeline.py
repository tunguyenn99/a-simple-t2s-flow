import os
import dlt
import pymssql
from dotenv import load_dotenv

load_dotenv()

OLTP_HOST = os.getenv("OLTP_HOST")
OLTP_PORT = os.getenv("OLTP_PORT", "1433")
OLTP_DATABASE = os.getenv("OLTP_DATABASE")
OLTP_USERNAME = os.getenv("OLTP_USERNAME")
OLTP_PASSWORD = os.getenv("OLTP_PASSWORD")
DUCKDB_PATH = os.getenv("DUCKDB_PATH", "duckdb_warehouse/warehouse.duckdb")

if not all([OLTP_HOST, OLTP_DATABASE, OLTP_USERNAME, OLTP_PASSWORD]):
    raise ValueError(
        "Please configure OLTP_HOST, OLTP_DATABASE, OLTP_USERNAME, OLTP_PASSWORD in .env"
    )


def get_sql_server_connection():
    return pymssql.connect(
        server=OLTP_HOST,
        port=int(OLTP_PORT),
        user=OLTP_USERNAME,
        password=OLTP_PASSWORD,
        database=OLTP_DATABASE,
    )


def query_table(table_name):
    with get_sql_server_connection() as conn:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(f"SELECT * FROM e_commerce.{table_name}")
        while True:
            rows = cursor.fetchmany(1000)
            if not rows:
                break
            for row in rows:
                yield row


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

    return [customer, ecom_sales, product, region]


def run_dlt_pipeline():
    os.makedirs(os.path.dirname(os.path.abspath(DUCKDB_PATH)), exist_ok=True)
    pipeline = dlt.pipeline(
        pipeline_name="xom_ecom_warehouse",
        destination=dlt.destinations.duckdb(DUCKDB_PATH),
        dataset_name="xom_ecom",
    )
    pipeline.run(sqlserver_source())
    return pipeline


if __name__ == "__main__":
    run_dlt_pipeline()
