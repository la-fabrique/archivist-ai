# Harness Monitoring — Design Spec

## Objectif

Monitorer l'activité des garde-fous (hooks) du harnais Claude Code via la télémétrie OTEL native, avec une stack locale Prometheus + Grafana.

## Architecture

```
┌─────────────┐      OTLP/gRPC       ┌────────────────┐
│ Claude Code │ ───────────────────▶  │ OTEL Collector │
│  (hooks)    │      :4317            │  (contrib)     │
└─────────────┘                       └───────┬────────┘
                                              │
                              transform processor
                              (events → metrics)
                                              │
                                    ┌─────────▼─────────┐
                                    │    Prometheus      │
                                    │    :9090           │
                                    └─────────┬─────────┘
                                              │
                                    ┌─────────▼─────────┐
                                    │     Grafana        │
                                    │     :3000          │
                                    └───────────────────┘
```

3 containers (docker-compose) :

1. **otel-collector** (`otel/opentelemetry-collector-contrib`) — reçoit OTLP, transforme les events hook en métriques Prometheus
2. **prometheus** — scrape le collector, stocke les time series
3. **grafana** — dashboard pré-provisionné "Harness Health"

## Signal source

Événements OTEL natifs de Claude Code (aucune modification des hooks nécessaire) :

- `claude_code.hook_execution_start` — `hook_event`, `hook_name`, `num_hooks`
- `claude_code.hook_execution_complete` — `hook_event`, `hook_name`, `num_success`, `num_blocking`, `num_non_blocking_error`, `total_duration_ms`

Variable `OTEL_LOG_TOOL_DETAILS=1` requise pour obtenir `hook_name` détaillé.

## Métriques dérivées

| Métrique Prometheus | Type | Labels | Source (attribut OTEL) |
|---|---|---|---|
| `harness_hook_fires_total` | counter | `hook_name`, `hook_event` | comptage des events |
| `harness_hook_success_total` | counter | `hook_name`, `hook_event` | `num_success` |
| `harness_hook_blocks_total` | counter | `hook_name`, `hook_event` | `num_blocking` |
| `harness_hook_errors_total` | counter | `hook_name`, `hook_event` | `num_non_blocking_error` |
| `harness_hook_duration_ms` | histogram | `hook_name`, `hook_event` | `total_duration_ms` |

## Requêtes clés

- **Hook vivant ?** → `rate(harness_hook_fires_total[1h]) > 0`
- **Taux de blocage** → `harness_hook_blocks_total / harness_hook_fires_total`
- **Latence P95** → `histogram_quantile(0.95, harness_hook_duration_ms)`
- **Hooks en erreur** → alerte si `rate(harness_hook_errors_total[5m]) > 0`

## Arborescence fichiers

```
.harness/monitoring/
├── docker-compose.yml
├── claude-env.sh
├── otel-collector.yaml
├── prometheus.yml
└── grafana/
    └── provisioning/
        ├── datasources/
        │   └── prometheus.yml
        └── dashboards/
            ├── dashboard.yml
            └── harness-health.json
```

## Configuration Claude Code

Fichier `claude-env.sh` à sourcer avant de lancer `claude` :

```bash
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_LOGS_EXPORTER=otlp
export OTEL_METRICS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
export OTEL_LOG_TOOL_DETAILS=1
export OTEL_METRIC_EXPORT_INTERVAL=10000
```

## Dashboard Grafana — "Harness Health"

4 panneaux :

| Panneau | Type | Query |
|---|---|---|
| Hook Activity | Time series | `rate(harness_hook_fires_total[5m])` par `hook_name` |
| Block Rate | Stat + gauge | `sum(blocks) / sum(fires)` par `hook_name` |
| Latency P95 | Time series | `histogram_quantile(0.95, rate(duration_bucket[5m]))` |
| Errors | Stat (rouge si > 0) | `sum(increase(errors_total[1h]))` par `hook_name` |

Variable template : `$hook_name` (multi-select, auto-populated).

## Usage

```bash
cd .harness/monitoring && docker compose up -d
source .harness/monitoring/claude-env.sh
claude
```

## Évolutions futures

- **Phase B** : métriques d'observabilité agent (tokens, itérations, drift)
- **Phase C** : métriques de fiabilité (conformité ADRs, régressions)
- Monitoring des skills via event `claude_code.skill_activated`
