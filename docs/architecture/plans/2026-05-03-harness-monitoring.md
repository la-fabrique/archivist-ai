# Harness Monitoring Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deploy a local OTEL Collector + Prometheus + Grafana stack that transforms Claude Code's native hook events into actionable Prometheus metrics and a pre-built dashboard.

**Architecture:** Claude Code emits `hook_execution_complete` events via OTLP/gRPC to an OTEL Collector, which uses the `count` connector to derive Prometheus metrics. Prometheus scrapes the collector. Grafana auto-provisions a "Harness Health" dashboard.

**Tech Stack:** Docker Compose, OpenTelemetry Collector Contrib, Prometheus, Grafana

---

## File Structure

```
.harness/monitoring/
├── docker-compose.yml          # 3 services: otel-collector, prometheus, grafana
├── claude-env.sh               # env vars to source before `claude`
├── otel-collector.yaml         # receiver → count connector → prometheus exporter
├── prometheus.yml              # scrape otel-collector :8889
└── grafana/
    └── provisioning/
        ├── datasources/
        │   └── prometheus.yml  # auto-provision Prometheus datasource
        └── dashboards/
            ├── dashboard.yml   # tells Grafana where to find JSON dashboards
            └── harness-health.json  # 4-panel dashboard
```

---

### Task 1: claude-env.sh

**Files:**
- Create: `.harness/monitoring/claude-env.sh`

- [ ] **Step 1: Create the env file**

```bash
#!/usr/bin/env bash
# Source this before running `claude` to enable harness monitoring.
# Requires: docker compose up -d in this directory.

export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_LOGS_EXPORTER=otlp
export OTEL_METRICS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
export OTEL_LOG_TOOL_DETAILS=1
export OTEL_METRIC_EXPORT_INTERVAL=10000
export OTEL_LOGS_EXPORT_INTERVAL=5000
```

- [ ] **Step 2: Make executable and commit**

```bash
chmod +x .harness/monitoring/claude-env.sh
git add .harness/monitoring/claude-env.sh
git commit -m "feat(harnais): add claude-env.sh for OTEL telemetry activation"
```

---

### Task 2: OTEL Collector configuration

**Files:**
- Create: `.harness/monitoring/otel-collector.yaml`

- [ ] **Step 1: Write the collector config**

```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317

connectors:
  count:
    logs:
      hook_fires:
        description: "Hook execution events"
        conditions:
          - 'attributes["event.name"] == "hook_execution_complete"'
        attributes:
          - key: hook_name
          - key: hook_event

processors:
  batch:
    timeout: 5s

exporters:
  prometheus:
    endpoint: 0.0.0.0:8889
    namespace: harness
  debug:
    verbosity: basic

service:
  pipelines:
    logs/input:
      receivers: [otlp]
      processors: [batch]
      exporters: [count, debug]
    metrics/derived:
      receivers: [count]
      processors: [batch]
      exporters: [prometheus]
    metrics/passthrough:
      receivers: [otlp]
      processors: [batch]
      exporters: [prometheus]
```

- [ ] **Step 2: Commit**

```bash
git add .harness/monitoring/otel-collector.yaml
git commit -m "feat(harnais): add OTEL Collector config with count connector"
```

---

### Task 3: Prometheus configuration

**Files:**
- Create: `.harness/monitoring/prometheus.yml`

- [ ] **Step 1: Write prometheus.yml**

```yaml
global:
  scrape_interval: 10s
  evaluation_interval: 10s

scrape_configs:
  - job_name: "otel-collector"
    static_configs:
      - targets: ["otel-collector:8889"]
```

- [ ] **Step 2: Commit**

```bash
git add .harness/monitoring/prometheus.yml
git commit -m "feat(harnais): add Prometheus scrape config"
```

---

### Task 4: Grafana provisioning — datasource

**Files:**
- Create: `.harness/monitoring/grafana/provisioning/datasources/prometheus.yml`

- [ ] **Step 1: Write datasource provisioning**

```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: false
```

- [ ] **Step 2: Commit**

```bash
git add .harness/monitoring/grafana/provisioning/datasources/prometheus.yml
git commit -m "feat(harnais): add Grafana Prometheus datasource provisioning"
```

---

### Task 5: Grafana provisioning — dashboard loader

**Files:**
- Create: `.harness/monitoring/grafana/provisioning/dashboards/dashboard.yml`

- [ ] **Step 1: Write dashboard provisioning config**

```yaml
apiVersion: 1

providers:
  - name: "Harness"
    orgId: 1
    folder: "Harness"
    type: file
    disableDeletion: false
    editable: true
    options:
      path: /etc/grafana/provisioning/dashboards
      foldersFromFilesStructure: false
```

- [ ] **Step 2: Commit**

```bash
git add .harness/monitoring/grafana/provisioning/dashboards/dashboard.yml
git commit -m "feat(harnais): add Grafana dashboard provisioning config"
```

---

### Task 6: Grafana dashboard JSON

**Files:**
- Create: `.harness/monitoring/grafana/provisioning/dashboards/harness-health.json`

- [ ] **Step 1: Write the dashboard JSON**

```json
{
  "uid": "harness-health",
  "title": "Harness Health",
  "tags": ["harness", "hooks"],
  "timezone": "browser",
  "refresh": "10s",
  "time": { "from": "now-1h", "to": "now" },
  "templating": {
    "list": [
      {
        "name": "hook_name",
        "type": "query",
        "datasource": { "type": "prometheus", "uid": "PBFA97CFB590B2093" },
        "query": "label_values(harness_hook_fires_total, hook_name)",
        "multi": true,
        "includeAll": true,
        "current": { "text": "All", "value": "$__all" },
        "refresh": 2
      }
    ]
  },
  "panels": [
    {
      "id": 1,
      "title": "Hook Activity",
      "type": "timeseries",
      "gridPos": { "h": 8, "w": 12, "x": 0, "y": 0 },
      "targets": [
        {
          "expr": "rate(harness_hook_fires_total{hook_name=~\"$hook_name\"}[5m])",
          "legendFormat": "{{hook_name}}"
        }
      ],
      "datasource": { "type": "prometheus" }
    },
    {
      "id": 2,
      "title": "Block Rate",
      "type": "gauge",
      "gridPos": { "h": 8, "w": 12, "x": 12, "y": 0 },
      "targets": [
        {
          "expr": "sum by (hook_name) (harness_hook_fires_total{hook_name=~\"$hook_name\", hook_event=\"num_blocking\"}) / sum by (hook_name) (harness_hook_fires_total{hook_name=~\"$hook_name\"})",
          "legendFormat": "{{hook_name}}"
        }
      ],
      "datasource": { "type": "prometheus" },
      "fieldConfig": {
        "defaults": {
          "min": 0,
          "max": 1,
          "thresholds": {
            "steps": [
              { "value": 0, "color": "green" },
              { "value": 0.5, "color": "yellow" },
              { "value": 0.8, "color": "red" }
            ]
          },
          "unit": "percentunit"
        }
      }
    },
    {
      "id": 3,
      "title": "Latency P95",
      "type": "timeseries",
      "gridPos": { "h": 8, "w": 12, "x": 0, "y": 8 },
      "targets": [
        {
          "expr": "histogram_quantile(0.95, rate(harness_hook_duration_ms_bucket{hook_name=~\"$hook_name\"}[5m]))",
          "legendFormat": "{{hook_name}} p95"
        }
      ],
      "datasource": { "type": "prometheus" },
      "fieldConfig": { "defaults": { "unit": "ms" } }
    },
    {
      "id": 4,
      "title": "Errors",
      "type": "stat",
      "gridPos": { "h": 8, "w": 12, "x": 12, "y": 8 },
      "targets": [
        {
          "expr": "sum by (hook_name) (increase(harness_hook_fires_total{hook_name=~\"$hook_name\", hook_event=\"num_non_blocking_error\"}[1h]))",
          "legendFormat": "{{hook_name}}"
        }
      ],
      "datasource": { "type": "prometheus" },
      "fieldConfig": {
        "defaults": {
          "thresholds": {
            "steps": [
              { "value": 0, "color": "green" },
              { "value": 1, "color": "red" }
            ]
          }
        }
      }
    }
  ],
  "schemaVersion": 39
}
```

- [ ] **Step 2: Commit**

```bash
git add .harness/monitoring/grafana/provisioning/dashboards/harness-health.json
git commit -m "feat(harnais): add Harness Health Grafana dashboard"
```

---

### Task 7: Docker Compose

**Files:**
- Create: `.harness/monitoring/docker-compose.yml`

- [ ] **Step 1: Write docker-compose.yml**

```yaml
services:
  otel-collector:
    image: otel/opentelemetry-collector-contrib:0.104.0
    command: ["--config", "/etc/otelcol/config.yaml"]
    volumes:
      - ./otel-collector.yaml:/etc/otelcol/config.yaml:ro
    ports:
      - "4317:4317"
      - "8889:8889"

  prometheus:
    image: prom/prometheus:v2.53.0
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus-data:/prometheus
    ports:
      - "9090:9090"
    depends_on:
      - otel-collector

  grafana:
    image: grafana/grafana:11.1.0
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=harness
      - GF_AUTH_ANONYMOUS_ENABLED=true
      - GF_AUTH_ANONYMOUS_ORG_ROLE=Viewer
    volumes:
      - ./grafana/provisioning:/etc/grafana/provisioning:ro
      - grafana-data:/var/lib/grafana
    ports:
      - "3000:3000"
    depends_on:
      - prometheus

volumes:
  prometheus-data:
  grafana-data:
```

- [ ] **Step 2: Commit**

```bash
git add .harness/monitoring/docker-compose.yml
git commit -m "feat(harnais): add docker-compose for monitoring stack"
```

---

### Task 8: Smoke test

**Files:**
- None created — validation only

- [ ] **Step 1: Start the stack**

```bash
cd .harness/monitoring && docker compose up -d
```

Expected: 3 containers running without restart loops. Check with:

```bash
docker compose ps
```

All 3 should show `Up` status.

- [ ] **Step 2: Verify OTEL Collector receives data**

```bash
source .harness/monitoring/claude-env.sh
# In another terminal, run a quick claude session that triggers a hook:
# e.g. edit a file in packages/referentiel/ to trigger referentiel-guard
# Then check collector debug output:
docker compose logs otel-collector | grep -i "hook"
```

Expected: log lines showing received events with `hook_execution_complete`.

- [ ] **Step 3: Verify Prometheus has metrics**

Open http://localhost:9090 and query:

```promql
harness_hook_fires_total
```

Expected: at least one time series with `hook_name` and `hook_event` labels.

- [ ] **Step 4: Verify Grafana dashboard**

Open http://localhost:3000, navigate to Dashboards → Harness → Harness Health.

Expected: 4 panels visible, "Hook Activity" showing data if hooks have fired.

- [ ] **Step 5: Tear down and commit .gitkeep for volumes**

```bash
docker compose down
```

No additional files to commit — smoke test is manual validation.

---

### Task 9: Documentation update

**Files:**
- Modify: `CLAUDE.md` (add harness monitoring entry to doc map)

- [ ] **Step 1: Add monitoring entry to CLAUDE.md doc map**

Add under `## Carte du dépôt`:

```markdown
- `.harness/monitoring/` — stack OTEL locale (Collector + Prometheus + Grafana) → `docs/architecture/specs/2026-05-03-harness-monitoring-design.md`
```

- [ ] **Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "docs(harnais): add monitoring stack to CLAUDE.md doc map"
```
