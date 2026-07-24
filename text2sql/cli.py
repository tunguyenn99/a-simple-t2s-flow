import argparse
import os
import sys

# Ensure parent directory is on sys.path for direct script execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table

from text2sql.executor import execute_sql
from text2sql.generator import generate_sql

console = Console()


def process_question(question: str):
    """Generate SQL from question, execute query, and display rich results."""
    console.print(
        Panel(
            f"[bold cyan]Question:[/bold cyan] {question}",
            title="🔍 Natural Language Prompt",
            border_style="cyan",
        )
    )

    with console.status("[bold green]Generating SQL query...[/bold green]"):
        sql_query = generate_sql(question)

    syntax = Syntax(sql_query, "sql", theme="monokai", line_numbers=True)
    console.print(
        Panel(syntax, title="⚡ Generated DuckDB SQL Query", border_style="green")
    )

    with console.status(
        "[bold green]Executing SQL against DuckDB Warehouse...[/bold green]"
    ):
        try:
            df, meta = execute_sql(sql_query)
        except Exception as err:
            console.print(f"[bold red]Execution Error:[/bold red] {err}")
            return

    # Render results table
    table = Table(
        title=f"📊 Results ({meta['row_count']} rows, {meta['execution_time_ms']} ms)",
        border_style="bright_blue",
    )
    for col in df.columns:
        table.add_column(str(col), style="bold yellow")

    for _, row in df.iterrows():
        table.add_row(*[str(val) for val in row])

    console.print(table)
    console.print()


def main():
    parser = argparse.ArgumentParser(
        description="Text-to-SQL Interface for E-Commerce Data Warehouse"
    )
    parser.add_argument(
        "query",
        nargs="?",
        help="Natural language question to convert to SQL and execute",
    )
    parser.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Start interactive CLI shell mode",
    )
    args = parser.parse_args()

    if args.query:
        process_question(args.query)
    elif args.interactive or not sys.stdin.isatty():
        console.print(
            Panel(
                "[bold magenta]🚀 Text-to-SQL Interactive Engine (DuckDB Warehouse)[/bold magenta]\nType your question in natural language (or 'exit' / 'q' to quit):",
                border_style="magenta",
            )
        )
        while True:
            try:
                prompt = console.input(
                    "[bold yellow]Ask Data Warehouse > [/bold yellow]"
                ).strip()
                if not prompt:
                    continue
                if prompt.lower() in ["exit", "quit", "q"]:
                    console.print("[bold green]Goodbye![/bold green]")
                    break
                process_question(prompt)
            except (KeyboardInterrupt, EOFError):
                console.print("\n[bold green]Exiting Text-to-SQL shell.[/bold green]")
                break
    else:
        # Default sample queries
        console.print(
            Panel(
                "[bold yellow]Demo Mode: Executing sample questions[/bold yellow]",
                border_style="yellow",
            )
        )
        samples = [
            "What is the total revenue and total profit?",
            "Top 5 products by revenue",
            "Show profit margin by market",
        ]
        for q in samples:
            process_question(q)


if __name__ == "__main__":
    main()
