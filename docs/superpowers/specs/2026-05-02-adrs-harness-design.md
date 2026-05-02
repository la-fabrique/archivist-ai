# ADRs Harness Integration — Design

**Goal:** Rendre les décisions d'architecture visibles et autoritaires pour l'agent codeur, via un système d'ADRs consulté avant toute modification structurante.

**Approach:** Option C — CLAUDE.md comme point d'entrée global + `archivist-cli-dev` comme skill pilote avec étape de consultation explicite.

---

## 1. Structure et format des ADRs

**Répertoire :** `docs/architecture/adrs/`

**Nommage :** `YYYY-MM-DD-ADR-XXX-<slug>.md`
- Date ISO pour tri chronologique
- Numéro séquentiel à 3 chiffres pour référence croisée (`ADR-001`)
- Slug kebab-case pour lisibilité

**Template :**

```markdown
# ADR-XXX: <Title>

**Date:** YYYY-MM-DD
**Status:** accepted | superseded by ADR-YYY

## Context
<Situation et contrainte qui rendent cette décision nécessaire.>

## Options Considered
- **Option A** — <résumé> — Pro: … / Con: …
- **Option B** — <résumé> — Pro: … / Con: …

## Decision
<Ce qui a été décidé, en une phrase. Pourquoi cette option.>

## Consequences
- <Conséquence 1 — positive ou négative>
- <Conséquence 2>
```

**Règles d'écriture LLM-oriented :**
- Bullets et phrases courtes — pas de prose étendue
- `Options Considered` omis si la décision n'avait pas d'alternative réelle
- `Status: superseded by ADR-YYY` quand une décision est remplacée — jamais de suppression

---

## 2. Mise à jour de CLAUDE.md

Ajouter dans la Carte du dépôt :

```
- `docs/architecture/adrs/` — décisions d'architecture (ADRs) — consulter avant toute modification non-triviale
```

Ajouter une section dédiée :

```markdown
## ADRs

Les ADRs consignent les décisions d'architecture qui s'appliquent au dépôt. Avant de modifier une couche structurante (architecture, contrats de sortie, ports, schéma de données), lire les ADRs pertinents dans `docs/architecture/adrs/`.

Un ADR ne se supprime pas — s'il est remplacé, son status passe à `superseded by ADR-YYY`.
```

---

## 3. Mise à jour de archivist-cli-dev

Ajouter une **Étape 0** en tête du workflow :

```markdown
### Étape 0 — Consulter les ADRs pertinents

Avant toute modification, lister les ADRs qui concernent ce package :

​```bash
ls docs/architecture/adrs/
​```

Lire ceux dont le titre ou les conséquences mentionnent `archivist-cli`, les contrats de sortie CLI, ou l'architecture hexagonale. Si un ADR s'applique, respecter sa décision sans la remettre en question — ouvrir une conversation avec le développeur si un ADR semble obsolète.
```

Ajouter à la checklist rapide :

```markdown
- [ ] ADRs pertinents consultés (docs/architecture/adrs/)
```

---

## Out of scope

- Création autonome d'ADRs par l'agent — fera l'objet d'une skill `write-adr` séparée
- Mise à jour des autres skills de dev (`referentiel-cli`, etc.) — pattern validé sur `archivist-cli-dev` d'abord
