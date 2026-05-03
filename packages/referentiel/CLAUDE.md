# referentiel

Contenu documentaire du référentiel de gestion. **Pas de code** — uniquement Markdown et YAML.

## Artefacts générés

- `referentiel.yaml` — export plat de toutes les fiches (généré par `referentiel-cli export-frontmatters`)
- `referentiel.pdf` — version imprimable (généré par `referentiel-cli generate-pdf`)

Ne pas éditer ces fichiers à la main.

## Structure

```
_index.md                    page d'accueil du référentiel
demarrage-rapide.md          guide de démarrage
regles-nommage.md            conventions de nommage des fichiers
regles-archivage.md          règles de durée de conservation
classement/                  fiches de classement (une par dossier/sous-dossier)
assets/                      ressources statiques
```

## Conventions des fiches

Chaque fiche dans `classement/` est un fichier Markdown avec frontmatter YAML obligatoire :

```yaml
---
id: section.sous_section           # identifiant unique, snake_case, hiérarchie par points
folder_name: "Nom affiché"         # nom du dossier tel qu'affiché à l'utilisateur
path: "Section/Sous-section"       # chemin complet dans l'arborescence cible
parent: section                    # id du parent (absent pour les racines)
dynamic: false                     # true si le dossier dépend d'une donnée variable (nom client…)
option: core                       # option de déploiement (core, dirigeant-assimile-salarie, assurances…)
required: true                     # true si le dossier est toujours créé pour l'option
description: "..."                 # description courte
---
```

### Nommage des fichiers

- Format : `section__sous_section.md` — double underscore comme séparateur de hiérarchie
- Le nom de fichier correspond à l'`id` avec `__` au lieu de `.`
- Racines : `section.md`, sous-dossiers : `section__enfant.md`
