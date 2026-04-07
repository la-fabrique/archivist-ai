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

### `Mes ventes/mes_modeles_de_devis/`

**Rôle :** gabarits de devis à dupliquer et adapter — pas les devis envoyés aux clients (voir `Mes ventes/mes_clients/[client]/devis/`).

**Format :** `modele-devis_objet_vN.ext`

**Exemple :** `modele-devis_prestation_conseil_v1.docx`

Même logique que les modèles de contrat : pas de date client, version du gabarit uniquement.

---

### `Mes ventes/mes_modeles_de_contrat/`

**Rôle :** gabarits à dupliquer et adapter — pas les contrats signés clients (voir `Mes ventes/mes_clients/[client]/contrats/`).

**Format :** `modele-contrat_{objet}_v{version}.ext`

**Exemple :** `modele-contrat_maintenance_annuelle_v2.docx`

Pas de préfixe date client : ce sont des documents réutilisables. La version (`v1`, `v2`) sert à distinguer les révisions du modèle.

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

### `Mes ventes/mes_modeles_d_offre/`

**Rôle :** gabarits d'offre à dupliquer et adapter — pas les offres envoyées aux clients (voir `Mes ventes/mes_clients/[client]/offres/`).

**Format :** `modele-offre_objet_vN.ext`

**Exemple :** `modele-offre_formation-react_v2.docx`

Même logique que les modèles de contrat et de devis : pas de date client, version du gabarit uniquement.

---

### `Mes ventes/Mes clients/[Nom du client]/Offres/`

**Format :** `[AAAA-MM]_Offre_[Nom client]_[Numero].[ext]`

- `[AAAA-MM]` — date d'émission
- `[Nom client]` — nom du client, forme lisible
- `[Numero]` — numéro de l'offre tel qu'il apparaît dans le logiciel
- `[ext]` — extension du fichier

**Exemple :** `2026-03_Offre_Dupont_O2600001.pdf`

---

### `Mes achats/factures_fournisseurs/`

**Format :** `AAAA-MM_facture_fournisseur_numero.ext`

**Exemple :** `2026-03_facture_orange_012.pdf`

Le numéro est celui porté sur la facture du fournisseur (ou un numéro séquentiel si la facture n'en a pas).

---

### `Mes achats/assurances/`

**Format :** `AAAA_type_assureur_objet.ext`

**Exemple :** `2026_police_axa_rcpro.pdf` / `2026_attestation_maif_vehicule.pdf`

Date à l'année (les polices couvrent généralement une année entière). Le type distingue la police de l'attestation — documents de nature différente même s'ils concernent le même contrat.

---

### `Mon social/`

**Format :** `AAAA-MM_type_nom-salarie.ext`

**Exemple :** `2026-03_fiche-paie_dupont-jean.pdf`

Le nom du salarié en dernier : dans ce dossier, tous les documents concernent du personnel. Le type en premier (`fiche-paie`, `contrat-travail`, `dpae`, `avenant`) facilite le tri.

---

### `Ma fiscalité/`

**Format :** `AAAA-MM_type_impot.ext`

**Exemple :** `2026-01_declaration_tva.pdf` / `2026_avis_cfe.pdf`

Pas de numéro séquentiel : il y a rarement deux déclarations TVA le même mois. La date peut être à l'année (`AAAA`) pour les impôts annuels (CFE, liasse fiscale).

---

### `Ma banque et caisse/`

**Format :** `AAAA-MM_releve_banque.ext`

**Exemple :** `2026-03_releve_banque-populaire.pdf`

Si tu as plusieurs comptes, le nom de la banque les différencie. Pour les remises de chèques : `2026-03_remise-cheques_banque-populaire_001.pdf` (nom de fichier inchangé ; le dossier parent éventuel suit la convention dossiers, ex. `Remises chèques/`).

---

### `Mon juridique/`

**Format :** `AAAA_type_objet.ext`

**Exemple :** `2025_statuts_sas-monentreprise.pdf` / `2024_pv-ag_approbation-comptes.pdf`

Date à l'année — les documents juridiques ne se rapportent généralement pas à un mois précis. L'objet décrit le contenu (`approbation-comptes`, `nomination-gerant`, `modification-statuts`).

---

### `Ma gestion administrative/`

**Format :** `AAAA-MM_type_expediteur_objet.ext`

**Exemple :** `2026-03_courrier_urssaf_mise-en-demeure.pdf`

L'expéditeur (ou destinataire pour les courriers sortants) est important ici car les documents sont hétérogènes. Il aide à retrouver rapidement un courrier d'un organisme précis.

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
| Pas de tiers                       | Omettre ce segment                                                                               | `2026-01_declaration_tva.pdf`                     |
| Pas de date mensuelle              | Date à l'année seule                                                                             | `2025_statuts_sas-monentreprise.pdf`              |
| Plusieurs versions                 | Suffixe `-v2`, `-v3` avant l'extension                                                           | `2026-03_Devis_Dupont_D2600001-v2.pdf`            |
| Scan ou photo d'un document papier | Préfixer le type avec `scan-`                                                                    | `2026-03_scan-facture_fournisseur-brico_001.pdf`  |
| Deux clients sur un même document  | Choisir le client principal, noter l'autre dans les métadonnées ou dans un fichier `.md` associé | `2026-03_Contrat_Dupont_collaboration.pdf`        |


