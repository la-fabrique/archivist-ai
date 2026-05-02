---
name: write-adr
description: Use when writing a new Architecture Decision Record (ADR) for the archivist-ai project — naming, numbering, format, location, and LLM-oriented writing rules
---

# Write ADR

## Localisation et nommage

**Répertoire :** `docs/architecture/adrs/`

**Prochain numéro :**
```bash
ls docs/architecture/adrs/*.md 2>/dev/null | grep -oP 'ADR-\d+' | sort | tail -1
```
Si vide → ADR-001. Sinon incrémenter.

**Nom de fichier :** `YYYY-MM-DD-ADR-XXX-<slug>.md`
- Date du jour ISO
- Numéro à 3 chiffres (ADR-001, ADR-002…)
- Slug kebab-case, sans accents

## Template

```markdown
# ADR-XXX: <Titre en français>

**Date:** YYYY-MM-DD
**Status:** accepted

## Context
<1-3 phrases. Situation et contrainte qui rendent cette décision nécessaire.>

## Decision
<1-2 phrases max. Ce qui a été décidé et pourquoi — pas de paragraphe.>

## Consequences
- <Contrainte concrète et vérifiable — 1 ligne>
- <...>
```

**`Options Considered`** — section facultative, à insérer entre Context et Decision **uniquement si** plusieurs alternatives réelles ont été comparées. Ne pas inventer des options pour remplir la section.

## Règles d'écriture (LLM-oriented)

- **Langue : français** — titre, corps, tout. Aucune exception.
- Decision : 1-2 phrases max, pas de paragraphe explicatif
- Consequences : bullets courts, chaque bullet = 1 contrainte vérifiable
- Context : 1-3 phrases, pas de prose
- Pas de redite du Context dans la Decision

## Red Flags — STOP

| Pensée | Réalité |
|--------|---------|
| "Je vais écrire en anglais c'est plus clair" | Non. Tout le projet est en français. Le titre aussi. |
| "La Decision mérite une explication détaillée" | 1-2 phrases max. Le Context fournit déjà le pourquoi. |
| "Je vais supprimer l'ancien ADR" | Jamais. Mettre `superseded by ADR-YYY`. |
| "Je devrais documenter les options pour être complet" | Ne pas inventer des options. Pas d'options réelles = section absente. |

## Checklist

- [ ] Numéro déterminé avec `ls docs/architecture/adrs/`
- [ ] Fichier dans `docs/architecture/adrs/`
- [ ] Contenu en français
- [ ] Consequences : 2-4 bullets
- [ ] Commit : `docs(adrs): add ADR-XXX <titre court>`
