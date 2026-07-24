.PHONY: help install ingest dbt-run dbt-test dbt-clean orchestrate charts format lint lint-fix check-all run-all

# Default target
.DEFAULT_GOAL := help

# Python Virtual Environment Binary Path
VENV_BIN := .venv/bin
PYTHON := $(VENV_BIN)/python
DBT := $(VENV_BIN)/dbt
BLACK := $(VENV_BIN)/black
SQLFLUFF := $(VENV_BIN)/sqlfluff

help: ## Display available commands
	@echo "======================================================================="
	@echo " 🚀 E-Commerce Data Warehouse Pipeline - Makefile Commands"
	@echo "======================================================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo "======================================================================="

install: ## Install python dependencies into virtual environment
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

ingest: ## Run DLT ingestion from SQL Server to DuckDB
	$(PYTHON) ingestion/dlt_pipeline.py

dbt-run: ## Run dbt models (Bronze -> Silver -> Gold)
	$(DBT) run --project-dir dbt_model --profiles-dir dbt_model

dbt-test: ## Run dbt data tests and assertions
	$(DBT) test --project-dir dbt_model --profiles-dir dbt_model

dbt-clean: ## Clean dbt compiled target directory
	$(DBT) clean --project-dir dbt_model

orchestrate: ## Run full end-to-end ETL orchestrator workflow
	$(PYTHON) orchestration/orchestrator.py

charts: ## Generate business analytics dashboard charts
	$(PYTHON) docs/chart_generation/generate_charts.py

text2sql: ## Run interactive Text-to-SQL query interface
	$(PYTHON) -m text2sql.cli --interactive

format: ## Format Python codebase using Black
	$(BLACK) ingestion/ orchestration/ docs/chart_generation/ text2sql/

lint: ## Lint dbt SQL models using SQLFluff
	$(SQLFLUFF) lint dbt_model/models --dialect duckdb

lint-fix: ## Automatically fix dbt SQL formatting issues using SQLFluff
	$(SQLFLUFF) fix dbt_model/models --dialect duckdb

check-all: ## Run Python formatting check and SQL linting
	$(BLACK) --check ingestion/ orchestration/ docs/chart_generation/ text2sql/
	$(SQLFLUFF) lint dbt_model/models --dialect duckdb

run-all: ingest dbt-run charts ## Run full pipeline end-to-end (Ingest -> dbt -> Charts)
