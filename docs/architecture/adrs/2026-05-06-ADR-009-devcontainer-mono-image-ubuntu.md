# ADR-009 : Devcontainer mono-image ubuntu:24.04 pour archivist-ai

**Date:** 2026-05-06
**Status:** accepted

## Context

Le dépôt archivist-ai nécessite deux runtimes distincts (Python 3.12 + uv pour `archivist-cli`, Node 20 pour `referentiel-cli`) et une stack monitoring Docker Compose optionnelle dans `.harness/`. Il n'existait pas d'environnement de développement reproductible.

## Options Considered

- **Mono-image custom** : un seul Dockerfile ubuntu:24.04 installe les deux runtimes. Simple, un seul terminal.
- **Multi-service compose** : un conteneur Python + un conteneur Node. Complexité réseau et synchronisation inutile pour un usage dev.

## Decision

Un devcontainer mono-image basé sur `ubuntu:24.04` couvre Python 3.12 (via uv) et Node 20. La stack monitoring reste dans `.harness/` et se démarre séparément — l'intégrer via `docker compose extends` casserait la persistance Prometheus/Grafana (`extends` n'hérite pas les volumes nommés).

## Consequences

- `PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true` est défini dans le Dockerfile : Puppeteer appelle le Chromium de l'hôte, pas du conteneur.
- Le conteneur tourne sous l'utilisateur non-root `vscode` (uid 1000) — convention Dev Containers.
- `postCreateCommand` exécute `uv sync` + `npm install` au premier démarrage ; le venv Python réside dans `packages/archivist-cli/.venv/`.
- La stack monitoring s'active séparément : `docker compose -f .harness/monitoring/compose.yml up -d` depuis l'hôte ; le `network_mode: host` du conteneur dev lui donne accès aux ports locaux.
