# Harnais Claude Code — archivist-ai

Infrastructure d'ingénierie autour de l'agent de dev.

## Hooks actifs (`settings.json`)

| Événement | Hook | Effet |
|-----------|------|-------|
| `PreToolUse` (Write\|Edit) | `.claude/hooks/referentiel-guard.sh` | Bloque toute écriture dans `packages/referentiel/` hors fichiers autorisés |
| `PostToolUse` (Bash) | `.claude/hooks/commit-lint.sh` | Vérifie le format Conventional Commits après chaque `git commit` |
| `SessionStart` | `.harness/scripts/session-start.sh` | Démarre la stack monitoring si le Collector n'est pas joignable |

## Monitoring (`monitoring/`)

Stack Docker locale : OTEL Collector → Prometheus → Grafana.

- Collector reçoit les events OTEL natifs de Claude Code (`hook_execution_complete`, etc.)
- Prometheus scrape `:8889`, stocke les time series
- Grafana `:3000` — dashboard "Harness Health" pré-provisionné (4 panneaux)

```bash
docker compose -f .harness/monitoring/compose.yml up -d
# ou : npm run monitoring:up
```

Variables d'environnement requises (sourcer avant `claude`) :

```bash
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_LOGS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
export OTEL_LOG_TOOL_DETAILS=1
```

Spec complète : `docs/architecture/specs/2026-05-03-harness-monitoring-design.md`

## Scripts (`scripts/`)

| Script | Usage |
|--------|-------|
| `session-start.sh` | Hook SessionStart — démarre monitoring si absent |
| `check_claude_coverage.py` | Vérifie que chaque `packages/*` est documenté dans CLAUDE.md |
