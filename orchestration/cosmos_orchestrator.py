import os
from datetime import datetime
from azure.cosmos import CosmosClient, PartitionKey
from dotenv import load_dotenv

load_dotenv()

COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT")
COSMOS_KEY = os.getenv("COSMOS_KEY")
COSMOS_DATABASE = os.getenv("COSMOS_DATABASE", "xom_ecom")
COSMOS_CONTAINER = os.getenv("COSMOS_CONTAINER", "pipeline_runs")

if not all([COSMOS_ENDPOINT, COSMOS_KEY]):
    raise ValueError("Please configure COSMOS_ENDPOINT and COSMOS_KEY in .env")


def get_cosmos_client():
    return CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)


def ensure_database_and_container(client):
    database = client.create_database_if_not_exists(id=COSMOS_DATABASE)
    container = database.create_container_if_not_exists(
        id=COSMOS_CONTAINER,
        partition_key=PartitionKey(path="/pipeline_id"),
        offer_throughput=400,
    )
    return container


def log_pipeline_run(pipeline_id, status, details=None):
    client = get_cosmos_client()
    container = ensure_database_and_container(client)
    item = {
        "id": pipeline_id,
        "pipeline_id": pipeline_id,
        "status": status,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "details": details or {},
    }
    container.upsert_item(item)
    return item
