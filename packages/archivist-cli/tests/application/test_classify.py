from __future__ import annotations

import pytest

from archivist_cli.application.classify import ClassifyConfig, ClassifyUseCase
from archivist_cli.domain.models import (
    ClassifyEventStatus,
    FileNaming,
    FileNamingField,
    ReferentielEntry,
)
from tests.fakes import FakeFilesystem, FakeIndex, FakeLlm, FakeMetadataExtractor, FakeReferentiel

TARGET = "file:///archive"


def _make_entry(
    id: str,
    path: str,
    role: str | None = None,
    file_naming: FileNaming | None = None,
    organization_type: str | None = None,
    organization_subfolder_pattern: str | None = None,
) -> ReferentielEntry:
    return ReferentielEntry(
        id=id,
        folder_name=path.split("/")[-1],
        path=path,
        dynamic=False,
        option="core",
        required=True,
        role=role,
        file_naming=file_naming,
        organization_type=organization_type,
        organization_subfolder_pattern=organization_subfolder_pattern,
    )


def _base_entries() -> list[ReferentielEntry]:
    return [
        _make_entry("reception", "_Réception", role="reception"),
        _make_entry("conservation_brut", "_Conservation brut", role="conservation_brut"),
        _make_entry("non_classe", "_Non classé", role="non_classe"),
    ]


def _make_fs(*extra_files: str) -> FakeFilesystem:
    fs = FakeFilesystem()
    fs.add_dir(f"{TARGET}/_Réception")
    fs.add_dir(f"{TARGET}/_Conservation brut")
    fs.add_dir(f"{TARGET}/_Non classé")
    for f in extra_files:
        fs.add_file(f)
    return fs


def _factures_entry() -> ReferentielEntry:
    return _make_entry(
        "mes_achats.factures_fournisseurs",
        "Mes achats/Mes factures fournisseurs",
        file_naming=FileNaming(
            pattern="[AAAA-MM]_Facture_[Nom fournisseur]_[Numero].[ext]",
            fields=(
                FileNamingField("AAAA-MM", "date d'émission"),
                FileNamingField("Nom fournisseur", "nom du fournisseur"),
                FileNamingField("Numero", "numéro de facture"),
            ),
        ),
        organization_type="chronological",
        organization_subfolder_pattern="AAAA-MM",
    )


def test_classify_nominal():
    """Fichier classifiable — déplacé et renommé selon le pattern du référentiel."""
    entries = _base_entries() + [_factures_entry()]
    fs = _make_fs(f"{TARGET}/_Réception/facture.pdf")
    fs.add_dir(f"{TARGET}/Mes achats/Mes factures fournisseurs")
    llm = FakeLlm(responses=[
        {"entry_id": "mes_achats.factures_fournisseurs", "reason": "facture fournisseur"},
        {"AAAA-MM": "2026-03", "Nom fournisseur": "OVH", "Numero": "F001"},
    ])

    uc = ClassifyUseCase(fs, FakeReferentiel(entries), FakeMetadataExtractor(), llm, FakeIndex())
    result = uc.run(ClassifyConfig(referentiel_uri="", target_uri=TARGET))

    assert len(result.events) == 1
    event = result.events[0]
    assert event.status == ClassifyEventStatus.CLASSIFIED
    assert event.dest_name == "2026-03_Facture_OVH_F001.pdf"
    assert event.dest_uri == f"{TARGET}/Mes achats/Mes factures fournisseurs/2026-03/2026-03_Facture_OVH_F001.pdf"
    assert fs.exists(event.dest_uri)
    assert not fs.exists(f"{TARGET}/_Réception/facture.pdf")


def test_classify_llm_returns_null_goes_to_non_classe():
    """LLM incertain → fichier dans _Non classé, statut unclassified."""
    entries = _base_entries()
    fs = _make_fs(f"{TARGET}/_Réception/unknown.pdf")
    llm = FakeLlm(responses=[{"entry_id": None, "reason": "type de document inconnu"}])

    uc = ClassifyUseCase(fs, FakeReferentiel(entries), FakeMetadataExtractor(), llm, FakeIndex())
    result = uc.run(ClassifyConfig(referentiel_uri="", target_uri=TARGET))

    event = result.events[0]
    assert event.status == ClassifyEventStatus.UNCLASSIFIED
    assert event.error_code == "llm_uncertain"
    assert event.llm_reason == "type de document inconnu"
    assert fs.exists(f"{TARGET}/_Non classé/unknown.pdf")
    assert not fs.exists(f"{TARGET}/_Réception/unknown.pdf")


def test_classify_backup_failure_file_stays_in_reception():
    """Échec du backup → fichier reste dans _Réception, statut failed."""
    from archivist_cli.domain.ports import FilesystemError as FSError

    class FailingZipFs(FakeFilesystem):
        def zip_file(self, src_uri: str, dest_uri: str) -> None:
            raise FSError("disque plein")

    entries = _base_entries()
    fs = FailingZipFs()
    fs.add_dir(f"{TARGET}/_Réception")
    fs.add_dir(f"{TARGET}/_Conservation brut")
    fs.add_dir(f"{TARGET}/_Non classé")
    fs.add_file(f"{TARGET}/_Réception/facture.pdf")

    uc = ClassifyUseCase(fs, FakeReferentiel(entries), FakeMetadataExtractor(), FakeLlm(), FakeIndex())
    result = uc.run(ClassifyConfig(referentiel_uri="", target_uri=TARGET))

    event = result.events[0]
    assert event.status == ClassifyEventStatus.FAILED
    assert event.error_code == "backup_error"
    assert fs.exists(f"{TARGET}/_Réception/facture.pdf")


def test_classify_metadata_error_goes_to_non_classe():
    """Échec extraction métadonnées → fichier dans _Non classé."""
    entries = _base_entries()
    fs = _make_fs(f"{TARGET}/_Réception/broken.pdf")
    extractor = FakeMetadataExtractor(fail_on={f"{TARGET}/_Réception/broken.pdf"})

    uc = ClassifyUseCase(fs, FakeReferentiel(entries), extractor, FakeLlm(), FakeIndex())
    result = uc.run(ClassifyConfig(referentiel_uri="", target_uri=TARGET))

    event = result.events[0]
    assert event.status == ClassifyEventStatus.FAILED
    assert event.error_code == "metadata_error"
    assert fs.exists(f"{TARGET}/_Non classé/broken.pdf")
    assert not fs.exists(f"{TARGET}/_Réception/broken.pdf")


def test_classify_llm_error_on_classify_goes_to_non_classe():
    """Erreur LLM (appel 1) → fichier dans _Non classé."""
    entries = _base_entries() + [_factures_entry()]
    fs = _make_fs(f"{TARGET}/_Réception/facture.pdf")
    llm = FakeLlm(fail_on_calls={0})

    uc = ClassifyUseCase(fs, FakeReferentiel(entries), FakeMetadataExtractor(), llm, FakeIndex())
    result = uc.run(ClassifyConfig(referentiel_uri="", target_uri=TARGET))

    event = result.events[0]
    assert event.status == ClassifyEventStatus.FAILED
    assert event.error_code == "llm_error"
    assert fs.exists(f"{TARGET}/_Non classé/facture.pdf")


def test_classify_llm_error_on_extract_fields_goes_to_non_classe():
    """Erreur LLM (appel 2 — extraction champs) → fichier dans _Non classé."""
    entries = _base_entries() + [_factures_entry()]
    fs = _make_fs(f"{TARGET}/_Réception/facture.pdf")
    llm = FakeLlm(
        responses=[{"entry_id": "mes_achats.factures_fournisseurs", "reason": "ok"}],
        fail_on_calls={1},
    )

    uc = ClassifyUseCase(fs, FakeReferentiel(entries), FakeMetadataExtractor(), llm, FakeIndex())
    result = uc.run(ClassifyConfig(referentiel_uri="", target_uri=TARGET))

    event = result.events[0]
    assert event.status == ClassifyEventStatus.FAILED
    assert event.error_code == "llm_error"
    assert fs.exists(f"{TARGET}/_Non classé/facture.pdf")


def test_classify_error_does_not_stop_other_files():
    """Erreur sur un fichier → les autres continuent d'être traités."""
    entries = _base_entries() + [_factures_entry()]
    fs = _make_fs(
        f"{TARGET}/_Réception/broken.pdf",
        f"{TARGET}/_Réception/facture.pdf",
    )
    fs.add_dir(f"{TARGET}/Mes achats/Mes factures fournisseurs")
    extractor = FakeMetadataExtractor(fail_on={f"{TARGET}/_Réception/broken.pdf"})
    llm = FakeLlm(responses=[
        {"entry_id": "mes_achats.factures_fournisseurs", "reason": "facture"},
        {"AAAA-MM": "2026-03", "Nom fournisseur": "OVH", "Numero": "F001"},
    ])

    uc = ClassifyUseCase(fs, FakeReferentiel(entries), extractor, llm, FakeIndex())
    result = uc.run(ClassifyConfig(referentiel_uri="", target_uri=TARGET))

    assert result.scanned == 2
    assert result.failed == 1
    assert result.classified == 1


def test_classify_empty_reception():
    """_Réception vide → aucun événement."""
    fs = _make_fs()
    uc = ClassifyUseCase(
        fs, FakeReferentiel(_base_entries()), FakeMetadataExtractor(), FakeLlm(), FakeIndex()
    )
    result = uc.run(ClassifyConfig(referentiel_uri="", target_uri=TARGET))
    assert result.scanned == 0


def test_classify_result_summary():
    """Les propriétés de ClassifyResult comptent correctement."""
    entries = _base_entries() + [_factures_entry()]
    fs = _make_fs(
        f"{TARGET}/_Réception/ok.pdf",
        f"{TARGET}/_Réception/unknown.pdf",
        f"{TARGET}/_Réception/broken.pdf",
    )
    fs.add_dir(f"{TARGET}/Mes achats/Mes factures fournisseurs")
    extractor = FakeMetadataExtractor(fail_on={f"{TARGET}/_Réception/broken.pdf"})
    llm = FakeLlm(responses=[
        {"entry_id": "mes_achats.factures_fournisseurs", "reason": "facture"},
        {"AAAA-MM": "2026-03", "Nom fournisseur": "OVH", "Numero": "F001"},
        {"entry_id": None, "reason": "inconnu"},
    ])

    uc = ClassifyUseCase(fs, FakeReferentiel(entries), extractor, llm, FakeIndex())
    result = uc.run(ClassifyConfig(referentiel_uri="", target_uri=TARGET))

    assert result.scanned == 3
    assert result.classified == 1
    assert result.unclassified == 1
    assert result.failed == 1
