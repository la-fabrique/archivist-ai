---
name: write-feature
description: Use when writing a new functional feature specification for the archivist-ai project. Triggered by /write-feature or when asked to write, describe, or specify a user-facing behavior. Output is a Gherkin .feature file in French placed in docs/features/.
---

# write-feature

## Vue d'ensemble

Rédige une feature Gherkin en français décrivant le comportement attendu d'une fonctionnalité. Le fichier produit est placé dans `docs/features/` avec l'extension `.feature`.

## Quand utiliser

- `/write-feature` ou "rédige la feature pour X"
- Avant d'implémenter une nouvelle fonctionnalité utilisateur
- Pour documenter un comportement existant non encore spécifié

## Processus

### 1. Clarifier si besoin

Si la demande est vague (périmètre flou, acteurs inconnus, critères d'acceptation absents), poser **une seule question groupée** avant de rédiger :

```
Avant de rédiger, quelques précisions :
- Qui est l'acteur principal ? (utilisateur, système, administrateur…)
- Quel est le résultat attendu en cas de succès ?
- Y a-t-il des cas d'erreur à couvrir ?
```

### 2. Nommer le fichier

Kebab-case français, court, décrit la fonctionnalité :

```
docs/features/recherche-documents.feature
docs/features/export-referentiel.feature
docs/features/authentification-utilisateur.feature
```

### 3. Structure du fichier

```gherkin
Feature: <titre court, verbe à l'infinitif>

<paragraphe de contexte : pourquoi cette feature existe, quelle valeur elle apporte>

Scenario: <cas nominal>
  Given <précondition>
  When <action>
  Then <résultat attendu>
  And <résultat complémentaire si nécessaire>

Scenario: <cas alternatif ou d'erreur>
  Given <précondition>
  When <action>
  Then <résultat attendu>
```

### Éléments optionnels

| Élément | Quand l'utiliser |
|---------|-----------------|
| `Background:` | Préconditions communes à tous les scenarios |
| `Scenario Outline:` + `Examples:` | Même comportement avec plusieurs jeux de données |
| Tags (`@smoke`, `@wip`) | Pour filtrage dans la CI ou suivi en cours |

## Règles de rédaction

- **Tout en français** — mots-clés Gherkin inclus (`Fonctionnalité`, `Scénario`, `Étant donné`, `Quand`, `Alors`, `Et`) **OU** mots-clés anglais (`Feature`, `Scenario`, `Given`, `When`, `Then`, `And`) — choisir un style et s'y tenir dans le fichier
- Le paragraphe de contexte explique le **pourquoi**, pas le comment
- Les steps décrivent le comportement observable, pas l'implémentation
- Un scenario = un cas, pas plusieurs comportements mélangés
- Pas de détails techniques dans les steps (pas de noms de classes, d'endpoints, de schémas SQL)

## Exemple

```gherkin
Feature: Recherche dans le référentiel

Pour permettre à l'utilisateur de trouver rapidement une entrée dans le référentiel,
le système doit proposer une recherche par mot-clé retournant les résultats les plus pertinents.

Scenario: Recherche avec résultats
  Given le référentiel contient 50 entrées dont 3 sur le thème "contrat"
  When l'utilisateur recherche "contrat"
  Then 3 résultats sont affichés
  And chaque résultat affiche le titre et un extrait contextuel

Scenario: Recherche sans résultat
  Given le référentiel ne contient aucune entrée sur le thème "xyzzy"
  When l'utilisateur recherche "xyzzy"
  Then un message "Aucun résultat" est affiché
  And aucun résultat n'est listé
```

## Après la rédaction

- Relire : chaque scenario est-il indépendant et testable isolément ?
- Si une décision d'architecture est impliquée, créer aussi un ADR (`docs/architecture/adrs/`)
