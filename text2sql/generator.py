import os
import re
import sqlglot
from dotenv import load_dotenv

load_dotenv()

from text2sql.schema import get_warehouse_schema

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")


def generate_sql_gemini(user_prompt: str, schema_ddl: str) -> str:
    """Generate DuckDB SQL using Google Gemini API."""
    try:
        from google import genai

        client = genai.Client(api_key=GEMINI_API_KEY)
        system_instruction = (
            "You are an expert Data Engineer and DuckDB SQL developer.\n"
            "Given the DuckDB warehouse schema DDL below, write a single valid SQL query for DuckDB dialect.\n"
            "Rules:\n"
            "1. Output ONLY the raw SQL code block or raw SQL string. Do NOT include markdown text outside sql block.\n"
            "2. Prefer using Silver models (main.silver_ecom_sales, main.silver_customer, etc.) or Gold analytics models (main.total_revenue_profit, main.top_10_products, main.revenue_by_segment, main.customer_rfm_segments, main.vip_churn_risk, main.monthly_revenue_yoy, main.profit_margin_by_market) for queries.\n"
            "3. Do NOT execute any mutation queries (NO INSERT, UPDATE, DELETE, DROP, ALTER).\n"
            "4. Always use COUNT(DISTINCT column_name) when counting unique entities (e.g. COUNT(DISTINCT order_id) for orders, COUNT(DISTINCT customer_id) for customers).\n"
            f"\n--- DATABASE SCHEMA DDL ---\n{schema_ddl}\n"
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{system_instruction}\nUser Question: {user_prompt}",
        )

        raw_sql = response.text.strip()
        # Clean markdown formatting if present
        raw_sql = re.sub(r"^```sql\s*", "", raw_sql, flags=re.IGNORECASE)
        raw_sql = re.sub(r"^```\s*", "", raw_sql)
        raw_sql = re.sub(r"\s*```$", "", raw_sql).strip()
        return raw_sql
    except Exception as exc:
        print(
            f"[Text2SQL LLM Warning] Gemini API call failed: {exc}. Falling back to rule engine."
        )
        return generate_sql_fallback(user_prompt)


def generate_sql_fallback(user_prompt: str) -> str:
    """Smart heuristic rule-based SQL generator for common domain analytics questions."""
    prompt_lower = user_prompt.lower()

    if (
        "total" in prompt_lower
        or "overall" in prompt_lower
        or (
            "revenue" in prompt_lower
            and "profit" in prompt_lower
            and "segment" not in prompt_lower
        )
    ):
        return "SELECT total_revenue, total_profit FROM main.total_revenue_profit;"

    if (
        "segment" in prompt_lower
        or "corporate" in prompt_lower
        or "consumer" in prompt_lower
    ):
        return "SELECT segment, revenue, profit FROM main.revenue_by_segment ORDER BY revenue DESC;"

    if "market" in prompt_lower or "margin" in prompt_lower:
        return "SELECT market, profit_margin FROM main.profit_margin_by_market ORDER BY profit_margin DESC;"

    if (
        "product" in prompt_lower
        or "top product" in prompt_lower
        or "best selling" in prompt_lower
    ):
        return "SELECT product_id, product_name, order_count, revenue, profit FROM main.top_10_products ORDER BY revenue DESC LIMIT 10;"

    if "country" in prompt_lower or "countries" in prompt_lower:
        return "SELECT country, revenue, unique_customers FROM main.top_15_countries_by_revenue ORDER BY revenue DESC LIMIT 15;"

    if "rfm" in prompt_lower or "churn" in prompt_lower or "vip" in prompt_lower:
        return "SELECT customer_id, order_count, total_revenue, days_since_last_order, churn_risk FROM main.vip_churn_risk ORDER BY total_revenue DESC LIMIT 10;"

    if (
        "monthly" in prompt_lower
        or "trend" in prompt_lower
        or "month" in prompt_lower
        or "yoy" in prompt_lower
    ):
        return "SELECT month_date, revenue, revenue_change, change_pct FROM main.monthly_revenue_yoy ORDER BY month_date ASC;"

    if "discount" in prompt_lower or "category" in prompt_lower:
        return "SELECT category, avg_discount FROM main.avg_discount_by_category ORDER BY avg_discount DESC;"

    # Default fallback: Sample sales from Silver
    return "SELECT order_id, customer_id, product_id, segment, market, revenue, profit, order_date FROM main.silver_ecom_sales LIMIT 10;"


def generate_sql(user_prompt: str, db_path: str = None) -> str:
    """Generate formatted DuckDB SQL query from natural language text."""
    schema_ddl = get_warehouse_schema(db_path) if db_path else get_warehouse_schema()

    if GEMINI_API_KEY and not GEMINI_API_KEY.startswith("your_"):
        sql = generate_sql_gemini(user_prompt, schema_ddl)
    else:
        sql = generate_sql_fallback(user_prompt)

    # Validate and format with sqlglot
    try:
        formatted_sql = sqlglot.transpile(
            sql, read="duckdb", write="duckdb", pretty=True
        )[0]
        return formatted_sql
    except Exception:
        return sql


if __name__ == "__main__":
    test_query = "What is the total revenue and profit?"
    print(f"Prompt: '{test_query}'\nGenerated SQL:\n{generate_sql(test_query)}")
