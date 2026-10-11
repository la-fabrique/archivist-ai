# ADR-014: Port Agent (contexte de dossier et session) dans notes-cli

**Date:** 2026-10-11
**Status:** accepted

## Context
`notes add idea` confie une idée à un agent installé dans un dossier (le bloc-notes), qui porte ses propres réglages, skills et hooks. L'échange est multi-tours et non interactif : chaque tour est une invocation qui se termine, car l'appelant est typiquement une session Claude sans terminal. Cet ADR complète sans les remplacer :
- ADR-004 (registre d'adaptateurs, versioning des ports)
- ADR-005 (port LanguageModel unique)
- ADR-013 (package partagé cli-core)

## Options Considered
- **Étendre `LanguageModel`** (`cwd`, `session_id`, schéma optionnel) : écartée, mélange deux formes d'interaction et rend le contrat flou.
- **Port technique générique `Agent`** : retenue.
- **Port métier `BlocNotes`** (`add_idea`, `reply`) : écartée, le port grossirait à chaque nouvelle commande.

## Decision
Créer dans `notes_cli.domain` un port générique `Agent` avec `send(message, session_id=None) -> AgentReply(session_id, text)` et `AgentError`. Le dossier de travail est fixé à la construction de l'adaptateur, jamais passé à `send`.

## Consequences
- `LanguageModel` reste le port unique des appels à schéma en un seul appel (archivist-cli, inchangé) ; `Agent` couvre le texte libre avec session, sans que `LanguageModel` reçoive `cwd`, `session_id` ni schéma optionnel.
- `Agent` vit dans `notes-cli`, pas dans `cli-core` : une seule CLI l'utilise (règle des deux CLIs d'ADR-013).
- Le domaine ne connaît ni le chemin du bloc-notes ni Claude : le registre lit le dossier dans la config et le passe à la factory de l'adaptateur (`{"workspace": <chemin>}`).
- Le use case compose le message (`"/add <idée>"`) ; une nouvelle commande (`notes add task`, `notes ask`…) ajoute un use case sans modifier le port.
- L'identifiant de session est connu avant l'appel : sans `session_id`, l'adaptateur génère lui-même l'UUID, et `AgentError` porte un `session_id` optionnel pour reprendre la conversation après un échec ou un délai dépassé.
