from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from platformdirs import user_data_dir


class JobHistory:
    def __init__(self, database: Path | None = None) -> None:
        self.database = database or Path(user_data_dir("OmniStem", "K.O.SONGS")) / "jobs.sqlite3"
        self.database.parent.mkdir(parents=True, exist_ok=True)
        self._create_schema()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database)
        connection.row_factory = sqlite3.Row
        return connection

    def _create_schema(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS jobs (
                    job_id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    status TEXT NOT NULL,
                    engine TEXT NOT NULL,
                    model TEXT,
                    input_file TEXT NOT NULL,
                    output_dir TEXT NOT NULL,
                    command_json TEXT NOT NULL,
                    manifest_path TEXT,
                    error TEXT
                )
                """
            )

    def upsert(self, record: dict[str, Any]) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO jobs (
                    job_id, status, engine, model, input_file, output_dir,
                    command_json, manifest_path, error
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(job_id) DO UPDATE SET
                    updated_at = CURRENT_TIMESTAMP,
                    status = excluded.status,
                    manifest_path = excluded.manifest_path,
                    error = excluded.error
                """,
                (
                    record["job_id"],
                    record["status"],
                    record["engine"],
                    record.get("model"),
                    record["input_file"],
                    record["output_dir"],
                    json.dumps(record.get("command", [])),
                    record.get("manifest_path"),
                    record.get("error"),
                ),
            )

    def list(self, limit: int = 50) -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM jobs ORDER BY created_at DESC LIMIT ?", (limit,)
            ).fetchall()
        return [dict(row) for row in rows]
