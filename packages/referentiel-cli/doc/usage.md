# Usage — referentiel-cli

## Initialiser l'arborescence

Crée tous les dossiers du référentiel selon les options choisies dans un dossier cible.

```bash
npx referentiel-cli init --options dirigeant-assimile-salarie,assurances --target /chemin/vers/mon/drive
```

### Options disponibles

| Option | Dossier(s) créé(s) | Cas d'usage |
|--------|--------------------|-------------|
| `core` | `Mes ventes/`, `Mes achats/`, `Mon juridique/`, `Ma fiscalité/`, `Ma banque/`, `Archives/` | Tous |
| `dirigeant-assimile-salarie` | `Mon social/` | Dirigeant SASU, assimilé salarié |
| `assurances` | `Mes assurances/` | RC Pro, mutuelle, assurance locaux |

`core` est toujours activé. Les autres options se cumulent.

### Exemple — SASU solo sans salarié

```bash
npx referentiel-cli init --options dirigeant-assimile-salarie,assurances --target ~/Documents/Mon-drive
```

Crée l'arborescence complète décrite dans le [démarrage rapide](../../referentiel/demarrage-rapide.md).
