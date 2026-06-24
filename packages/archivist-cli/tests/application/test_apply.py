from __future__ import annotations

from archivist_cli.application.apply import apply
from archivist_cli.domain.models import ApplyEventStatus
from archivist_cli.domain.ports import FilesystemError
from tests.fakes import FakeFilesystem

TARGET = "file:///archive"
NON_CLASSE = f"{TARGET}/_Non classé"


def _make_fs(*files: str) -> FakeFilesystem:
    fs = FakeFilesystem()
    fs.add_dir(f"{TARGET}/_Réception")
    fs.add_dir(NON_CLASSE)
    fs.add_dir(f"{TARGET}/Mes achats/Mes factures fournisseurs/2026-03")
    for f in files:
        fs.add_file(f)
    return fs


def test_apply_classified_moves_file():
    src = f"{TARGET}/_Réception/facture.pdf"
    dest = f"{TARGET}/Mes achats/Mes factures fournisseurs/2026-03/2026-03_Facture_OVH_F001.pdf"
    fs = _make_fs(src)

    result = apply(
        filesystem=fs,
        decisions=[{"uri": src, "name": "facture.pdf", "status": "classified", "dest_uri": dest}],
        non_classe_uri=NON_CLASSE,
    )

    assert result.moved == 1
    assert result.failed == 0
    event = result.events[0]
    assert event.status == ApplyEventStatus.MOVED
    assert event.dest_uri == dest
    assert fs.exists(dest)
    assert not fs.exists(src)


def test_apply_unclassified_goes_to_non_classe():
    src = f"{TARGET}/_Réception/unknown.pdf"
    fs = _make_fs(src)

    result = apply(
        filesystem=fs,
        decisions=[{"uri": src, "name": "unknown.pdf", "status": "unclassified"}],
        non_classe_uri=NON_CLASSE,
    )

    assert result.moved == 1
    event = result.events[0]
    assert event.status == ApplyEventStatus.MOVED
    assert event.dest_uri == f"{NON_CLASSE}/unknown.pdf"
    assert fs.exists(f"{NON_CLASSE}/unknown.pdf")
    assert not fs.exists(src)


def test_apply_failed_goes_to_non_classe():
    src = f"{TARGET}/_Réception/broken.pdf"
    fs = _make_fs(src)

    result = apply(
        filesystem=fs,
        decisions=[{"uri": src, "name": "broken.pdf", "status": "failed", "reason": "metadata_error"}],
        non_classe_uri=NON_CLASSE,
    )

    assert result.moved == 1
    assert fs.exists(f"{NON_CLASSE}/broken.pdf")
    assert not fs.exists(src)


def test_apply_stale_source_skipped():
    """Fichier déjà absent (état périmé) → skipped sans erreur."""
    src = f"{TARGET}/_Réception/already_gone.pdf"
    dest = f"{TARGET}/Mes achats/Mes factures fournisseurs/2026-03/out.pdf"
    fs = _make_fs()  # src n'existe pas

    result = apply(
        filesystem=fs,
        decisions=[{"uri": src, "name": "already_gone.pdf", "status": "classified", "dest_uri": dest}],
        non_classe_uri=NON_CLASSE,
    )

    assert result.skipped == 1
    assert result.moved == 0
    assert result.failed == 0
    event = result.events[0]
    assert event.status == ApplyEventStatus.SKIPPED
    assert event.reason == "source_not_found"


def test_apply_summary_line_ignored():
    """La ligne summary de classify (sans uri) est ignorée silencieusement."""
    src = f"{TARGET}/_Réception/facture.pdf"
    dest = f"{TARGET}/Mes achats/Mes factures fournisseurs/2026-03/out.pdf"
    fs = _make_fs(src)

    decisions = [
        {"scanned": 1, "classified": 1, "unclassified": 0, "failed": 0},  # summary line
        {"uri": src, "name": "facture.pdf", "status": "classified", "dest_uri": dest},
    ]

    result = apply(filesystem=fs, decisions=decisions, non_classe_uri=NON_CLASSE)

    assert result.moved == 1


def test_apply_missing_dest_uri_fails():
    """Décision classified sans dest_uri → event FAILED."""
    src = f"{TARGET}/_Réception/facture.pdf"
    fs = _make_fs(src)

    result = apply(
        filesystem=fs,
        decisions=[{"uri": src, "name": "facture.pdf", "status": "classified"}],
        non_classe_uri=NON_CLASSE,
    )

    assert result.failed == 1
    event = result.events[0]
    assert event.status == ApplyEventStatus.FAILED
    assert "dest_uri" in event.reason


def test_apply_filesystem_error_returns_failed():
    class FailingMoveFs(FakeFilesystem):
        def move_file(self, src_uri: str, dest_uri: str) -> None:
            raise FilesystemError("disk full")

    src = f"{TARGET}/_Réception/facture.pdf"
    dest = f"{TARGET}/Mes achats/Mes factures fournisseurs/2026-03/out.pdf"
    fs = FailingMoveFs()
    fs.add_dir(f"{TARGET}/_Réception")
    fs.add_dir(NON_CLASSE)
    fs.add_dir(f"{TARGET}/Mes achats/Mes factures fournisseurs/2026-03")
    fs.add_file(src)

    result = apply(
        filesystem=fs,
        decisions=[{"uri": src, "name": "facture.pdf", "status": "classified", "dest_uri": dest}],
        non_classe_uri=NON_CLASSE,
    )

    assert result.failed == 1
    assert result.moved == 0


def test_apply_empty_decisions():
    fs = _make_fs()
    result = apply(filesystem=fs, decisions=[], non_classe_uri=NON_CLASSE)
    assert result.moved == 0
    assert result.skipped == 0
    assert result.failed == 0


def test_apply_multiple_mixed():
    """Mélange classified / unclassified / stale → tous traités indépendamment."""
    src_ok = f"{TARGET}/_Réception/facture.pdf"
    src_unk = f"{TARGET}/_Réception/unknown.pdf"
    src_gone = f"{TARGET}/_Réception/gone.pdf"
    dest_ok = f"{TARGET}/Mes achats/Mes factures fournisseurs/2026-03/out.pdf"
    fs = _make_fs(src_ok, src_unk)

    decisions = [
        {"uri": src_ok, "name": "facture.pdf", "status": "classified", "dest_uri": dest_ok},
        {"uri": src_unk, "name": "unknown.pdf", "status": "unclassified"},
        {"uri": src_gone, "name": "gone.pdf", "status": "classified", "dest_uri": f"{TARGET}/somewhere/gone.pdf"},
    ]

    result = apply(filesystem=fs, decisions=decisions, non_classe_uri=NON_CLASSE)

    assert result.moved == 2
    assert result.skipped == 1
    assert result.failed == 0
