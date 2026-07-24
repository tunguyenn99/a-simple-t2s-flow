import os
from datetime import datetime, timezone
from azure.cosmos import CosmosClient, PartitionKey
from dotenv import load_dotenv

load_dotenv()

COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT")
COSMOS_KEY = os.getenv("COSMOS_KEY")
COSMOS_DATABASE = os.getenv("COSMOS_DATABASE", "xom_ecom")
COSMOS_CONTAINER = os.getenv("COSMOS_CONTAINER", "pipeline_runs")


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
    item = {
        "id": pipeline_id,
        "pipeline_id": pipeline_id,
        "status": status,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "details": details or {},
    }
    if (
        not COSMOS_ENDPOINT
        or not COSMOS_KEY
        or "your-account" in str(COSMOS_ENDPOINT)
        or "your_cosmos" in str(COSMOS_KEY)
    ):
        print(
            f"[Cosmos DB] Skipping cloud metadata sync (credentials not set). Local run logged: {status}"
        )
        return item
    try:
        client = get_cosmos_client()
        container = ensure_database_and_container(client)
        container.upsert_item(item)
    except Exception as exc:
        print(f"[Cosmos DB Warning] Could not log run to Cosmos DB: {exc}")
    return item
