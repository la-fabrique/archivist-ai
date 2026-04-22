# Règles de nommage

> Partie du [Référentiel de gestion documentaire](./_index.md) — v0

---

## Principe directeur

Un nom de fichier doit répondre à **3 questions sans ouvrir le document** :

1. **Quand ?** — à quelle période ce document se rapporte-t-il ?
2. **Quoi ?** — quel est le type de document ?
3. **Qui / quoi ?** — quel tiers, quel objet ?

Un bon nom de fichier est lisible par un humain ET triable automatiquement dans l'explorateur de fichiers.

---

## Dossiers de l’arborescence

Les **noms de dossiers** (toute l’arborescence de classement) suivent une convention en **français lisible** :


| Règle                  | Détail                                                                                                                    |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **Majuscule initiale** | Première lettre en majuscule, le reste en minuscules                                                                      |
| **Espaces**            | Les mots sont séparés par des espaces                                                                                     |
| **Accents**            | On conserve les accents français (`Ma fiscalité`, pas `Ma fiscalite`)                                                     |
| **Pas de tiret**       | Sauf pour les dossiers **uniquement chronologiques** au format `AAAA-MM` ou `AAAA` (lisibilité et tri dans l’explorateur) |


**Exemples de dossiers :** `Mes ventes/`, `Mes factures clients/`, `Mes modèles de contrat/`, `Factures fournisseurs/`, `Dupont/`, `Archives/`, `2026-03/`.

**Fichiers vs dossiers :** les règles du socle commun ci‑dessous concernent les **fichiers** (nom avec date, type, tiers…). Les dossiers ne reprennent pas ce format — uniquement la convention décrite ici.

---

## Socle commun (fichiers)

Ces 4 règles s’appliquent aux **fichiers** de tous les dossiers, sans exception.


| Règle                   | Détail                                                       |
| ----------------------- | ------------------------------------------------------------ |
| **Date en préfixe**     | Toujours en début de nom, format `AAAA-MM` ou `AAAA`         |
| **Casse**               | Majuscule initiale sur chaque segment, pas d'accents, pas d'espaces |
| **Séparateurs**         | Tiret `-` dans un segment, underscore `_` entre les segments |
| **Extension explicite** | `.pdf`, `.xlsx`, `.jpg` — toujours présente                  |


**Pourquoi ces choix :**

- **Date en préfixe** → l'explorateur trie les fichiers par ordre chronologique automatiquement. Les factures de janvier apparaissent avant celles de mars, sans intervention manuelle.
- **Majuscule initiale par segment, sans accents** → lisibilité immédiate du nom de fichier, tout en garantissant la portabilité entre systèmes (Windows, macOS, Linux, Google Drive, OneDrive, NAS). Pas d'accents pour éviter les problèmes d'encodage à l'échange ou à la sauvegarde.
- **Underscores entre segments** → la distinction visuelle entre les parties du nom est immédiate. `2026-03_Facture_Dupont_F2600003.pdf` se lit en un coup d'œil.

---

## Conventions d'écriture


| Convention                      | Règle                                                                                        | Exemple                             |
| ------------------------------- | -------------------------------------------------------------------------------------------- | ----------------------------------- |
| **Dossiers**                    | Français lisible, voir section [Dossiers de l'arborescence](#dossiers-de-larborescence) | `Mes ventes/Mes factures clients/2026-03/` |
| Casse (fichiers)                | Majuscule initiale sur chaque segment                                                        | `Facture`, `Dupont`, `Declaration`  |
| Mots dans un segment (fichiers) | Séparés par des tirets `-`                                                                   | `mise-en-demeure`, `fiche-paie`     |
| Segments entre eux (fichiers)   | Séparés par des underscores `_`                                                              | `2026-03_Facture_Dupont`            |
| Espaces                         | Jamais                                                                                       | `client-dupont` pas `client dupont` |
| Accents                         | Jamais                                                                                       | `fiscalite` pas `fiscalité`         |
| Abréviations                    | Seulement si universelles                                                                    | `tva`, `rh` — éviter le reste       |


---

## Cas particuliers


| Cas                                | Règle                                                                                            | Exemple                                           |
| ---------------------------------- | ------------------------------------------------------------------------------------------------ | ------------------------------------------------- |
| Pas de tiers                       | Omettre ce segment                                                                               | `2026-01_Declaration-TVA.pdf`                     |
| Pas de date mensuelle              | Date à l'année seule                                                                             | `2025_Statuts_SAS-Monentreprise.pdf`              |
| Plusieurs versions                 | Suffixe `-v2`, `-v3` avant l'extension                                                           | `2026-03_Devis_Dupont_D2600001-v2.pdf`            |
| Scan ou photo d'un document papier | Préfixer le type avec `scan-`                                                                    | `2026-03_scan-facture_fournisseur-brico_001.pdf`  |
| Deux clients sur un même document  | Choisir le client principal, noter l'autre dans les métadonnées ou dans un fichier `.md` associé | `2026-03_Contrat_Dupont_collaboration.pdf`        |


