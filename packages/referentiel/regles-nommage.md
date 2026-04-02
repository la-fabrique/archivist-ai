# Règles de nommage

> Partie du [Référentiel de gestion documentaire](_index.md) — v0

---

## Principe directeur

Un nom de fichier doit répondre à **3 questions sans ouvrir le document** :

1. **Quand ?** — à quelle période ce document se rapporte-t-il ?
2. **Quoi ?** — quel est le type de document ?
3. **Qui / quoi ?** — quel tiers, quel objet ?

Un bon nom de fichier est lisible par un humain ET triable automatiquement dans l'explorateur de fichiers.

---

## Socle commun

Ces 4 règles s'appliquent à tous les dossiers sans exception.

| Règle | Détail |
|-------|--------|
| **Date en préfixe** | Toujours en début de nom, format `AAAA-MM` ou `AAAA` |
| **Minuscules** | Pas d'accents, pas de majuscules, pas d'espaces |
| **Séparateurs** | Tiret `-` dans un segment, underscore `_` entre les segments |
| **Extension explicite** | `.pdf`, `.xlsx`, `.jpg` — toujours présente |

**Pourquoi ces choix :**

- **Date en préfixe** → l'explorateur trie les fichiers par ordre chronologique automatiquement. Les factures de janvier apparaissent avant celles de mars, sans intervention manuelle.
- **Minuscules sans accents** → portabilité totale entre systèmes (Windows, macOS, Linux, Google Drive, OneDrive, NAS). Un fichier nommé `Réunion Équipe.docx` peut créer des problèmes à l'échange ou à la sauvegarde. `reunion-equipe.docx` ne créera jamais de problème.
- **Underscores entre segments** → la distinction visuelle entre les parties du nom est immédiate. `2026-03_facture_client-dupont_003.pdf` se lit en un coup d'œil.

---

## Règles par dossier

Chaque dossier définit ses propres segments selon la nature de ses documents. Le socle commun s'applique partout ; les segments pertinents varient.

### `Mes Ventes/Factures/`

**Format :** `AAAA-MM_facture_tiers_numero.ext`

**Exemple :** `2026-03_facture_client-dupont_003.pdf`

Le numéro séquentiel (`001`, `002`…) différencie plusieurs factures au même client le même mois. Il correspond idéalement au numéro de facture de ta comptabilité.

---

### `Mes Ventes/Devis/`

**Format :** `AAAA-MM_devis_tiers_numero.ext`

**Exemple :** `2026-03_devis_client-martin_001.pdf`

Même logique que les factures. Si un devis est révisé, utilise le suffixe de version : `2026-03_devis_client-martin_001-v2.pdf`.

---

### `Mes Ventes/Contrats/`

**Format :** `AAAA-MM_contrat_tiers_objet.ext`

**Exemple :** `2026-03_contrat_client-dupont_maintenance.pdf`

L'objet remplace le numéro séquentiel — un contrat se retrouve plus facilement par son objet que par un numéro. Garde l'objet court et explicite (`maintenance`, `formation`, `prestation-conseil`).

---

### `Mes Ventes/Offres/`

**Format :** `nom-offre_version.ext`

**Exemple :** `formation-react_v2.pdf`

Pas de date mensuelle ici : les offres et brochures sont intemporelles. La version (`v1`, `v2`) suffit à les différencier. La date de modification du fichier fait foi si nécessaire.

---

### `Mes Achats/Factures fournisseurs/`

**Format :** `AAAA-MM_facture_fournisseur_numero.ext`

**Exemple :** `2026-03_facture_orange_012.pdf`

Le numéro est celui porté sur la facture du fournisseur (ou un numéro séquentiel si la facture n'en a pas).

---

### `Mes Achats/Assurances/`

**Format :** `AAAA_type_assureur_objet.ext`

**Exemple :** `2026_police_axa_rcpro.pdf` / `2026_attestation_maif_vehicule.pdf`

Date à l'année (les polices couvrent généralement une année entière). Le type distingue la police de l'attestation — documents de nature différente même s'ils concernent le même contrat.

---

### `Mon Social/`

**Format :** `AAAA-MM_type_nom-salarie.ext`

**Exemple :** `2026-03_fiche-paie_dupont-jean.pdf`

Le nom du salarié en dernier : dans ce dossier, tous les documents concernent du personnel. Le type en premier (`fiche-paie`, `contrat-travail`, `dpae`, `avenant`) facilite le tri.

---

### `Ma Fiscalité/`

**Format :** `AAAA-MM_type_impot.ext`

**Exemple :** `2026-01_declaration_tva.pdf` / `2026_avis_cfe.pdf`

Pas de numéro séquentiel : il y a rarement deux déclarations TVA le même mois. La date peut être à l'année (`AAAA`) pour les impôts annuels (CFE, liasse fiscale).

---

### `Ma Banque et Caisse/`

**Format :** `AAAA-MM_releve_banque.ext`

**Exemple :** `2026-03_releve_banque-populaire.pdf`

Si tu as plusieurs comptes, le nom de la banque les différencie. Pour les remises de chèques : `2026-03_remise-cheques_banque-populaire_001.pdf`.

---

### `Mon Juridique/`

**Format :** `AAAA_type_objet.ext`

**Exemple :** `2025_statuts_sas-monentreprise.pdf` / `2024_pv-ag_approbation-comptes.pdf`

Date à l'année — les documents juridiques ne se rapportent généralement pas à un mois précis. L'objet décrit le contenu (`approbation-comptes`, `nomination-gerant`, `modification-statuts`).

---

### `Ma Gestion Administrative/`

**Format :** `AAAA-MM_type_expediteur_objet.ext`

**Exemple :** `2026-03_courrier_urssaf_mise-en-demeure.pdf`

L'expéditeur (ou destinataire pour les courriers sortants) est important ici car les documents sont hétérogènes. Il aide à retrouver rapidement un courrier d'un organisme précis.

---

## Conventions d'écriture

| Convention | Règle | Exemple |
|-----------|-------|---------|
| Casse | Tout en minuscules | `facture` pas `Facture` |
| Mots dans un segment | Séparés par des tirets `-` | `client-dupont`, `mise-en-demeure` |
| Segments entre eux | Séparés par des underscores `_` | `2026-03_facture_client-dupont` |
| Espaces | Jamais | `client-dupont` pas `client dupont` |
| Accents | Jamais | `fiscalite` pas `fiscalité` |
| Abréviations | Seulement si universelles | `tva`, `rh` — éviter le reste |

---

## Cas particuliers

| Cas | Règle | Exemple |
|-----|-------|---------|
| Pas de tiers | Omettre ce segment | `2026-01_declaration_tva.pdf` |
| Pas de date mensuelle | Date à l'année seule | `2025_statuts_sas-monentreprise.pdf` |
| Plusieurs versions | Suffixe `-v2`, `-v3` avant l'extension | `2026-03_devis_client-dupont_001-v2.pdf` |
| Scan ou photo d'un document papier | Préfixer le type avec `scan-` | `2026-03_scan-facture_fournisseur-brico_001.pdf` |
| Deux clients sur un même document | Choisir le client principal, noter l'autre dans les métadonnées ou dans un fichier `.md` associé | `2026-03_contrat_client-dupont_collaboration.pdf` |
