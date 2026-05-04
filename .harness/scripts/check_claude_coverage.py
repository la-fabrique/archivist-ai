#!/usr/bin/env python3
"""Ensure every packages/* directory is documented in CLAUDE.md.

Usage (from repo root): python scripts/check_claude_coverage.py
Exit 0 = all packages covered, exit 1 = gaps (with actionable messages).
"""
import sys
from pathlib import Path


def main() -> None:
    packages_dir = Path("packages")
    claude_md = Path("CLAUDE.md")

    if not packages_dir.exists():
        print(f"ERREUR : {packages_dir} introuvable")
        sys.exit(1)
    if not claude_md.exists():
        print(f"ERREUR : {claude_md} introuvable")
        sys.exit(1)

    content = claude_md.read_text(encoding="utf-8")
    packages = sorted(p.name for p in packages_dir.iterdir() if p.is_dir())

    errors = []
    for pkg in packages:
        if pkg not in content:
            errors.append(
                f"Le package '{pkg}' n'est pas documenté dans CLAUDE.md — "
                f"ajouter une entrée `packages/{pkg}/` dans la section 'Carte du dépôt'"
            )

    if errors:
        print("Couverture CLAUDE.md incomplète :")
        for e in errors:
            print(f"  • {e}")
        sys.exit(1)

    print(f"CLAUDE.md couvre tous les packages ({len(packages)} vérifiés : {', '.join(packages)}).")


if __name__ == "__main__":
    main()
