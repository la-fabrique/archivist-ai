#!/usr/bin/env bash
# Claude Code status line script
# LEFT:  model | branch | context% | tokens_in | tokens_out
# RIGHT: 5h session% | time_remaining | 7d weekly%

input=$(cat)

# --- Parse fields ---
model=$(echo "$input" | jq -r '.model.display_name // .model.id // "unknown"')
branch=$(echo "$input" | jq -r '.workspace.git_worktree // empty')
if [ -z "$branch" ]; then
  branch=$(git -C "$(echo "$input" | jq -r '.workspace.current_dir // "/workspace"')" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")
fi

ctx_used=$(echo "$input" | jq -r '.context_window.used_percentage // empty')
tokens_in=$(echo "$input" | jq -r '.context_window.current_usage.input_tokens // empty')
tokens_out=$(echo "$input" | jq -r '.context_window.current_usage.output_tokens // empty')

five_h_pct=$(echo "$input" | jq -r '.rate_limits.five_hour.used_percentage // empty')
five_h_resets=$(echo "$input" | jq -r '.rate_limits.five_hour.resets_at // empty')
seven_d_pct=$(echo "$input" | jq -r '.rate_limits.seven_day.used_percentage // empty')

# --- Colors (dim-friendly) ---
RESET=$'\033[0m'
BOLD=$'\033[1m'
DIM=$'\033[2m'
CYAN=$'\033[36m'
YELLOW=$'\033[33m'
GREEN=$'\033[32m'
MAGENTA=$'\033[35m'
BLUE=$'\033[34m'
RED=$'\033[31m'

# --- Build LEFT segment ---
left=""

# Model
left+="${CYAN}${model}${RESET}"

# Branch
left+=" ${DIM}|${RESET} ${BLUE}${branch}${RESET}"

# Context %
if [ -n "$ctx_used" ]; then
  ctx_int=$(printf "%.0f" "$ctx_used")
  if [ "$ctx_int" -ge 80 ]; then
    ctx_color="$RED"
  elif [ "$ctx_int" -ge 50 ]; then
    ctx_color="$YELLOW"
  else
    ctx_color="$GREEN"
  fi
  left+=" ${DIM}|${RESET} ${ctx_color}ctx:${ctx_int}%${RESET}"
fi

# Tokens in
if [ -n "$tokens_in" ] && [ "$tokens_in" != "null" ]; then
  if [ "$tokens_in" -ge 1000 ]; then
    tokens_in_fmt="$(echo "$tokens_in" | awk '{printf "%.1fk", $1/1000}')"
  else
    tokens_in_fmt="${tokens_in}"
  fi
  left+=" ${DIM}|${RESET} ${MAGENTA}in:${tokens_in_fmt}${RESET}"
fi

# Tokens out
if [ -n "$tokens_out" ] && [ "$tokens_out" != "null" ]; then
  if [ "$tokens_out" -ge 1000 ]; then
    tokens_out_fmt="$(echo "$tokens_out" | awk '{printf "%.1fk", $1/1000}')"
  else
    tokens_out_fmt="${tokens_out}"
  fi
  left+=" ${DIM}|${RESET} ${YELLOW}out:${tokens_out_fmt}${RESET}"
fi

# --- Build RIGHT segment ---
right=""

# 5-hour session %
if [ -n "$five_h_pct" ]; then
  five_h_int=$(printf "%.0f" "$five_h_pct")
  if [ "$five_h_int" -ge 80 ]; then
    five_color="$RED"
  elif [ "$five_h_int" -ge 50 ]; then
    five_color="$YELLOW"
  else
    five_color="$GREEN"
  fi
  right+="${five_color}session:${five_h_int}%${RESET}"
fi

# Time remaining in 5h session
if [ -n "$five_h_resets" ] && [ "$five_h_resets" != "null" ]; then
  now=$(date +%s)
  remaining_secs=$(( five_h_resets - now ))
  if [ "$remaining_secs" -gt 0 ]; then
    remaining_min=$(( remaining_secs / 60 ))
    if [ "$remaining_min" -ge 60 ]; then
      remaining_str="$(( remaining_min / 60 ))h$(( remaining_min % 60 ))m"
    else
      remaining_str="${remaining_min}m"
    fi
    [ -n "$right" ] && right+=" ${DIM}|${RESET} "
    right+="${DIM}resets:${remaining_str}${RESET}"
  fi
fi

# 7-day weekly %
if [ -n "$seven_d_pct" ]; then
  seven_d_int=$(printf "%.0f" "$seven_d_pct")
  if [ "$seven_d_int" -ge 80 ]; then
    week_color="$RED"
  elif [ "$seven_d_int" -ge 50 ]; then
    week_color="$YELLOW"
  else
    week_color="$GREEN"
  fi
  [ -n "$right" ] && right+=" ${DIM}|${RESET} "
  right+="${week_color}week:${seven_d_int}%${RESET}"
fi

printf '%s  %s\n' "$left" "$right"
