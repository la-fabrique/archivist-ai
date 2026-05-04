# ADR-006: Stack de monitoring locale pour les hooks du harnais

**Date:** 2026-05-04
**Status:** accepted

## Context

Les hooks du harnais Claude Code émettent nativement des événements OTLP (`hook_execution_complete`) mais aucune infrastructure ne collecte ni n'expose ces signaux. L'activité des garde-fous est donc invisible sans accès aux logs bruts.

## Decision

Déployer une stack Docker Compose locale (OTEL Collector Contrib + Prometheus + Grafana) dans `.harness/monitoring/` qui reçoit les événements OTLP/gRPC de Claude Code, dérive des métriques Prometheus via le connecteur `count`, et les expose dans un dashboard Grafana pré-provisionné "Harness Health".

## Consequences

- Les hooks ne sont pas modifiés — la télémétrie est activée uniquement via les variables d'environnement de `claude-env.sh`.
- Cinq métriques sont disponibles : `harness_hook_fires_total`, `harness_hook_success_total`, `harness_hook_blocks_total`, `harness_hook_errors_total`, `harness_hook_duration_ms`.
- La stack doit être démarrée manuellement avant chaque session (`docker compose up -d`).
- `OTEL_LOG_TOOL_DETAILS=1` est requis pour obtenir le label `hook_name` détaillé dans les métriques.
