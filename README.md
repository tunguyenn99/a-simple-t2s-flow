# a-simple-t2s-flow

Text-to-SQL pipeline using dbt + DuckDB + DLT, with Cosmos orchestration metadata.

## Mục tiêu
- Chuyển dữ liệu từ SQL Server OLTP vào DuckDB để làm luồng OLTP → OLAP.
- Xây dựng warehouse với dbt theo 3 layer: bronze, silver, gold.
- Tạo pipeline DLT load dữ liệu vào DuckDB.
- Ghi metadata / orchestrator run states lên Cosmos DB.

## Cài đặt
1. Sao chép file cấu hình mẫu:
   ```bash
   cp .env.example .env
   ```
2. Thiết lập `.env` với thông tin SQL Server và DuckDB.
3. Kích hoạt môi trường ảo project:
   ```bash
   source .venv/bin/activate
   ```
4. Cài dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Cấu trúc project
- `.venv/`: virtual environment riêng của project.
- `.env`: cấu hình môi trường (không nên commit).
- `dbt_project.yml`: cấu hình dự án dbt.
- `profiles.yml`: cấu hình adapter DuckDB cho dbt.
- `models/bronze/`: load dữ liệu raw 1-1.
- `models/silver/`: clean và đổi kiểu dữ liệu.
- `models/gold/`: các model trả lời câu hỏi trong `context.md`.
- `analysis/`: nơi chứa các các analysis macro hoặc query khám phá.
- `snapshots/`: nơi chứa snapshots nếu cần ghi phiên bản dữ liệu.
- `seeds/`: nơi chứa dữ liệu seed tĩnh.
- `tests/`: nơi chứa tests của dbt.
- `dlt/`: mã pipeline DLT.
- `orchestration/`: mã orchestration và logging Cosmos.

## Sử dụng
- Chạy DLT pipeline:
  ```bash
  source .venv/bin/activate
  python dlt_pipeline.py
  ```
- Chạy dbt models:
  ```bash
  source .venv/bin/activate
  dbt run
  ```
- Chạy orchestrator:
  ```bash
  source .venv/bin/activate
  python orchestrator.py
  ```

## Lint và định dạng
- Cài thêm dependencies bằng:
  ```bash
  source .venv/bin/activate
  pip install -r requirements.txt
  ```
- Định dạng Python với Black:
  ```bash
  black .
  ```
- Kiểm tra SQL với SQLFluff:
  ```bash
  sqlfluff lint models/**/*.sql
  sqlfluff fix models/**/*.sql
  ```
- Cài và kích hoạt `pre-commit` hook:
  ```bash
  source .venv/bin/activate
  pip install -r requirements.txt
  pre-commit install
  pre-commit run --all-files
  ```

## Lưu ý
- `.env` hiện tại dùng SQL Server làm nguồn OLTP.
- DuckDB path mặc định là `data/warehouse.duckdb`.
- Nếu muốn cùng data qua Azure Cosmos, cấu hình thêm `COSMOS_ENDPOINT` và `COSMOS_KEY`.
