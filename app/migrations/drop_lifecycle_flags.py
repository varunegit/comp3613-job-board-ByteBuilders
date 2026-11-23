"""Drop redundant application lifecycle flag columns."""

from __future__ import annotations

from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine

FLAG_COLUMNS = ("flag_reviewed", "flag_shortlisted", "flag_rejected", "flag_hired")


def run(engine: Engine) -> list[str]:
    insp = inspect(engine)
    if "application" not in insp.get_table_names():
        return []

    existing = {column["name"] for column in insp.get_columns("application")}
    dropped = [column for column in FLAG_COLUMNS if column in existing]
    with engine.begin() as connection:
        for column in dropped:
            connection.execute(text(f'ALTER TABLE application DROP COLUMN "{column}"'))
    return dropped
