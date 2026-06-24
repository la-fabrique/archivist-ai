import textwrap
from pathlib import Path

import pytest

from archivist_cli.adapters.referentiel.yaml_file import YamlFileReferentiel
from archivist_cli.domain.ports import ReferentielError


def test_load_entries_from_yaml(tmp_path: Path):
    yaml_content = textwrap.dedent("""\
        - id: ma_banque
          folder_name: Ma banque
          path: Ma banque
          dynamic: false
          option: core
          required: true
        - id: ma_banque.rib
          folder_name: Mes RIB
          path: Ma banque/Mes RIB
          parent: ma_banque
          dynamic: false
          option: core
          required: true
    """)
    yaml_path = tmp_path / "referentiel.yaml"
    yaml_path.write_text(yaml_content, encoding="utf-8")

    ref = YamlFileReferentiel(uri=yaml_path.as_uri())
    entries = ref.load_entries()

    assert len(entries) == 2
    assert entries[0].id == "ma_banque"
    assert entries[1].parent == "ma_banque"


def test_load_entries_file_not_found():
    ref = YamlFileReferentiel(uri="file:///nonexistent/referentiel.yaml")
    with pytest.raises(ReferentielError, match="not found"):
        ref.load_entries()


def test_load_entries_invalid_yaml(tmp_path: Path):
    yaml_path = tmp_path / "bad.yaml"
    yaml_path.write_text("{{invalid", encoding="utf-8")

    ref = YamlFileReferentiel(uri=yaml_path.as_uri())
    with pytest.raises(ReferentielError, match="parse"):
        ref.load_entries()


def test_load_entries_with_role(tmp_path: Path):
    yaml_content = textwrap.dedent("""\
        - id: reception
          folder_name: _Réception
          path: _Réception
          dynamic: false
          option: core
          required: true
          role: reception
        - id: ma_banque
          folder_name: Ma banque
          path: Ma banque
          dynamic: false
          option: core
          required: true
    """)
    yaml_path = tmp_path / "referentiel.yaml"
    yaml_path.write_text(yaml_content, encoding="utf-8")

    ref = YamlFileReferentiel(uri=yaml_path.as_uri())
    entries = ref.load_entries()

    by_id = {e.id: e for e in entries}
    assert by_id["reception"].role == "reception"
    assert by_id["ma_banque"].role is None
