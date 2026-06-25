from __future__ import annotations

from pathlib import Path

import pytest

from tests.adapters.test_contracts import AuditLogContractSuite
from archivist_cli.adapters.audit.sqlite_local import SqliteAuditLog
from archivist_cli.domain.ports import AuditLog


class TestSqliteAuditLogContract(AuditLogContractSuite):
    @pytest.fixture
    def audit_log(self, tmp_path: Path) -> AuditLog:
        return SqliteAuditLog(db_path=tmp_path / "audit.db")
