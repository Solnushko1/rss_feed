"""Click commands."""

import sys
from pathlib import Path

import click

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent
TEST_PATH = PROJECT_ROOT / "tests"


@click.command()
@click.option(
    "-c/-C",
    "--coverage/--no-coverage",
    default=True,
    is_flag=True,
    help="Show coverage report",
)
@click.option(
    "-k",
    "--filter",
    default=None,
    help="Filter tests by keyword expressions",
)
def test(coverage, filter) -> None:  # noqa: A002
    """Run the tests."""
    import pytest

    args = [TEST_PATH, "--verbose"]
    if coverage:
        args.append("--cov=rss_feed")
    if filter:
        args.extend(["-k", filter])
    rv = pytest.main(args=args)
    sys.exit(rv)
