#!/usr/bin/env python3
"""Validate referentiel.yaml against the expected schema.

Usage (from repo root): python scripts/check_referentiel_yaml.py
Exit 0 = valid, exit 1 = errors (with actionable messages).
"""
import sys
import yaml
from pathlib import Path

REQUIRED_FIELDS = {
    "id", "folder_name", "path", "dynamic",
    "option", "required", "description", "organization",
}


def validate(path: Path) -> list[str]:
    errors = []
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        return [f"referentiel.yaml invalide : erreur YAML — {e}"]

    if not isinstance(data, list):
        return ["referentiel.yaml doit être une liste d'entrées à la racine"]

    for i, entry in enumerate(data):
        if not isinstance(entry, dict):
            errors.append(f"Entrée {i} : doit être un objet, pas {type(entry).__name__}")
            continue
        missing = REQUIRED_FIELDS - entry.keys()
        if missing:
            entry_id = entry.get("id", f"#{i}")
            for field in sorted(missing):
                errors.append(
                    f"Entrée '{entry_id}' : le champ '{field}' est requis — "
                    f"ajouter `{field}: <valeur>` à cette entrée"
                )

    return errors


def main() -> None:
    path = Path("packages/referentiel/referentiel.yaml")
    if not path.exists():
        print(f"ERREUR : {path} introuvable — vérifier le chemin depuis la racine du dépôt")
        sys.exit(1)

    errors = validate(path)
    if errors:
        print("referentiel.yaml invalide :")
        for e in errors:
            print(f"  • {e}")
        sys.exit(1)

    print(f"referentiel.yaml valide ({path}).")


if __name__ == "__main__":
    main()
