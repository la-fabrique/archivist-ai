#!/usr/bin/env bash
# Installe ou met à jour le binaire notes depuis la dernière release notes-cli/*.
# Lancé par le hook SessionStart : silencieux et jamais bloquant (sort toujours 0).
set -u

API="https://api.github.com/repos/la-fabrique/archivist-ai/releases?per_page=100"
tmp=""
trap 'rm -f "${tmp:-}"' EXIT
trap 'exit 0' HUP INT TERM
DATA="${CLAUDE_PLUGIN_DATA:-${CLAUDE_CONFIG_DIR:-$HOME/.claude}/plugins/data/notes-archivist}"

install_latest() {
  local asset json url tag
  case "$(uname -s)/$(uname -m)" in
    Linux/x86_64) asset=notes-linux ;;
    Darwin/arm64) asset=notes-macos-arm64 ;;
    *) return 0 ;;
  esac

  json=$(curl -fsSL --proto '=https' --proto-redir '=https' --max-time 5 -H 'Accept: application/vnd.github+json' "$API") || return 0
  # Les releases arrivent de la plus récente à la plus ancienne : la première URL notes-cli/ est la dernière.
  url=$(printf '%s' "$json" \
    | grep -o "\"browser_download_url\": *\"[^\"]*/releases/download/notes-cli/[^\"]*/$asset\"" \
    | head -n1 | sed 's/.*"\(https:[^"]*\)"$/\1/')
  case "$url" in
    https://github.com/la-fabrique/archivist-ai/releases/download/notes-cli/*) ;;
    *) return 0 ;;
  esac
  tag=${url#*/releases/download/}
  tag=${tag%/"$asset"}

  if [ -x "$DATA/notes" ] && [ "$(cat "$DATA/version" 2>/dev/null)" = "$tag" ]; then
    return 0
  fi

  mkdir -p "$DATA" || return 0
  tmp=$(mktemp "$DATA/.notes.XXXXXX") || return 0
  if curl -fsSL --proto '=https' --proto-redir '=https' --max-time 60 -o "$tmp" "$url" && chmod +x "$tmp" && mv -f "$tmp" "$DATA/notes"; then
    printf '%s\n' "$tag" > "$DATA/version"
  else
    rm -f "$tmp"
  fi
}

install_latest >/dev/null 2>&1
exit 0
