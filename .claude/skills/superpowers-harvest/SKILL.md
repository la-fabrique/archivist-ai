---
name: superpowers-harvest
description: Use when a superpowers plan has been fully implemented and the session is ending. Triggers a subagent that extracts features and ADRs from docs/superpowers/ then deletes those files.
---

# superpowers-harvest

## Vue d'ensemble

À la fin d'une session de développement piloté par un plan superpowers, ce skill dispatche un subagent qui :

1. Lit les fichiers dans `docs/superpowers/plans/` et `docs/superpowers/specs/`
2. En extrait les features fonctionnelles et/ou les décisions d'architecture
3. Les écrit dans les bons répertoires (`docs/features/`, `docs/architecture/adrs/`)
4. Supprime les fichiers superpowers (en conservant les `.gitkeep`)

## Quand utiliser

- Le plan (checklist) est entièrement coché
- La session de dev superpowers est terminée
- Des fichiers existent dans `docs/superpowers/plans/` ou `docs/superpowers/specs/`

## Processus

### 1. Vérifier qu'il y a quelque chose à récolter

```bash
find docs/superpowers -type f ! -name ".gitkeep"
```

Si la commande ne retourne rien → rien à faire, skill terminé.

### 2. Dispatcher le subagent de récolte

Dispatcher un subagent **SUBAGENT-STOP exempt** avec ce prompt (adapter les chemins de fichiers réels) :

```
Tu es un subagent de récolte documentaire pour le projet archivist-ai.

## Contexte

Un plan superpowers vient d'être implémenté. Tu dois extraire la documentation
produite et la placer dans les bons répertoires du projet, puis supprimer les
fichiers temporaires.

## Fichiers à traiter

Lis tous les fichiers dans :
- docs/superpowers/plans/    (plans d'implémentation)
- docs/superpowers/specs/    (specs de design, décisions d'architecture)

Ignore les fichiers `.gitkeep`.

## Règles d'extraction

### Features fonctionnelles → docs/features/

Un fichier contient une feature si :
- Il décrit un comportement observable par un utilisateur final
- Il mentionne des cas d'usage, des scénarios d'interaction
- Il décrit ce que le système "doit faire" du point de vue utilisateur

Si trouvé : utilise le skill `write-feature` pour créer le fichier `.feature`
correspondant dans `docs/features/`. Le skill décrit le format Gherkin attendu.

### Décisions d'architecture → docs/architecture/adrs/

Un fichier contient une décision d'architecture si :
- Il choisit entre plusieurs approches techniques
- Il explique pourquoi une technologie/pattern a été retenu
- Il décrit des contraintes structurantes sur le code

Si trouvé : utilise le skill `write-adr` pour créer l'ADR correspondant dans
`docs/architecture/adrs/`. Le skill décrit le format et le numérotage.

### Ni l'un ni l'autre

Un plan d'implémentation pur (liste de tâches, étapes de code) sans décision
d'architecture ni feature utilisateur ne produit rien. Le supprimer directement.

## Après extraction

Supprime tous les fichiers traités dans `docs/superpowers/plans/` et
`docs/superpowers/specs/`, **sauf** les `.gitkeep`.

```bash
find docs/superpowers -type f ! -name ".gitkeep" -delete
```

## Rapport final

Résume ce qui a été créé :
- Features écrites : liste des fichiers créés dans docs/features/
- ADRs écrits : liste des fichiers créés dans docs/architecture/adrs/
- Fichiers supprimés : liste des fichiers superpowers supprimés
```

### 3. Valider le rapport du subagent

Vérifier que les fichiers annoncés existent bien :

```bash
# Features créées
ls docs/features/

# ADRs créés
ls docs/architecture/adrs/

# Superpowers nettoyés (seuls .gitkeep doivent rester)
find docs/superpowers -type f
```

## Erreurs fréquentes

| Situation | Action |
|-----------|--------|
| Le spec est un doc de design pur sans décision → pas d'ADR évident | Ne pas forcer un ADR ; signaler à l'utilisateur |
| Le plan contient des features ET des décisions | Créer les deux documents séparément |
| Un ADR couvre déjà le sujet | Ajouter `superseded by` à l'ancien, ne pas dupliquer |
| Le subagent oublie de supprimer les fichiers | Relancer `find docs/superpowers -type f ! -name ".gitkeep" -delete` manuellement |
