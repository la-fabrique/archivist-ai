#!/usr/bin/env bash
# SessionStart hook: vérifie et démarre la stack monitoring si nécessaire.

COLLECTOR_HOST="localhost"
COLLECTOR_PORT="4317"
COMPOSE_FILE="$(dirname "$0")/../monitoring/compose.yml"

if nc -z -w1 "$COLLECTOR_HOST" "$COLLECTOR_PORT" 2>/dev/null; then
  exit 0
fi

# Collector inaccessible — démarrer la stack
docker compose -f "$COMPOSE_FILE" up -d 2>/dev/null

# Attendre jusqu'à 10s que le collector réponde
for i in $(seq 1 10); do
  sleep 1
  if nc -z -w1 "$COLLECTOR_HOST" "$COLLECTOR_PORT" 2>/dev/null; then
    jq -n '{"systemMessage": "HARNAIS: stack monitoring démarrée (Collector + Prometheus + Grafana sur :3000)"}'
    exit 0
  fi
done

jq -n '{"systemMessage": "HARNAIS: impossible de démarrer le Collector sur localhost:4317 — vérifier docker ou lancer: npm run monitoring:up"}'
