"""CLI command for generating activity reports."""

import click


@click.command()
@click.option("--from", "from_date", required=True, help="Start date (YYYY-MM-DD)")
@click.option("--to", "to_date", required=True, help="End date (YYYY-MM-DD)")
@click.option("--output", "-o", help="Output file path (stdout if not specified)")
def generate_report(from_date: str, to_date: str, output: str = None):
    """Generate activity report for a date range (placeholder implementation).

    Example:
        python -m src.cli --from 2025-01-01 --to 2025-01-07
        python -m src.cli --from 2025-01-01 --to 2025-01-07 -o report.md
    """
    print(f"Hello generate report from {from_date} to {to_date}")
    if output:
        print(f"Output will be saved to: {output}")
    # TODO: Implement report generation from daily_summaries


if __name__ == "__main__":
    generate_report()
