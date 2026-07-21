from datetime import datetime
from dlt_pipeline import run_dlt_pipeline
from cosmos_orchestrator import log_pipeline_run


def main():
    run_id = f'xom_ecom_run_{datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")}'
    try:
        pipeline = run_dlt_pipeline()
        result = log_pipeline_run(
            run_id, "success", {"pipeline_name": pipeline.pipeline_name}
        )
        print("Orchestration complete:", result)
    except Exception as exc:
        error_details = {"error": str(exc)}
        log_pipeline_run(run_id, "failed", error_details)
        raise


if __name__ == "__main__":
    main()
