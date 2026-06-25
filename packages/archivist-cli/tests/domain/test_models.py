from __future__ import annotations

from archivist_cli.domain.models import (
    ClassifyEvent, ClassifyEventStatus, ClassifyResult,
    FileNaming, FileNamingField, ReferentielEntry,
)


def test_entry_from_dict_minimal():
    raw = {
        "id": "ma_banque",
        "folder_name": "Ma banque",
        "path": "Ma banque",
        "dynamic": False,
        "option": "core",
        "required": True,
    }
    entry = ReferentielEntry.from_dict(raw)
    assert entry.id == "ma_banque"
    assert entry.folder_name == "Ma banque"
    assert entry.path == "Ma banque"
    assert entry.dynamic is False
    assert entry.option == "core"
    assert entry.required is True
    assert entry.parent is None


def test_entry_from_dict_with_parent():
    raw = {
        "id": "ma_banque.rib",
        "folder_name": "Mes RIB",
        "path": "Ma banque/Mes RIB",
        "parent": "ma_banque",
        "dynamic": False,
        "option": "core",
        "required": True,
    }
    entry = ReferentielEntry.from_dict(raw)
    assert entry.parent == "ma_banque"


def test_entry_is_scaffoldable_static():
    entry = ReferentielEntry(
        id="ma_banque",
        folder_name="Ma banque",
        path="Ma banque",
        dynamic=False,
        option="core",
        required=True,
    )
    assert entry.is_scaffoldable is True


def test_entry_is_not_scaffoldable_when_dynamic():
    entry = ReferentielEntry(
        id="archives.annee",
        folder_name="[AAAA]",
        path="Archives/[AAAA]",
        dynamic=True,
        option="core",
        required=True,
    )
    assert entry.is_scaffoldable is False


def test_entry_is_not_scaffoldable_when_dynamic_without_placeholder():
    entry = ReferentielEntry(
        id="custom_dynamic",
        folder_name="Custom",
        path="Custom/Folder",
        dynamic=True,
        option="core",
        required=True,
    )
    assert entry.is_scaffoldable is False


def test_entry_is_not_scaffoldable_when_path_has_placeholder():
    entry = ReferentielEntry(
        id="mes_ventes.clients.nom_client.contrats",
        folder_name="Contrats",
        path="Mes ventes/Mes clients/[Nom du client]/Contrats",
        dynamic=False,
        option="core",
        required=True,
    )
    assert entry.is_scaffoldable is False


def test_referentiel_entry_loads_file_naming():
    raw = {
        "id": "mes_achats.factures_fournisseurs",
        "folder_name": "Mes factures fournisseurs",
        "path": "Mes achats/Mes factures fournisseurs",
        "dynamic": False,
        "option": "core",
        "required": True,
        "description": "Factures reçues",
        "file_naming": {
            "pattern": "[AAAA-MM]_Facture_[Nom fournisseur]_[Numero].[ext]",
            "fields": [
                {"name": "AAAA-MM", "description": "date d'émission"},
                {"name": "Nom fournisseur", "description": "nom du fournisseur"},
                {"name": "Numero", "description": "numéro de facture"},
                {"name": "ext", "description": "extension"},
            ],
        },
        "organization": {"type": "chronological", "subfolder_pattern": "AAAA-MM"},
    }
    entry = ReferentielEntry.from_dict(raw)
    assert entry.description == "Factures reçues"
    assert entry.file_naming is not None
    assert entry.file_naming.pattern == "[AAAA-MM]_Facture_[Nom fournisseur]_[Numero].[ext]"
    assert len(entry.file_naming.fields) == 4
    assert entry.file_naming.fields[0] == FileNamingField(name="AAAA-MM", description="date d'émission")
    assert entry.organization_type == "chronological"
    assert entry.organization_subfolder_pattern == "AAAA-MM"


def test_referentiel_entry_without_file_naming():
    raw = {
        "id": "reception",
        "folder_name": "_Réception",
        "path": "_Réception",
        "dynamic": False,
        "option": "core",
        "required": True,
        "role": "reception",
    }
    entry = ReferentielEntry.from_dict(raw)
    assert entry.file_naming is None
    assert entry.organization_type is None
    assert entry.description is None


def test_classify_result_counts():
    events = [
        ClassifyEvent(uri="a", name="a.pdf", status=ClassifyEventStatus.CLASSIFIED, entry_id="x", dest_name="y.pdf", dest_uri="file:///y.pdf"),
        ClassifyEvent(uri="b", name="b.pdf", status=ClassifyEventStatus.UNCLASSIFIED, error_code="unknown"),
        ClassifyEvent(uri="c", name="c.pdf", status=ClassifyEventStatus.FAILED, error_code="error"),
    ]
    result = ClassifyResult(events=events)
    assert result.scanned == 3
    assert result.classified == 1
    assert result.unclassified == 1
    assert result.failed == 1


def test_audit_session_fields():
    from archivist_cli.domain.models import AuditSession

    events = (
        ClassifyEvent(
            uri="file:///archive/_Réception/facture.pdf",
            name="facture.pdf",
            status=ClassifyEventStatus.CLASSIFIED,
            entry_id="factures",
            dest_name="2026-06_facture.pdf",
            dest_uri="file:///archive/Factures/2026-06/2026-06_facture.pdf",
        ),
        ClassifyEvent(
            uri="file:///archive/_Réception/doc.pdf",
            name="doc.pdf",
            status=ClassifyEventStatus.UNCLASSIFIED,
            error_code="llm_uncertain",
            llm_reason="type inconnu",
        ),
    )
    session = AuditSession(
        session_id="abc-123",
        started_at="2026-06-25T10:00:00+00:00",
        ended_at="2026-06-25T10:00:05+00:00",
        referentiel_uri="file:///ref.yaml",
        root_uri="file:///archive",
        events=events,
        scanned=2,
        classified=1,
        unclassified=1,
        failed=0,
    )
    assert session.session_id == "abc-123"
    assert len(session.events) == 2
    assert session.classified == 1
