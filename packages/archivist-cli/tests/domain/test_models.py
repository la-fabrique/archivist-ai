from archivist_cli.domain.models import ReferentielEntry


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
