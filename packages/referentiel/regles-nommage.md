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

## Règles par dossier

Chaque dossier définit ses propres segments selon la nature de ses documents. Le socle commun s'applique partout ; les segments pertinents varient.

### `Mes ventes/Mes factures clients/`

**Format :** `[AAAA-MM]_Facture_[Nom client]_[Numero].[ext]`

- `[AAAA-MM]` — date d'émission
- `[Nom client]` — nom du client, forme lisible
- `[Numero]` — numéro de la facture tel qu'il apparaît dans le logiciel de facturation
- `[ext]` — extension du fichier

**Exemple :** `2026-03_Facture_Dupont_F2600003.pdf`

---

### `Mes ventes/Mes modèles/Contrats/`

**Rôle :** gabarits de contrat à dupliquer et adapter — pas les contrats signés clients (voir `Mes ventes/Mes clients/[client]/Contrats/`).

**Format :** `modele-contrat_[objet]_v[N].[ext]`

**Exemple :** `modele-contrat_maintenance-annuelle_v2.docx`

Pas de préfixe date client : ce sont des documents réutilisables. La version (`v1`, `v2`) sert à distinguer les révisions du modèle.

---

### `Mes ventes/Mes modèles/Devis et offres/`

**Rôle :** gabarits de devis et d'offres commerciales à dupliquer et adapter.

**Format :** `modele-devis_[objet]_v[N].[ext]`

**Exemple :** `modele-devis_prestation-conseil_v1.docx`

Pas de préfixe date : ce sont des gabarits réutilisables. La version (`v1`, `v2`) distingue les révisions.

---

### `Mes ventes/Mes clients/[Nom du client]/Contrats/`

**Format :** `[AAAA-MM]_Contrat_[Nom client]_[Numéro-Révision].[ext]` ou `[AAAA-MM]_Avenant_[Nom client]_[Numéro-Révision].[ext]`

- `[AAAA-MM]` — date d'émission
- `[Nom client]` — nom du client, forme lisible
- `[Numéro-Révision]` — référence libre (numéro de contrat, objet, version… selon ta convention)
- `[ext]` — extension du fichier

**Exemples :** `2026-04_Contrat_Acme_C2026-01.pdf` / `2026-04_Avenant_Acme_C2026-02.pdf`

---

### `Mes ventes/Mes clients/[Nom du client]/Devis/`

**Format :** `[AAAA-MM]_Devis_[Nom client]_[Numero].[ext]`

- `[AAAA-MM]` — date d'émission
- `[Nom client]` — nom du client, forme lisible
- `[Numero]` — numéro du devis tel qu'il apparaît dans le logiciel
- `[ext]` — extension du fichier

**Exemple :** `2026-03_Devis_Martin_D2600001.pdf`

---

### `Mes achats/Mes factures fournisseurs/`

**Format :** `[AAAA-MM]_Facture_[Nom fournisseur]_[Numero].[ext]`

- `[AAAA-MM]` — date d'émission de la facture
- `[Nom fournisseur]` — nom du fournisseur, forme lisible
- `[Numero]` — numéro de la facture tel qu'il apparaît sur le document
- `[ext]` — extension du fichier

**Exemple :** `2026-03_Facture_OVH_F2600042.pdf`

---

### `Mon social/`

**Format :** `[AAAA-MM]_[Type]_[Nom-salarie].[ext]`

**Exemple :** `2026-03_Fiche-de-paie_Dupont.pdf`

Le nom du salarié en dernier : dans ce dossier, tous les documents concernent du personnel. Le type en premier (`Fiche-de-paie`, `Contrat-travail`, `DPAE`, `Avenant`) facilite le tri.

---

### `Ma fiscalité/`

**Format :** `[AAAA-MM]_[Type].[ext]`

**Exemple :** `2026-01_Declaration-TVA.pdf` / `2026_Avis-CFE.pdf`

Pas de numéro séquentiel : il y a rarement deux déclarations TVA le même mois. La date peut être à l'année (`AAAA`) pour les impôts annuels (CFE, liasse fiscale).

---

### `Ma banque/`

**Format :** `[AAAA-MM]_Releve_[Nom-banque]_[Numero].[ext]`

**Exemple :** `2026-03_Releve_Banque-Populaire_003.pdf`

Le sous-dossier `[Nom banque]/` permet de distinguer plusieurs établissements. Le numéro de relevé (tel qu'il apparaît sur le document) permet de trier les relevés d'un même compte.

---

### `Mon juridique/`

**Format :** `[AAAA]_[Type]_[Objet].[ext]`

**Exemple :** `2025_Statuts_SAS-Monentreprise.pdf` / `2024_PV-AG_approbation-comptes.pdf`

Date à l'année — les documents juridiques ne se rapportent généralement pas à un mois précis. L'objet décrit le contenu (`approbation-comptes`, `nomination-gerant`, `modification-statuts`).

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


