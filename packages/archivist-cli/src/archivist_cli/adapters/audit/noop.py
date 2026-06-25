from __future__ import annotations

from typing import ClassVar

from archivist_cli.domain.models import AuditSession
from archivist_cli.domain.ports import AuditLog


class NoopAuditLog(AuditLog):
    VERSION: ClassVar[int] = 1

    def write(self, session: AuditSession) -> None:
        pass
