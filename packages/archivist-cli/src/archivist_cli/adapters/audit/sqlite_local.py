from __future__ import annotations

import sqlite3
from contextlib import closing
from pathlib import Path
from typing import ClassVar

from archivist_cli.config import app_data_dir
from archivist_cli.domain.models import AuditSession
from archivist_cli.domain.ports import AuditLog, AuditLogError

_CREATE_SESSIONS = """
CREATE TABLE IF NOT EXISTS audit_sessions (
    session_id      TEXT PRIMARY KEY,
    started_at      TEXT NOT NULL,
    ended_at        TEXT NOT NULL,
    referentiel_uri TEXT NOT NULL,
    root_uri        TEXT NOT NULL,
    scanned         INTEGER NOT NULL,
    classified      INTEGER NOT NULL,
    unclassified    INTEGER NOT NULL,
    failed          INTEGER NOT NULL
)
"""

_CREATE_EVENTS = """
CREATE TABLE IF NOT EXISTS audit_events (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id  TEXT NOT NULL REFERENCES audit_sessions(session_id),
    file_name   TEXT NOT NULL,
    file_uri    TEXT NOT NULL,
    status      TEXT NOT NULL,
    entry_id    TEXT,
    dest_name   TEXT,
    dest_uri    TEXT,
    error_code  TEXT,
    llm_reason  TEXT
)
"""


class SqliteAuditLog(AuditLog):
    VERSION: ClassVar[int] = 1

    def __init__(self, db_path: Path | None = None) -> None:
        self._db_path = db_path or (app_data_dir() / "audit.db")

    def write(self, session: AuditSession) -> None:
        try:
            self._db_path.parent.mkdir(parents=True, exist_ok=True)
            with closing(sqlite3.connect(self._db_path)) as con:
                con.execute("PRAGMA journal_mode=WAL")
                con.execute(_CREATE_SESSIONS)
                con.execute(_CREATE_EVENTS)
                with con:
                    con.execute(
                        "INSERT INTO audit_sessions VALUES (?,?,?,?,?,?,?,?,?)",
                        (
                            session.session_id,
                            session.started_at,
                            session.ended_at,
                            session.referentiel_uri,
                            session.root_uri,
                            session.scanned,
                            session.classified,
                            session.unclassified,
                            session.failed,
                        ),
                    )
                    con.executemany(
                        """INSERT INTO audit_events
                           (session_id, file_name, file_uri, status,
                            entry_id, dest_name, dest_uri, error_code, llm_reason)
                           VALUES (?,?,?,?,?,?,?,?,?)""",
                        [
                            (
                                session.session_id,
                                e.name,
                                e.uri,
                                e.status.value,
                                e.entry_id,
                                e.dest_name,
                                e.dest_uri,
                                e.error_code,
                                e.llm_reason,
                            )
                            for e in session.events
                        ],
                    )
        except sqlite3.Error as exc:
            raise AuditLogError(str(exc)) from exc
