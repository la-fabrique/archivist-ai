#!/usr/bin/env bash
# OTEL GenAI instrumentation lib for harness hooks.
# Semconv: opentelemetry.io/docs/specs/semconv/gen-ai/ (snapshot 2026-05-11, Development)
# All functions exit 0 silently if the collector is unreachable.

HARNESS_COLLECTOR_HTTP="${HARNESS_COLLECTOR_HTTP:-http://localhost:4318}"
HARNESS_MODEL="${HARNESS_MODEL:-claude-sonnet-4-6}"

_h_now_nano() { date +%s%N; }
_h_now_sec()  { date +%s; }

# emit_span <name> <trace_id> <span_id> <parent_span_id> <attrs_json_array>
# attrs_json_array: a JSON array of OTLP KeyValue objects, or "[]" for none
# trace_id: 32 hex chars; span_id / parent_span_id: 16 hex chars
emit_span() {
  local name="$1" trace_id="$2" span_id="$3" parent_span_id="$4" attrs="${5:-[]}"
  local ts; ts=$(_h_now_nano)

  local parent_field=""
  [[ -n "$parent_span_id" ]] && parent_field="\"parentSpanId\":\"${parent_span_id}\","

  curl -sf --max-time 2 -X POST "${HARNESS_COLLECTOR_HTTP}/v1/traces" \
    -H "Content-Type: application/json" \
    --data-raw "{\"resourceSpans\":[{
      \"resource\":{\"attributes\":[{\"key\":\"service.name\",\"value\":{\"stringValue\":\"harness\"}}]},
      \"scopeSpans\":[{\"spans\":[{
        \"traceId\":\"${trace_id}\",
        \"spanId\":\"${span_id}\",
        ${parent_field}
        \"name\":\"${name}\",
        \"kind\":3,
        \"startTimeUnixNano\":\"${ts}\",
        \"endTimeUnixNano\":\"${ts}\",
        \"attributes\":${attrs}
      }]}]
    }]}" 2>/dev/null || true
}

# emit_session_metric <session_id> <branch>
# Emits gauge "session_info" with value = unix timestamp (used by Grafana table)
emit_session_metric() {
  local session_id="$1" branch="$2"
  local ts_nano ts_sec
  ts_nano=$(_h_now_nano)
  ts_sec=$(_h_now_sec)

  curl -sf --max-time 2 -X POST "${HARNESS_COLLECTOR_HTTP}/v1/metrics" \
    -H "Content-Type: application/json" \
    --data-raw "{\"resourceMetrics\":[{
      \"resource\":{\"attributes\":[{\"key\":\"service.name\",\"value\":{\"stringValue\":\"harness\"}}]},
      \"scopeMetrics\":[{\"metrics\":[{
        \"name\":\"session_info\",
        \"gauge\":{\"dataPoints\":[{
          \"attributes\":[
            {\"key\":\"session_id\",\"value\":{\"stringValue\":\"${session_id}\"}},
            {\"key\":\"branch\",\"value\":{\"stringValue\":\"${branch}\"}}
          ],
          \"timeUnixNano\":\"${ts_nano}\",
          \"asDouble\":${ts_sec}
        }]}
      }]}]
    }]}" 2>/dev/null || true
}

# emit_skill_metric <session_id> <skill_name> <branch>
# Emits gauge "skill_invoked" with value = 1 (counted per session in Prometheus)
emit_skill_metric() {
  local session_id="$1" skill_name="$2" branch="$3"
  local ts_nano; ts_nano=$(_h_now_nano)

  curl -sf --max-time 2 -X POST "${HARNESS_COLLECTOR_HTTP}/v1/metrics" \
    -H "Content-Type: application/json" \
    --data-raw "{\"resourceMetrics\":[{
      \"resource\":{\"attributes\":[{\"key\":\"service.name\",\"value\":{\"stringValue\":\"harness\"}}]},
      \"scopeMetrics\":[{\"metrics\":[{
        \"name\":\"skill_invoked\",
        \"gauge\":{\"dataPoints\":[{
          \"attributes\":[
            {\"key\":\"session_id\",\"value\":{\"stringValue\":\"${session_id}\"}},
            {\"key\":\"skill_name\",\"value\":{\"stringValue\":\"${skill_name}\"}},
            {\"key\":\"branch\",\"value\":{\"stringValue\":\"${branch}\"}}
          ],
          \"timeUnixNano\":\"${ts_nano}\",
          \"asDouble\":1
        }]}
      }]}]
    }]}" 2>/dev/null || true
}
